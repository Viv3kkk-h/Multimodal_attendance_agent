
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def read_csv_rows(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")

    with file_path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"No data rows found in {file_path.name}")

    return rows


def build_multimodal_summary():
    attendance_rows = read_csv_rows(
        RESULTS_DIR / "attendance_summary.csv"
    )
    audio_activity_rows = read_csv_rows(
        RESULTS_DIR / "audio_activity_summary.csv"
    )
    audio_feature_rows = read_csv_rows(
        RESULTS_DIR / "audio_features.csv"
    )

    # Use the most recent saved attendance session.
    attendance = attendance_rows[-1]
    audio_activity = audio_activity_rows[-1]
    audio_features = audio_feature_rows[-1]

    visual_duration = float(attendance["session_duration_seconds"])
    audio_duration = float(audio_activity["duration_seconds"])

    # Activity 4.2: Experimental multimodal signal fusion
    visual_presence_percent = float(
        attendance["estimated_presence_percent"]
    )

    audio_activity_percent = float(
        audio_activity["possible_activity_percent"]
    )

    fusion_index = round(
        (visual_presence_percent + audio_activity_percent) / 2,
        2
    )

    # Activity 4.3: Experimental scoring category
    experimental_score = fusion_index

    if experimental_score < 40:
        signal_level = "Lower combined signal level"
    elif experimental_score < 70:
        signal_level = "Moderate combined signal level"
    else:
        signal_level = "Higher combined signal level"

    summary = {
        "visual_session_end": attendance["session_end"],
        "visual_session_duration_seconds": visual_duration,
        "observed_presence_seconds": float(
            attendance["observed_presence_seconds"]
        ),
        "estimated_presence_percent": float(
            attendance["estimated_presence_percent"]
        ),
        "audio_file": audio_activity["audio_file"],
        "audio_duration_seconds": audio_duration,
        "audio_sample_rate_hz": audio_activity["sample_rate_hz"],
        "possible_audio_activity_percent": float(
            audio_activity["possible_activity_percent"]
        ),
        "experimental_fusion_index_percent": fusion_index,
        "fusion_method": "Equal-weight arithmetic mean",
        "fusion_validity": (
            "Exploratory only; recordings are not synchronized "
            "and audio activity is not verified speech."
        ),
        "experimental_engagement_score_percent": experimental_score,
        "experimental_signal_level": signal_level,
        "scoring_method": (
            "Equal-weight average of visual presence and "
            "possible audio activity, with heuristic thresholds"
        ),
        "scoring_limitation": (
            "Not a validated engagement measure; recordings "
            "are not synchronized and audio activity is not "
            "verified speech."
        ),
        "audio_rms_mean": audio_features["rms_mean"],
        "audio_zero_crossing_rate_mean": (
            audio_features["zero_crossing_rate_mean"]
        ),
        "audio_spectral_centroid_mean_hz": (
            audio_features["spectral_centroid_mean_hz"]
        ),
        "duration_difference_seconds": round(
            abs(visual_duration - audio_duration), 3
        ),
        "synchronization_status": (
            "Not synchronized; separate recordings"
        ),
        "engagement_score": "Not calculated in Activity 4.1",
        "interpretation_note": (
            "Visual presence and audio activity are proxies, "
            "not verified attention or engagement measurements."
        ),
    }

    output_path = RESULTS_DIR / "multimodal_session_summary.csv"

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=summary.keys()
        )
        writer.writeheader()
        writer.writerow(summary)

    return summary, output_path


def main():
    try:
        summary, output_path = build_multimodal_summary()

        print("\nMultimodal agent executed successfully!\n")

        for key, value in summary.items():
            print(f"{key}: {value}")

        print(f"\nCombined summary saved to: {output_path}")

    except (FileNotFoundError, ValueError, KeyError) as error:
        print(f"Agent error: {error}")


if __name__ == "__main__":
    main()
