
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def read_latest_summary():
    input_path = RESULTS_DIR / "multimodal_session_summary.csv"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Summary file not found: {input_path}"
        )

    with input_path.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("The multimodal summary contains no data.")

    return rows[-1]


def generate_recommendations(summary):
    recommendations = []

    presence = float(summary["estimated_presence_percent"])
    audio_activity = float(
        summary["possible_audio_activity_percent"]
    )
    synchronization = summary["synchronization_status"]

    if presence < 60:
        recommendations.append({
            "area": "Visual input",
            "observation": (
                f"Estimated visual presence was {presence:.2f}%."
            ),
            "recommendation": (
                "Check camera positioning, lighting, and face "
                "detection before drawing conclusions."
            ),
        })

    if audio_activity < 20:
        recommendations.append({
            "area": "Audio input",
            "observation": (
                f"Possible audio activity was {audio_activity:.2f}%."
            ),
            "recommendation": (
                "Check microphone levels and recording quality. "
                "Low-energy audio does not necessarily mean silence."
            ),
        })

    if "Not synchronized" in synchronization:
        recommendations.append({
            "area": "Data synchronization",
            "observation": (
                "The visual and audio recordings were not synchronized."
            ),
            "recommendation": (
                "Record synchronized timestamps and align the "
                "measurements before interpreting them together."
            ),
        })

    if not recommendations:
        recommendations.append({
            "area": "Data quality",
            "observation": (
                "The basic input-quality thresholds were not triggered."
            ),
            "recommendation": (
                "Continue collecting quality-checked data and validate "
                "the system under different recording conditions."
            ),
        })

    recommendations.append({
        "area": "Interpretation and privacy",
        "observation": (
            "Visual presence and audio energy are indirect signals."
        ),
        "recommendation": (
            "Do not treat these measurements as proof of attention "
            "or engagement. Use consent-based data collection and "
            "protect recordings."
        ),
    })

    return recommendations


def save_recommendations(recommendations):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "recommendations.csv"

    fieldnames = [
        "area",
        "observation",
        "recommendation",
    ]

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recommendations)

    return output_path


def main():
    try:
        summary = read_latest_summary()
        recommendations = generate_recommendations(summary)
        output_path = save_recommendations(recommendations)

        print("\nActivity 5.1: Recommendations generated!\n")

        for item in recommendations:
            print(f"[{item['area']}]")
            print(f"Observation: {item['observation']}")
            print(f"Recommendation: {item['recommendation']}\n")

        print(f"Recommendations saved to: {output_path}")

    except (FileNotFoundError, ValueError, KeyError) as error:
        print(f"Recommendation engine error: {error}")


if __name__ == "__main__":
    main()
