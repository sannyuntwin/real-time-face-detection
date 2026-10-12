# Real-Time Face Detection & Attendance System

Two tools in one repo:

| Script | What it does |
|--------|-------------|
| `src/face_detection.py` | Basic webcam face detection with Haar Cascade |
| `src/attendance_system.py` | Smart attendance logger using face recognition + SQLite |

## Requirements

- Python 3.7+
- A webcam
- On Windows/Mac, `cmake` and `dlib` must be installed before `face_recognition` (`pip install cmake dlib`)

```bash
pip install -r requirements.txt
```

## Face Detection (basic)

```bash
python src/face_detection.py
```

Draws green rectangles around detected faces. Press **q** to quit.

## Attendance System

### 1. Register faces

Add one photo per person to the `faces/` folder. Name each file after the person:

```
faces/
  john_doe.jpg
  jane_smith.png
```

The filename (without extension) becomes the display name — underscores are converted to spaces and title-cased.

### 2. Run

```bash
python src/attendance_system.py
```

- **Green box** = recognized person (logged to DB)
- **Red box** = unknown face

Attendance records are saved to `data/attendance.db`. Press **q** to quit.

### Viewing logs

```bash
sqlite3 data/attendance.db "SELECT * FROM logs ORDER BY date, time;"
```

## Project structure

```
real-time-face-detection/
├── faces/               # Drop registered face images here
├── data/                # SQLite DB auto-created here at runtime
├── models/
│   └── haarcascade_frontalface_default.xml
├── src/
│   ├── face_detection.py
│   └── attendance_system.py
└── requirements.txt
```
