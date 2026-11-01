
import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

import cv2


# A short detection gap is tolerated.
GRACE_PERIOD_SECONDS = 2.0

# Use the face detector downloaded for Activity 2.1.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CASCADE_PATH = (
    PROJECT_ROOT
    / "models"
    / "haarcascade_frontalface_default.xml"
)


def run_attendance(source="0"):
    detector = cv2.CascadeClassifier(str(CASCADE_PATH))

    if detector.empty():
        raise RuntimeError(
            f"Could not load face detector: {CASCADE_PATH}"
        )

    video_source = int(source) if source.isdigit() else source
    capture = cv2.VideoCapture(video_source)

    if not capture.isOpened():
        raise RuntimeError(
            f"Could not open video source: {video_source}"
        )

    session_start = time.monotonic()
    last_seen = None
    confirmed_presence = 0.0
    face_detected = False

    print("Attendance session started. Press Q to finish.")

    previous_frame_time = None
    
    try:
        while True:
            success, frame = capture.read()

            if not success:
                break

            now = time.monotonic()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=6,
                minSize=(30, 30),
            )

            # This first version assumes one participant.
            # Multiple detected boxes are treated as visual presence,
            # not as proof of multiple people or verified identity.
            face_detected = len(faces) > 0

            for x, y, width, height in faces:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2,
                )

            
            
            # Count only intervals where the face is detected.
            # The grace period prevents status flickering but does
            # not add missing time to confirmed presence.

            if previous_frame_time is None:
                frame_interval = 0.0
            else:
                frame_interval = min(
                    now - previous_frame_time, 0.25
                )

            previous_frame_time = now

            if face_detected:
                confirmed_presence += frame_interval
                last_seen = now
                status = "Face present"
                status_color = (0, 255, 0)

            elif (
                last_seen is not None
                and now - last_seen <= GRACE_PERIOD_SECONDS
            ):
                status = "Temporarily not detected"
                status_color = (0, 165, 255)

            else:
                last_seen = None
                status = "Face not detected"
                status_color = (0, 0, 255)


                status = "Face not detected"
                status_color = (0, 0, 255)

            elapsed = now - session_start
            attendance_percent = (
                min(100.0, confirmed_presence / elapsed * 100)
                if elapsed > 0
                else 0.0
            )

            cv2.putText(
                frame,
                f"Status: {status}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                status_color,
                2,
            )

            cv2.putText(
                frame,
                f"Observed presence: {confirmed_presence:.1f}s",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Session elapsed: {elapsed:.1f}s",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Estimated presence: {attendance_percent:.1f}%",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 0),
                2,
            )

            cv2.imshow("Attendance - Press Q to finish", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        capture.release()
        cv2.destroyAllWindows()

    session_duration = time.monotonic() - session_start
    attendance_percent = (
        min(100.0, confirmed_presence / session_duration * 100)
        if session_duration > 0
        else 0.0
    )

    # Save a session summary for project evidence.
    output_dir = PROJECT_ROOT / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "attendance_summary.csv"

    file_exists = output_file.exists()

    with output_file.open(
        "a", newline="", encoding="utf-8"
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "session_end",
                "session_duration_seconds",
                "observed_presence_seconds",
                "estimated_presence_percent",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "session_end": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "session_duration_seconds": round(
                    session_duration, 2
                ),
                "observed_presence_seconds": round(
                    confirmed_presence, 2
                ),
                "estimated_presence_percent": round(
                    attendance_percent, 2
                ),
            }
        )

    print("\nSession finished.")
    print(f"Session duration: {session_duration:.1f} seconds")
    print(f"Observed presence: {confirmed_presence:.1f} seconds")
    print(f"Estimated presence: {attendance_percent:.1f}%")
    print(f"Summary saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index or prerecorded video path",
    )
    args = parser.parse_args()

    run_attendance(args.source)
