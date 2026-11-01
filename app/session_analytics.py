
import csv
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"No data found in {path.name}")

    return rows


def build_report():
    summary_rows = read_csv(
        RESULTS_DIR / "multimodal_session_summary.csv"
    )
    feature_rows = read_csv(
        RESULTS_DIR / "audio_features.csv"
    )
    recommendation_rows = read_csv(
        RESULTS_DIR / "recommendations.csv"
    )

    summary = summary_rows[-1]
    features = feature_rows[-1]

    report = [
        "MULTIMODAL ATTENDANCE AND ENGAGEMENT AGENT",
        "INDIVIDUAL SESSION ANALYTICS REPORT",
        "=" * 55,
        f"Report generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "1. VISUAL SESSION",
        "-" * 30,
        f"Session end: {summary['visual_session_end']}",
        f"Session duration: {summary['visual_session_duration_seconds']} seconds",
        f"Observed presence: {summary['observed_presence_seconds']} seconds",
        f"Estimated visual presence: {summary['estimated_presence_percent']}%",
        "",
        "2. AUDIO ANALYTICS",
        "-" * 30,
        f"Audio file: {features['audio_file']}",
        f"Duration: {features['duration_seconds']} seconds",
        f"Sample rate: {features['sample_rate_hz']} Hz",
        f"Mean RMS energy: {features['rms_mean']}",
        f"Mean zero-crossing rate: {features['zero_crossing_rate_mean']}",
        f"Mean spectral centroid: {features['spectral_centroid_mean_hz']} Hz",
        f"Possible audio activity: {summary['possible_audio_activity_percent']}%",
        "",
        "3. MULTIMODAL ANALYSIS",
        "-" * 30,
        f"Experimental fusion index: {summary['experimental_fusion_index_percent']}%",
        f"Signal-level category: {summary['experimental_signal_level']}",
        f"Fusion method: {summary['fusion_method']}",
        f"Synchronization: {summary['synchronization_status']}",
        f"Duration difference: {summary['duration_difference_seconds']} seconds",
        "",
        "4. RECOMMENDATIONS",
        "-" * 30,
    ]

    for item in recommendation_rows:
        report.extend([
            f"Area: {item['area']}",
            f"Observation: {item['observation']}",
            f"Recommendation: {item['recommendation']}",
            "",
        ])

    report.extend([
        "5. LIMITATIONS AND RESPONSIBLE USE",
        "-" * 30,
        "Visual presence is an estimate, not identity verification.",
        "Audio energy does not confirm speech or participation.",
        "The visual and audio recordings are not synchronized.",
        "The experimental fusion index is not a validated engagement score.",
        "Do not use this report alone to judge attention, performance, or ability.",
        "Collect data with appropriate consent and protect recordings.",
        "",
        "END OF REPORT",
    ])

    output_path = RESULTS_DIR / "session_analytics_report.txt"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    return output_path


def main():
    try:
        output_path = build_report()
        print("Activity 5.2: Session analytics report generated!")
        print(f"Report saved to: {output_path}")
        print("\nReport preview:\n")
        print(output_path.read_text(encoding="utf-8"))

    except (FileNotFoundError, ValueError, KeyError) as error:
        print(f"Analytics report error: {error}")


if __name__ == "__main__":
    main()
