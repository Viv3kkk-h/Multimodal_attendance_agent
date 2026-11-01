
from pathlib import Path

import pandas as pd
import streamlit as st

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

st.set_page_config(
    page_title="Multimodal Attendance Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Multimodal Attendance & Engagement Agent")
st.caption(
    "Experimental prototype | Visual presence and audio activity analytics"
)

st.warning(
    "This dashboard displays estimated visual presence and possible audio "
    "activity. These are indirect signals, not proof of attention, identity, "
    "speech, or engagement. Current recordings may not be synchronized."
)


def load_latest_csv(filename):
    """Load a results CSV safely, returning None if unavailable."""
    path = RESULTS_DIR / filename

    if not path.exists():
        st.warning(f"Results file not found: results/{filename}")
        return None

    try:
        data = pd.read_csv(path)
        if data.empty:
            st.warning(f"The file results/{filename} contains no records.")
            return None
        return data
    except (
        OSError,
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
        UnicodeDecodeError,
    ) as error:
        st.error(f"Could not read {filename}: {error}")
        return None


summary = load_latest_csv("multimodal_session_summary.csv")
audio_features = load_latest_csv("audio_features.csv")
recommendations = load_latest_csv("recommendations.csv")

if summary is not None:
    row = summary.iloc[-1]

    st.subheader("Session overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Estimated visual presence",
            f"{row['estimated_presence_percent']:.2f}%",
        )

    with col2:
        st.metric(
            "Possible audio activity",
            f"{row['possible_audio_activity_percent']:.2f}%",
        )

    with col3:
        st.metric(
            "Experimental fusion index",
            f"{row['experimental_fusion_index_percent']:.2f}%",
        )

    st.caption(
        "The fusion index is an exploratory arithmetic average, not a "
        "validated engagement score."
    )

    st.subheader("Visual presence")
    visual_values = {
        "Session duration (seconds)": row["visual_session_duration_seconds"],
        "Observed presence (seconds)": row["observed_presence_seconds"],
        "Estimated presence (%)": row["estimated_presence_percent"],
    }
    st.dataframe(
        pd.DataFrame(
            {"Metric": visual_values.keys(), "Value": visual_values.values()}
        ),
        hide_index=True,
        width="stretch",
    )

    st.subheader("Multimodal analysis")
    st.write(
        "**Signal-level category:**",
        row.get("experimental_signal_level", "Not available"),
    )
    st.write(
        "**Synchronization:**",
        row.get("synchronization_status", "Not available"),
    )
    st.write(
        "**Duration difference (seconds):**",
        row.get("duration_difference_seconds", "Not available"),
    )

if audio_features is not None:
    st.subheader("Audio features")
    st.dataframe(audio_features, hide_index=True, width="stretch")

if recommendations is not None:
    st.subheader("Recommendations")
    st.dataframe(
        recommendations,
        hide_index=True,
        width="stretch",
    )

report_path = RESULTS_DIR / "session_analytics_report.txt"

st.subheader("Individual session report")

if report_path.exists():
    try:
        report_text = report_path.read_text(encoding="utf-8")
        with st.expander("View full analytics report"):
            st.text(report_text)
    except OSError as error:
        st.error(f"Could not read the report: {error}")
else:
    st.info("The session analytics report has not been generated yet.")

st.divider()
st.caption(
    "Responsible use: obtain appropriate consent, protect recordings, "
    "and do not use experimental metrics alone to judge people."
)
