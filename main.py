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

    # Variables for text animation
    text_alpha = 0
    text_target_alpha = 0
    text_fade_speed = 0.1
    warning_text = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (1280, 720))

        # Run YOLOv8 to detect cars
        results = model(resized_frame)

        red_alert_triggered = False
        car_detected = False

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])

                if model.names[cls] == 'car' and conf >= 0.5:
                    car_detected = True
                    bbox_width = x2 - x1
                    bbox_height = y2 - y1
                    distance = estimate_distance(bbox_width, bbox_height)

                    # Determine color based on distance
                    if distance < 10:
                        color = (0, 0, 255)  # Red for high alert
                        red_alert_triggered = True
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
        
        # Update text and alpha target based on detection
        if red_alert_triggered:
            warning_text = "⚠ Warning"
            text_target_alpha = 1
            text_color = (0, 0, 255)
            bg_color = (0, 0, 100)
        elif not car_detected:
            warning_text = "Free road"
            text_target_alpha = 1
            text_color = (0, 255, 0)
            bg_color = (0, 100, 0)
        else:
            text_target_alpha = 0

        # Animate alpha
        if text_alpha < text_target_alpha:
            text_alpha = min(text_alpha + text_fade_speed, text_target_alpha)
        elif text_alpha > text_target_alpha:
            text_alpha = max(text_alpha - text_fade_speed, text_target_alpha)

        if text_alpha > 0:
            overlay = resized_frame.copy()
            font_scale = 2
            font = cv2.FONT_HERSHEY_TRIPLEX
            try:
                text_size, _ = cv2.getTextSize(warning_text, font, font_scale, 3)
            except UnicodeEncodeError:
                warning_text = "Warning"
                text_size, _ = cv2.getTextSize(warning_text, font, font_scale, 3)

            text_x = (resized_frame.shape[1] - text_size[0]) // 2
            text_y = 100

            # Draw semi-transparent background
            bg_x1, bg_y1 = text_x - 20, text_y - text_size[1] - 20
            bg_x2, bg_y2 = text_x + text_size[0] + 20, text_y + 20
            cv2.rectangle(overlay, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, -1)

            # Add blended overlay to the frame
            cv2.addWeighted(overlay, text_alpha, resized_frame, 1 - text_alpha, 0, resized_frame)
            
            # Draw text
            cv2.putText(resized_frame, warning_text, (text_x, text_y),
                        font, font_scale, 
                        (int(text_color[0]), 
                         int(text_color[1]), 
                         int(text_color[2])), 3)

        cv2.imshow('Car Distance', resized_frame)
        time.sleep(frame_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

process_video()
