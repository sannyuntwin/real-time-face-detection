# Real-Time Face Detection & Attendance System

Two tools in one repo:

| Script | What it does |
|--------|-------------|
| `src/face_detection.py` | Basic webcam face detection with Haar Cascade |
| `src/attendance_system.py` | Smart attendance logger using face recognition + SQLite |

---

## Setup on Ubuntu (WSL2 or native)

### 1. Install system dependencies

```bash
sudo apt update
sudo apt install -y python3-pip cmake python3-dev libopenblas-dev ffmpeg v4l-utils
```

### 2. Clone the repo

```bash
git clone https://github.com/sannyuntwin/real-time-face-detection.git
cd real-time-face-detection
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python packages

```bash
pip install -r requirements.txt
```

> `dlib` compiles from source — takes 5–10 minutes. This is normal.

### 5. Add your face image

Drop a photo into the `faces/` folder named after the person:

```bash
cp ~/Downloads/your_photo.jpg faces/your_name.jpg
```

If your photo is on Windows (WSL users):
```bash
cp /mnt/c/Users/YourName/Pictures/photo.jpg faces/your_name.jpg
```

The filename becomes the display name — `john_doe.jpg` → **"John Doe"**.

---

## WSL2 webcam setup (Windows only)

WSL2 doesn't have webcam access by default. Follow these steps once.

### On Windows PowerShell (as Administrator)

Install usbipd:
```powershell
winget install --interactive --exact dorssel.usbipd-win
```

List USB devices and find your webcam:
```powershell
usbipd list
```

Share and attach the webcam to WSL (replace `1-4` with your webcam's BUSID):
```powershell
usbipd bind --busid 1-4
usbipd attach --wsl --busid 1-4
```

> You need to run `usbipd attach` every time you restart WSL.

### Add your user to the video group (Ubuntu, one-time)

```bash
sudo usermod -aG video $USER
newgrp video
```

---

## Running

### Attendance system

```bash
source venv/bin/activate
export DISPLAY=:0
python3 src/attendance_system.py
```

- **Green box** = recognized person (logged to DB)
- **Red box** = unknown face
- Press **q** to quit

### Basic face detection

```bash
source venv/bin/activate
export DISPLAY=:0
python3 src/face_detection.py
```

---

## View attendance logs

```bash
python3 -c "import sqlite3; [print(r) for r in sqlite3.connect('data/attendance.db').execute('SELECT * FROM logs ORDER BY date, time')]"
```

---

## Project structure

```
real-time-face-detection/
├── faces/               # Drop registered face images here (gitignored)
├── data/                # SQLite DB auto-created here at runtime (gitignored)
├── models/
│   └── haarcascade_frontalface_default.xml
├── src/
│   ├── face_detection.py
│   └── attendance_system.py
└── requirements.txt
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'face_recognition'` | `pip install face_recognition` inside the venv |
| `can't open camera by index` | Run `usbipd attach --wsl --busid <id>` on Windows |
| `could not connect to display` | `export DISPLAY=:0` |
| `select() timeout` | Close Windows apps using the camera; reattach with usbipd |
