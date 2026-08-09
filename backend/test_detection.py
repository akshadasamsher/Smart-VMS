from ultralytics import YOLO
import cv2

model = YOLO("yolo26n.pt")

video_path = "../frontend/public/camera01.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: Could not open video")
    exit()

for frame_number in range(50):

    ret, frame = cap.read()

    if not ret:
        break

    results = model(
        frame,
        classes=[0],
        conf=0.20,
        verbose=False
    )

    boxes = results[0].boxes

    print(
        f"Frame {frame_number + 1}: "
        f"{len(boxes)} person(s) detected"
    )

cap.release()

print("Test completed")