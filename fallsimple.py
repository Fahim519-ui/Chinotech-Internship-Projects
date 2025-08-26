import cv2
import math
import time
import threading
import numpy as np
import os
from ultralytics import YOLO
from datetime import datetime

# Initialize YOLOv8-pose model
model = YOLO('yolov8n-pose.pt')  # Lightweight model 

# Keypoint indices (COCO format)
NOSE = 0
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6
LEFT_HIP = 11
RIGHT_HIP = 12
LEFT_ANKLE = 15
RIGHT_ANKLE = 16

# ========== ACCURACY EVALUATION SYSTEM ==========
class FallDetectionEvaluator:
    def __init__(self):
        self.start_time = time.time()
        self.detection_history = []
        self.processing_times = []
        self.frame_count = 0
        self.processed_frames = 0
        self.fall_count = 0
        
    def record_frame(self, processed=False):
        self.frame_count += 1
        if processed:
            self.processed_frames += 1
            
    def record_detection(self, confidence, timestamp):
        detection = {
            'timestamp': timestamp,
            'confidence': confidence,
            'processing_time': self.processing_times[-1] if self.processing_times else 0
        }
        self.detection_history.append(detection)
        self.fall_count += 1
        
    def record_processing_time(self, processing_time):
        self.processing_times.append(processing_time)
        
    def calculate_metrics(self):
        total_detections = len(self.detection_history)
        
        avg_processing_time = np.mean(self.processing_times) if self.processing_times else 0
        fps = self.processed_frames / (time.time() - self.start_time) if (time.time() - self.start_time) > 0 else 0
        
        return {
            'total_detections': total_detections,
            'fall_count': self.fall_count,
            'avg_processing_time': round(avg_processing_time, 4),
            'fps': round(fps, 1),
            'evaluation_duration': round(time.time() - self.start_time, 1),
            'total_frames': self.frame_count,
            'processed_frames': self.processed_frames
        }
    
    def save_results(self, filename):
        metrics = self.calculate_metrics()
        with open(filename, 'w') as f:
            f.write("Fall Detection System Evaluation Results\n")
            f.write("=========================================\n\n")
            f.write(f"Evaluation Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Evaluation Duration: {metrics['evaluation_duration']} seconds\n")
            f.write(f"Total Frames: {metrics['total_frames']}\n")
            f.write(f"Processed Frames: {metrics['processed_frames']}\n\n")
            
            f.write("Performance Metrics:\n")
            f.write(f"Total Detections: {metrics['total_detections']}\n")
            f.write(f"Fall Count: {metrics['fall_count']}\n\n")
            
            f.write("System Performance:\n")
            f.write(f"Average Processing Time: {metrics['avg_processing_time']} seconds\n")
            f.write(f"Average FPS: {metrics['fps']}\n\n")
            
            f.write("Detection History:\n")
            for i, detection in enumerate(self.detection_history):
                f.write(f"{i+1}. Time: {detection['timestamp']:.1f}s, "
                       f"Confidence: {detection['confidence']:.2f}, "
                       f"Process Time: {detection['processing_time']:.3f}s\n")
  
