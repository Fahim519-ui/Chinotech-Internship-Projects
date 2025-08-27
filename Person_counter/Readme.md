Person Counter with YOLO and SORT Tracking
A Raspberry Pi-optimized person counting system that uses YOLOv8 for detection and SORT (Simple Online and Realtime Tracking) for tracking people across video frames. The system counts people crossing two predefined lines in a video.

Features
* Real-time person detection using YOLOv8 Nano (optimized for Raspberry Pi)
* Object tracking using SORT algorithm
* Dual-line crossing detection
* Performance optimizations for resource-constrained devices
* Video output with visualization of detections and counts

Requirements
* Raspberry Pi (tested on Pi 4)
* Python 3.7+
* OpenCV
* Ultralytics YOLOv8
* NumPy
* SORT tracking algorithm

Installation
1. Clone the repository and install dependencies:
pip install opencv-python numpy ultralytics
2. Download the YOLOv8 Nano model:
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
3. Install the SORT tracker:
cd ~
git clone https://github.com/abewley/sort.git

Usage
1. Place your input video file in the correct directory (default: ~/Desktop/Chinotech_Internship/crowded pedestrian street.mov)
2. Run the script:python person_counter.py
3. Press 'q' to quit the application

Configuration
Key parameters you can adjust:
* max_age: Maximum frames to keep a track alive without detection (default: 20)
* min_hits: Minimum detections before a track is initialized (default: 3)
* iou_threshold: Intersection over Union threshold for tracking (default: 0.3)
* conf: Confidence threshold for person detection (default: 0.3)
* limitsUp, limitsDown: Coordinates for the counting lines

Output
The script generates:
* An output video with bounding boxes, IDs, and counting information
* Console output with total counts for both directions
* Real-time FPS counter to monitor performance

Performance Notes:
This implementation includes several Raspberry Pi optimizations:
* Reduced frame processing (every 3rd frame)
* Lower resolution for processing (640x360)
* Environment variables to limit thread usage
* Simplified drawing operations

Results:
The script will display and output:
* Number of people crossing the "Up" line
* Number of people crossing the "Down" line
* Total counts for both directions
