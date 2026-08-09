from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo26n.pt")

print("YOLO model loaded successfully")

# Run detection on CCTV video
results = model.predict(
    source="../frontend/public/camera01.mp4",
    save=True,
    conf=0.5
)

print("Detection completed")