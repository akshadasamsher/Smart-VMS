from ultralytics import YOLO
import cv2
import time
import requests


# ==========================================
# YOLO MODEL
# ==========================================

model = YOLO("yolo26n.pt")


# ==========================================
# VIDEO
# ==========================================

video_path = "../frontend/public/camera01.mp4"

cap = cv2.VideoCapture(video_path)


if not cap.isOpened():

    print("ERROR: Could not open video")

    exit()


# ==========================================
# VIDEO INFORMATION
# ==========================================

fps = cap.get(cv2.CAP_PROP_FPS)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


print("Video resolution:", width, "x", height)
print("FPS:", fps)


# ==========================================
# RESTRICTED ZONE
# ==========================================

ZONE_X1 = 1100
ZONE_Y1 = 450

ZONE_X2 = 2750
ZONE_Y2 = 1850


# ==========================================
# FASTAPI URL
# ==========================================

API_URL = "http://127.0.0.1:8000/events"


# ==========================================
# CHECK POINT
# ==========================================

def inside_zone(x, y):

    return (
        ZONE_X1 <= x <= ZONE_X2
        and
        ZONE_Y1 <= y <= ZONE_Y2
    )


# ==========================================
# ALERT CONTROL
# ==========================================

last_saved_time = 0

SAVE_COOLDOWN = 5


# ==========================================
# WINDOW
# ==========================================

window_name = "Smart VMS - AI Intrusion Detection"

cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    window_name,
    1100,
    650
)


# ==========================================
# PROCESS VIDEO
# ==========================================

frame_number = 0


while True:

    ret, frame = cap.read()


    if not ret:

        break


    frame_number += 1


    # Video timestamp
    video_time = frame_number / fps


    # ======================================
    # YOLO
    # ======================================

    results = model(
        frame,
        classes=[0],
        conf=0.20,
        verbose=False
    )


    # ======================================
    # DRAW ZONE
    # ======================================

    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        3
    )


    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255),
        2
    )


    intrusion_detected = False

    detected_confidence = 0.0


    # ======================================
    # PROCESS PERSONS
    # ======================================

    for result in results:

        boxes = result.boxes


        for box in boxes:

            x1, y1, x2, y2 = box.xyxy[0].tolist()


            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)


            confidence = float(box.conf[0])


            # Person center

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )


            # ==================================
            # CHECK ZONE
            # ==================================

            person_inside = inside_zone(
                center_x,
                center_y
            )


            if person_inside:

                intrusion_detected = True

                detected_confidence = confidence

                box_color = (0, 0, 255)

            else:

                box_color = (0, 255, 0)


            # ==================================
            # DRAW PERSON
            # ==================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                box_color,
                2
            )


            # ==================================
            # CENTER POINT
            # ==================================

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                box_color,
                -1
            )


            # ==================================
            # LABEL
            # ==================================

            label = f"Person {confidence:.2f}"


            cv2.putText(
                frame,
                label,
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                box_color,
                2
            )


    # ======================================
    # INTRUSION
    # ======================================

    if intrusion_detected:

        # Display alert

        cv2.rectangle(
            frame,
            (15, 15),
            (340, 55),
            (0, 0, 255),
            -1
        )


        cv2.putText(
            frame,
            "INTRUSION DETECTED",
            (25, 43),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        # ==================================
        # SAVE EVENT
        # ==================================

        current_time = time.time()


        if current_time - last_saved_time > SAVE_COOLDOWN:

            print()
            print("================================")
            print("INTRUSION DETECTED")
            print("================================")
            print(
                f"Camera      : Camera 01"
            )
            print(
                f"Timestamp   : {video_time:.2f}"
            )
            print(
                f"Confidence  : {detected_confidence:.2f}"
            )
            print(
                "Zone        : Restricted Area"
            )


            # ==================================
            # SEND EVENT TO FASTAPI
            # ==================================

            try:

                response = requests.post(

                    API_URL,

                    params={

                        "camera_id": "Camera 01",

                        "event_type": "Intrusion",

                        "timestamp": video_time,

                        "confidence": detected_confidence,

                        "zone": "Restricted Area"

                    },

                    timeout=5

                )


                if response.status_code == 200:

                    print(
                        "Database event saved successfully!"
                    )

                else:

                    print(
                        "API error:",
                        response.status_code
                    )


            except requests.exceptions.RequestException as error:

                print(
                    "Could not connect to FastAPI:"
                )

                print(error)


            print("================================")
            print()


            last_saved_time = current_time


    else:

        # Normal status

        cv2.rectangle(
            frame,
            (15, 15),
            (180, 55),
            (0, 120, 0),
            -1
        )


        cv2.putText(
            frame,
            "SYSTEM NORMAL",
            (25, 43),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


    # ======================================
    # CAMERA INFORMATION
    # ======================================

    cv2.putText(
        frame,
        "CAMERA 01 | EAST GATE",
        (15, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    # ======================================
    # SHOW VIDEO
    # ======================================

    cv2.imshow(
        window_name,
        frame
    )


    # ======================================
    # QUIT
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()

print("Detection stopped.")