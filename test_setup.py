
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import librosa
import soundfile as sf

print("All core libraries imported successfully!")

# Test a basic OpenCV operation
image = np.zeros((200, 200, 3), dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("OpenCV image conversion:", gray.shape)
print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("MediaPipe:", mp.__version__)
print("Librosa:", librosa.__version__)
print("SoundFile:", sf.__version__)
print("Setup test completed.")
