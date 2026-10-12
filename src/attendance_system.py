import sys
import types

# face_recognition_models uses pkg_resources which is absent in Python 3.12 venvs
if 'pkg_resources' not in sys.modules:
    from importlib.resources import files as _pkg_files
    _pr = types.ModuleType('pkg_resources')
    _pr.resource_filename = lambda pkg, path: str(_pkg_files(pkg).joinpath(path))
    sys.modules['pkg_resources'] = _pr

import cv2
import face_recognition
import numpy as np
import os
import sqlite3
from datetime import datetime

# --- STEP 1: INITIALIZE DATABASE ---
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/attendance.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

with sqlite3.connect(DB_PATH) as _setup_conn:
    _setup_conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            UNIQUE(name, date)
        )
    ''')

# In-memory set of names already logged today — avoids per-frame DB writes
_logged_today: set = set()

def log_attendance(name):
    """Logs attendance once per person per day. Skips if already logged this session."""
    if name in _logged_today:
        return
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    try:
        with sqlite3.connect(DB_PATH) as db_conn:
            db_conn.execute(
                "INSERT INTO logs (name, date, time) VALUES (?, ?, ?)",
                (name, current_date, current_time)
            )
        _logged_today.add(name)
        print(f"Attendance logged for {name} at {current_time}")
    except sqlite3.IntegrityError:
        # Already in DB from a prior session today
        _logged_today.add(name)

# --- STEP 2: LOAD KNOWN FACES ---
FACES_DIR = os.path.join(os.path.dirname(__file__), '../faces')
known_face_encodings = []
known_face_names = []

if os.path.exists(FACES_DIR):
    for filename in os.listdir(FACES_DIR):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            path = os.path.join(FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            # Get the mathematical "fingerprint" of the face
            encodings = face_recognition.face_encodings(image)
            
            if encodings:
                known_face_encodings.append(encodings[0])
                # Use filename without extension as the person's name (e.g., "john_doe")
                name = os.path.splitext(filename)[0].replace('_', ' ').title()
                known_face_names.append(name)

print(f"Loaded {len(known_face_names)} registered faces.")

# --- STEP 3: REAL-TIME SCANNING ---
video_capture = cv2.VideoCapture(0)
frame_count = 0
# Cache last detection results so the display stays smooth between processed frames
last_face_locations = []
last_face_names = []

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame_count += 1

    # Run face recognition every 3 frames to keep the UI responsive
    if frame_count % 3 == 0:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        last_face_locations = face_locations
        last_face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            if True in matches:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    log_attendance(name)
            last_face_names.append(name)

    for (top, right, bottom, left), name in zip(last_face_locations, last_face_names):
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow('Smart Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