# Initialize accuracy evaluator
evaluator = FallDetectionEvaluator()

    
# ========== OPTIMIZED VIDEO STREAM CLASS ==========
class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)

        # Set optimized camera parameters
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_FPS, 15)

        # Verify settings
        print(f"[INFO] Resolution: {self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)}x{self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        print(f"[INFO] FPS: {self.stream.get(cv2.CAP_PROP_FPS):.1f}")

        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


# ========== MAIN PROCESSING ==========

# Initialize optimized video stream
vs = VideoStream('rtsp://admin:Ch!no1NTvgPW@192.168.1.164:554/Streaming/Channels/101').start()
time.sleep(2.0)  # Allow camera to warm up

# Fall tracking dictionary - stores time, box, and keypoints
fall_detections = {}
DISPLAY_DURATION = 4  # seconds

# Performance monitoring and frame skipping
start_time = time.time()
frame_count = 0
last_processing_time = time.time()
processing_interval = 0.1  # Process ~10 FPS

# Fall detection parameters
FALL_ANGLE_THRESHOLD = 45  # degrees 
FALL_RATIO_THRESHOLD = 0.7  # height/width ratio
MIN_CONFIDENCE = 0.3  # Minimum keypoint confidence

print("[INFO] Starting fall detection system")
print("[INFO] Press 'q' to quit")

# Create results directory on desktop
desktop_path = os.path.join(os.path.expanduser("~"), "/home/chinotech/Desktop")
results_dir = os.path.join(desktop_path, "Fall_Detection_Results")
os.makedirs(results_dir, exist_ok=True)

# Auto-save interval (in seconds)
auto_save_interval = 60  # Save every minute
last_save_time = time.time()

while True:
    frame_start_time = time.time()
    frame = vs.read()
    if frame is None:
        break

    current_time = time.time()
    frame_count += 1
    evaluator.record_frame()

    # Skip processing if not enough time has passed
    if current_time - last_processing_time < processing_interval:
        display_frame = frame.copy()

        # Draw fall alerts from previous detections
        for person_id, data in list(fall_detections.items()):
            if current_time - data['time'] < DISPLAY_DURATION:
                box = data['box']
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(display_frame, 'FALL DETECTED!', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    else:
        last_processing_time = current_time
        evaluator.record_frame(processed=True)
        process_start_time = time.time()

        # Early downsampling for processing
        process_frame = cv2.resize(frame, (320, 320))

        # YOLOv8 Inference
        results = model(process_frame, imgsz=320, verbose=False)
        if len(results) > 0:
            results = results[0]
            keypoints = results.keypoints.xy.cpu().numpy()
            confidences = results.keypoints.conf.cpu().numpy() if results.keypoints.conf is not None else None
            boxes = results.boxes.xyxy.cpu().numpy()
        else:
            keypoints = np.array([])
            boxes = np.array([])
            confidences = None

        # Scale results back to original frame size
        scale_x = frame.shape[1] / 320
        scale_y = frame.shape[0] / 320

        # Process detections
        for i, (kpts, box) in enumerate(zip(keypoints, boxes)):
            # Scale keypoints and box to original frame size
            kpts = kpts * [scale_x, scale_y]
            scaled_box = box * [scale_x, scale_y, scale_x, scale_y]

            # Get confidences if available
            kpt_confs = confidences[i] if confidences is not None else [1.0] * len(kpts)

            # Extract keypoints with confidence check
            valid_keypoints = {}
            for idx, name in [(NOSE, 'nose'),
                              (LEFT_SHOULDER, 'left_shoulder'),
                              (RIGHT_SHOULDER, 'right_shoulder'),
                              (LEFT_HIP, 'left_hip'),
                              (RIGHT_HIP, 'right_hip'),
                              (LEFT_ANKLE, 'left_ankle'),
                              (RIGHT_ANKLE, 'right_ankle')]:
                if kpt_confs[idx] > MIN_CONFIDENCE:
                    valid_keypoints[name] = kpts[idx]

            # Only proceed if we have enough keypoints
            if len(valid_keypoints) < 4:
                continue

            # Calculate midpoints for better stability
            mid_shoulder = None
            if 'left_shoulder' in valid_keypoints and 'right_shoulder' in valid_keypoints:
                mid_shoulder = (
                    (valid_keypoints['left_shoulder'][0] + valid_keypoints['right_shoulder'][0]) / 2,
                    (valid_keypoints['left_shoulder'][1] + valid_keypoints['right_shoulder'][1]) / 2
                )
            elif 'left_shoulder' in valid_keypoints:
                mid_shoulder = valid_keypoints['left_shoulder']
            elif 'right_shoulder' in valid_keypoints:
                mid_shoulder = valid_keypoints['right_shoulder']

            mid_hip = None
            if 'left_hip' in valid_keypoints and 'right_hip' in valid_keypoints:
                mid_hip = (
                    (valid_keypoints['left_hip'][0] + valid_keypoints['right_hip'][0]) / 2,
                    (valid_keypoints['left_hip'][1] + valid_keypoints['right_hip'][1]) / 2
                )
            elif 'left_hip' in valid_keypoints:
                mid_hip = valid_keypoints['left_hip']
            elif 'right_hip' in valid_keypoints:
                mid_hip = valid_keypoints['right_hip']

            # Get lowest ankle (closest to ground)
            ankle_y = -1
            ankle_point = None
            for name in ['left_ankle', 'right_ankle']:
                if name in valid_keypoints:
                    if valid_keypoints[name][1] > ankle_y:
                        ankle_y = valid_keypoints[name][1]
                        ankle_point = valid_keypoints[name]

            # If we don't have all necessary points, skip
            if mid_shoulder is None or mid_hip is None or ankle_point is None:
                continue

            # Calculate body vector (shoulder to hip)
            body_vector = (mid_hip[0] - mid_shoulder[0], mid_hip[1] - mid_shoulder[1])

            # Calculate body angle from vertical (0 = standing, 90 = lying down)
            angle = np.degrees(np.arctan2(body_vector[0], body_vector[1]))
            abs_angle = abs(angle)

            # Calculate body height/width ratio
            body_height = abs(mid_shoulder[1] - ankle_point[1])
            body_width = abs(valid_keypoints.get('left_shoulder', [0, 0])[0] -
                             valid_keypoints.get('right_shoulder', [0, 0])[0])
            if body_width < 1:  # Avoid division by zero
                body_width = 1
            height_width_ratio = body_height / body_width

            # Calculate distance for fall detection
            shoulder_hip_dist = math.dist(mid_shoulder, mid_hip)
            shoulder_ankle_dist = abs(mid_shoulder[1] - ankle_point[1])

            # Fall detection conditions
            fall_detected = False
            detection_confidence = 0.0

            # Condition 1: Body angle is beyond threshold
            if abs_angle > FALL_ANGLE_THRESHOLD:
                fall_detected = True
                detection_confidence += 0.3

            # Condition 2: Height/width ratio indicates lying position
            if height_width_ratio < FALL_RATIO_THRESHOLD:
                fall_detected = True
                detection_confidence += 0.3


            # Condition 3: Head is lower than hips (inverted position)
            if 'nose' in valid_keypoints and valid_keypoints['nose'][1] > mid_hip[1]:
                fall_detected = True
                detection_confidence += 0.3


            # Condition 4: Ankles are above shoulders (lying position)
            if ankle_point[1] < mid_shoulder[1]:
                fall_detected = True
                detection_confidence += 0.3


            # Condition 5: Distance-based condition
            if shoulder_ankle_dist < shoulder_hip_dist * 1.5:
                fall_detected = True
                detection_confidence += 0.3


            # If any condition is met, register fall
            if fall_detected:
                person_id = tuple(scaled_box.astype(int))
                fall_detections[person_id] = {
                    'time': current_time,
                    'box': scaled_box
                }

                # Record detection for accuracy tracking
                evaluator.record_detection(detection_confidence, current_time)

                # Print detection info for debugging
                print("Fall detected!")

        # Record processing time
        processing_time = time.time() - process_start_time
        evaluator.record_processing_time(processing_time)

        # Update display frame
        display_frame = frame.copy()

        # Draw all detections
        for kpts, box in zip(keypoints, boxes):
            scaled_box = box * [scale_x, scale_y, scale_x, scale_y]
            x1, y1, x2, y2 = map(int, scaled_box)

            # Check if this is a fall detection
            person_id = tuple(scaled_box.astype(int))
            is_fall = person_id in fall_detections and current_time - fall_detections[person_id]['time'] < DISPLAY_DURATION

            # Draw bounding box (red for fall, green for normal)
            color = (0, 0, 255) if is_fall else (0, 255, 0)
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)

            # Draw fall alert text
            if is_fall:
                cv2.putText(display_frame, 'FALL DETECTED!', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Calculate and display FPS
    elapsed = current_time - start_time
    fps = frame_count / elapsed
    cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Show output
    cv2.imshow('Fall Detection System', display_frame)
    
    # Auto-save results periodically
    if current_time - last_save_time >= auto_save_interval:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = os.path.join(results_dir, f"fall_detection_results_{timestamp}.txt")
        evaluator.save_results(results_filename)
        print(f"Auto-saved results to {results_filename}")
        last_save_time = current_time
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):  # Pause on spacebar
        while cv2.waitKey(1) & 0xFF != ord(' '):
            pass

# Cleanup
vs.stop()
cv2.destroyAllWindows()

# Save final results and display summary
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_filename = os.path.join(results_dir, f"final_results_{timestamp}.txt")
evaluator.save_results(results_filename)

final_metrics = evaluator.calculate_metrics()
print("\n" + "="*50)
print("FALL DETECTION SYSTEM - FINAL RESULTS")
print("="*50)
print(f"Evaluation Duration: {final_metrics['evaluation_duration']} seconds")
print(f"Total Frames: {final_metrics['total_frames']}")
print(f"Processed Frames: {final_metrics['processed_frames']}")
print(f"Total Detections: {final_metrics['total_detections']}")
print(f"Fall Count: {final_metrics['fall_count']}")
print(f"Average Processing Time: {final_metrics['avg_processing_time']:.4f} seconds")
print(f"Average FPS: {final_metrics['fps']:.1f}")
print(f"Results saved to: {results_filename}")
print("="*50)
