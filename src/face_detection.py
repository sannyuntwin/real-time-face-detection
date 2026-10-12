import cv2
import os

# 1. Load the pre-trained Haar Cascade face detection model
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(model_path)

if face_cascade.empty():
    raise FileNotFoundError(f"Failed to load Haar Cascade model from: {model_path}")

# 2. Open a connection to your default webcam (0 is usually the built-in webcam)
video_capture = cv2.VideoCapture(0)

print("Press 'q' to quit the application.")

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # 3. Convert the frame to grayscale (Haar Cascades require grayscale images)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 4. Detect faces in the grayscale frame
    # scaleFactor: Compensates for faces looking bigger/smaller due to distance
    # minNeighbors: How many cascade rectangles need to overlap to confirm a face
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 5. Draw a bounding box around every detected face
    for (x, y, w, h) in faces:
        # cv2.rectangle(image, top_left_corner, bottom_right_corner, color_in_BGR, thickness)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 6. Display the resulting frame in a window named 'Face Detection'
    cv2.imshow('Face Detection', frame)

    # 7. Break the loop immediately if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 8. Release the camera resource and close all open windows
video_capture.release()
cv2.destroyAllWindows()
