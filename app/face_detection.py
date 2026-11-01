import argparse
import cv2
from pathlib import Path


def detect_faces(source):
    cascade_path = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "haarcascade_frontalface_default.xml"
)
    detector = cv2.CascadeClassifier(str(cascade_path))

    if detector.empty():
        raise RuntimeError("Could not load the face detector.")

    # Source 0 means the default webcam.
    # A string path means a prerecorded video.
    source = int(source) if source.isdigit() else source
    capture = cv2.VideoCapture(source)

    if not capture.isOpened():
        raise RuntimeError(
            f"Could not open video source: {source}"
        )

    try:
        while True:
            success, frame = capture.read()

            if not success:
                break

            gray = cv2.cvtColor(
                frame, cv2.COLOR_BGR2GRAY
            )

            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=6,
                minSize=(30, 30),
            )

            for x, y, width, height in faces:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2,
                )

            cv2.putText(
                frame,
                f"Faces detected: {len(faces)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Face Detection - Press Q to quit", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        capture.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index or path to a video file",
    )
    args = parser.parse_args()

    try:
        detect_faces(args.source)
    except (RuntimeError, cv2.error) as error:
        print(f"Error: Face detection could not start or continue. {error}")

