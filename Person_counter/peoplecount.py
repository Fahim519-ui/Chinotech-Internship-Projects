import os
import numpy as np
import cv2
from ultralytics import YOLO
import math
import sys
import time

# Raspberry Pi optimizations
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
sys.path.append(os.path.expanduser('~/person_counter/sort'))
from sort import Sort

# Create output directory
output_dir = os.path.expanduser('~/Desktop/Chinotech_Internship')
os.makedirs(output_dir, exist_ok=True)

# Video input
cap = cv2.VideoCapture(os.path.join(output_dir, 'crowded pedestrian street.mov'))

# Use nano model for Raspberry Pi
model = YOLO(os.path.expanduser('~/person_counter/yolov8n.pt'))

# Only detect persons
classNames = ["person"]

# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# Counting lines
limitsUp = [103, 161, 296, 161]
limitsDown = [527, 489, 735, 489]

totalCountUp = []
totalCountDown = []

# Output video
output_path = os.path.join(output_dir, 'output.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 15  # Reduced FPS for Pi
out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

frame_count = 0
start_time = time.time()

while True:
    success, img = cap.read()
    if not success:
        break
    
    frame_count += 1
    
    # Process only every 3rd frame to reduce load
    if frame_count % 3 != 0:
        out.write(img)
        continue
        
    # Reduce resolution for processing
    img_small = cv2.resize(img, (640, 360))
    results = model(img_small, stream=True, verbose=False)  # Disable logs

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            
            # Scale coordinates back to original size
            scale_x = img.shape[1] / 640
            scale_y = img.shape[0] / 360
            x1, y1, x2, y2 = int(x1*scale_x), int(y1*scale_y), int(x2*scale_x), int(y2*scale_y)
            
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            currentClass = classNames[0]  # Only person class

            if conf > 0.3:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultsTracker = tracker.update(detections)

    # Draw counting lines
    cv2.line(img, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 0, 255), 3)
    cv2.line(img, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 0, 255), 3)

    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        
        # Simple rectangle instead of cornerRect to save resources
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.putText(img, f'{int(id)}', (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

        cx, cy = x1 + w // 2, y1 + h // 2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Line crossing detection
        if limitsUp[0] < cx < limitsUp[2] and abs(cy - limitsUp[1]) < 20:
            if id not in totalCountUp:
                totalCountUp.append(id)
                cv2.line(img, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 255, 0), 3)

        if limitsDown[0] < cx < limitsDown[2] and abs(cy - limitsDown[1]) < 20:
            if id not in totalCountDown:
                totalCountDown.append(id)
                cv2.line(img, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 255, 0), 3)
    
    # Display counters
    cv2.putText(img, f'Up: {len(totalCountUp)}', (50, 50), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f'Down: {len(totalCountDown)}', (50, 100), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Display processing info
    fps = frame_count / (time.time() - start_time)
    cv2.putText(img, f'FPS: {fps:.1f}', (50, img.shape[0]-50), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    out.write(img)
    cv2.imshow("Person Counter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Total counted Up: {len(totalCountUp)}")
print(f"Total counted Down: {len(totalCountDown)}")
