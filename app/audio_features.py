
import argparse
import csv
from pathlib import Path
import soundfile as sf

import librosa
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def extract_audio_features(audio_path):
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    # Load audio at its original sample rate.
    signal, sample_rate = librosa.load(
        str(audio_path),
        sr=None,
        mono=True,
    )

    if signal.size == 0:
        raise ValueError("The audio file is empty.")

    # Calculate basic signal features.
    duration_seconds = len(signal) / sample_rate

    rms = librosa.feature.rms(y=signal)[0]
    zero_crossing_rate = (
        librosa.feature.zero_crossing_rate(y=signal)[0]
    )
    spectral_centroid = librosa.feature.spectral_centroid(
        y=signal,
        sr=sample_rate,
    )[0]

    features = {
        "audio_file": audio_path.name,
        "sample_rate_hz": sample_rate,
        "duration_seconds": round(duration_seconds, 3),
        "rms_mean": round(float(np.mean(rms)), 6),
        "zero_crossing_rate_mean": round(
            float(np.mean(zero_crossing_rate)), 6
        ),
        "spectral_centroid_mean_hz": round(
            float(np.mean(spectral_centroid)), 3
        ),
    }

    return features


def save_features(features):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "audio_features.csv"

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=features.keys()
        )
        writer.writeheader()
        writer.writerow(features)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Extract basic audio signal features."
    )
    parser.add_argument(
        "audio_path",
        help="Path to a WAV or other supported audio file",
    )
    args = parser.parse_args()

    try:
        features = extract_audio_features(args.audio_path)
        output_path = save_features(features)

        print("\nAudio features extracted successfully!")
        for name, value in features.items():
            print(f"{name}: {value}")

        print(f"\nResults saved to: {output_path}")

    except (
        FileNotFoundError,
        ValueError,
        sf.LibsndfileError,
    ) as error:
        print(f"Error: Unable to process audio file. {error}")


if __name__ == "__main__":
    main()
