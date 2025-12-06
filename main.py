import cv2
import numpy as np
import time
from ultralytics import YOLO  # YOLOv8 module

# Function to estimate distance based on bounding box width
def estimate_distance(bbox_width, bbox_height):
    focal_length = 1000  # Adjust based on camera setup
    known_width = 2.0  # Approximate width of a car in meters
    distance = (known_width * focal_length) / bbox_width
    return distance

def process_video():
    model = YOLO('weights/yolov8n.pt')
    cap = cv2.VideoCapture('video/video.mp4')

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    target_fps = 30
    frame_time = 1.0 / target_fps
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (1280, 720))

        # Run YOLOv8 to detect cars
        results = model(resized_frame)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])

                if model.names[cls] == 'car' and conf >= 0.5:
                    bbox_width = x2 - x1
                    bbox_height = y2 - y1
                    distance = estimate_distance(bbox_width, bbox_height)

                    # Determine color based on distance
                    if distance < 10:
                        color = (0, 0, 255)  # Red for high alert
                    elif 10 <= distance <= 30:
                        color = (0, 255, 255)  # Yellow for caution
                    else:
                        color = (0, 255, 0)  # Green for safe

                    # Draw car bounding box
                    label = f'{model.names[cls]} {conf:.2f}'
                    cv2.rectangle(resized_frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(resized_frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    # Distance display
                    distance_label = f'{distance:.2f}m'
                    cv2.putText(resized_frame, distance_label, (x1, y2 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        cv2.imshow('Car Distance', resized_frame)
        time.sleep(frame_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

process_video()
