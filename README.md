# Multimodal Attendance & Engagement Agent

A Python-based prototype that combines visual presence estimation, audio feature analysis, session-level summaries, and a Streamlit dashboard.

## Project Overview

The Multimodal Attendance & Engagement Agent explores how video-derived presence signals and audio activity features can be analyzed together to produce an experimental session summary.

The project is designed as an educational prototype. Its outputs are estimates, not verified measures of attendance, attention, or engagement.

## Features

- **Face Detection:** Detects faces in a video stream using OpenCV Haar Cascade.
- **Presence Estimation:** Estimates the time a face is detected during a session.
- **Audio Feature Extraction:** Calculates audio duration, RMS energy, zero-crossing rate, and spectral centroid.
- **Audio Activity Analysis:** Uses an RMS energy threshold to identify possible audio activity.
- **Multimodal Summary:** Combines available visual and audio summaries into an experimental session-level index.
- **Recommendations:** Generates suggestions and limitations based on the available results.
- **Dashboard:** Displays session metrics and recommendations through Streamlit.

## Technology Stack

- Python
- OpenCV
- NumPy and pandas
- librosa and SoundFile
- Streamlit

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies.
4. Run the relevant application module.

Example commands for Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Running the Project

Launch the dashboard:

```powershell
streamlit run app/dashboard.py
```

Run face detection:

```powershell
python app/face_detection.py
```

Run the analysis modules:

```powershell
python app/audio_features.py sample_audio.wav
python app/audio_activity.py sample_audio.wav
python app/multimodal_agent.py
python app/recommendations.py
python app/session_analytics.py
```

The audio commands require an appropriate local audio file. Generated results are written to the `results/` directory.

## Limitations

- Face detection can produce false positives or miss faces depending on camera quality, lighting, distance, and background.
- Audio energy is not verified speech detection and cannot establish who is speaking.
- The visual and audio samples may cover different time periods and may not be synchronized.
- The experimental fusion index is not a scientifically validated engagement score.
- The system does not verify a person's identity.

## Responsible Use

Use recordings only with appropriate consent and a clear explanation of the system's purpose. Protect personal recordings and session data. Do not use experimental scores to grade, rank, or make consequential decisions about students.

## Project Status

Educational prototype under development. Testing, documentation, and demonstration materials are being prepared.
