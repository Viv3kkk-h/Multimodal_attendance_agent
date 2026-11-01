
import argparse
import csv
from pathlib import Path

import librosa
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

FRAME_LENGTH = 0.03  # 30 milliseconds
HOP_LENGTH = 0.01    # Analyze every 10 milliseconds


def analyze_audio(audio_path):
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    signal, sample_rate = librosa.load(
        str(audio_path), sr=None, mono=True
    )

    if signal.size == 0:
        raise ValueError("The audio file is empty.")

    frame_size = max(1, int(FRAME_LENGTH * sample_rate))
    hop_size = max(1, int(HOP_LENGTH * sample_rate))

    # Measure the energy of overlapping audio frames.
    rms_values = []

    for start in range(0, len(signal), hop_size):
        frame = signal[start:start + frame_size]

        if len(frame) == 0:
            continue

        rms = np.sqrt(np.mean(frame ** 2))
        rms_values.append(float(rms))

    rms_values = np.array(rms_values)

    # Estimate the background level from quieter frames.
    noise_floor = float(np.percentile(rms_values, 20))
    threshold = max(noise_floor * 2.5, 0.01)

    frame_results = []
    active_frames = 0

    for index, rms in enumerate(rms_values):
        start_time = index * hop_size / sample_rate
        end_time = min(
            start_time + FRAME_LENGTH,
            len(signal) / sample_rate
        )

        active = bool(rms >= threshold)

        if active:
            active_frames += 1
            label = "Possible speech or sound activity"
        else:
            label = "Low-energy audio"

        frame_results.append({
            "start_seconds": round(start_time, 3),
            "end_seconds": round(end_time, 3),
            "rms_energy": round(float(rms), 6),
            "activity_label": label,
        })

    total_duration = len(signal) / sample_rate
    # Each frame represents one hop interval for duration estimation.
    active_duration = min(
    active_frames * HOP_LENGTH,
    total_duration
    )

    active_percent = active_duration / total_duration * 100

    # Overlapping frames mean active_duration is approximate.
    active_percent = (
        min(active_duration, total_duration) / total_duration * 100
    )

    summary = {
        "audio_file": audio_path.name,
        "duration_seconds": round(total_duration, 3),
        "sample_rate_hz": sample_rate,
        "energy_threshold": round(threshold, 6),
        "possible_activity_seconds": round(
            min(active_duration, total_duration), 3
        ),
        "low_energy_seconds": round(
            max(0, total_duration - min(active_duration, total_duration)),
            3
        ),
        "possible_activity_percent": round(active_percent, 2),
        "method": "RMS energy threshold; not verified speech detection",
    }

    return frame_results, summary


def save_results(frame_results, summary):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    frames_path = RESULTS_DIR / "audio_activity_frames.csv"
    summary_path = RESULTS_DIR / "audio_activity_summary.csv"

    with frames_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=frame_results[0].keys()
        )
        writer.writeheader()
        writer.writerows(frame_results)

    with summary_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=summary.keys())
        writer.writeheader()
        writer.writerow(summary)

    return frames_path, summary_path


def main():
    parser = argparse.ArgumentParser(
        description="Estimate audio activity using RMS energy."
    )
    parser.add_argument(
        "audio_path",
        help="Path to an audio file, such as sample_audio.wav"
    )
    args = parser.parse_args()

    try:
        frames, summary = analyze_audio(args.audio_path)
        frames_path, summary_path = save_results(frames, summary)

        print("\nAudio activity analysis completed!\n")

        for name, value in summary.items():
            print(f"{name}: {value}")

        print(f"\nFrame-level results: {frames_path}")
        print(f"Session summary: {summary_path}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
