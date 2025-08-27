Fall Detection System Documentation:

Overview:
This system is a real-time fall detection solution that uses YOLOv8 pose estimation to monitor human poses and detect potential fall events. It processes video streams (including RTSP cameras) and provides visual alerts when falls are detected, while also logging performance metrics and detection history.

System Architecture:

1. Core Components

Pose Estimation: Uses YOLOv8n-pose model for human keypoint detection
Video Streaming: Handles RTSP streams with optimized parameters
Fall Detection Logic: Analyzes body angles and proportions to identify falls
Evaluation System: Tracks performance metrics and detection history
Visualization: Displays real-time feedback with bounding boxes and alerts

2. Keypoint Definitions (COCO Format)

The system uses these specific keypoints for pose analysis:

NOSE (0)
LEFT_SHOULDER (5)
RIGHT_SHOULDER (6)
LEFT_HIP (11)
RIGHT_HIP (12)
LEFT_ANKLE (15)
RIGHT_ANKLE (16)

Installation and Setup:

Setup Virtual Environment on Raspberry Pi 5 
cd /home/chinotech/hailo-rpi5-examples
./install.sh
source setup_env.sh

Install required dependencies:
 pip install opencv-python numpy ultralytics
      
Download Yolov8 pose model
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-pose.pt




Setup and connect the camera 
Update the RTSP stream URL in the main processing section:
vs = VideoStream('rtsp://username:password@ip:port/stream_path').start()
Run main script
Python fallsimple.py


Output:
Real-time video display with bounding boxes and fall alerts
Automatic saving of performance results and accuracy metrics  to ~/Desktop/Fall_Detection_Results

Algorithm Details:

Fall Detection Logic:

The system uses a multi-condition approach to detect falls:

Body Angle Calculation: Measures the angle between shoulder and hip points relative to vertical
Height/Width Ratio: Calculates the proportion of body height to width
Head Position: Checks if head is below hips
Ankle Position: Checks if ankles are above shoulders (lying position)
Distance Comparison: Compares shoulder-ankle distance to shoulder-hip distance

Note: The midpoints of shoulder and hips are calculated and used for all calculations. Calculation for the midpoint of ankle is avoided since the ankle point captures instability.

A fall is detected when any one of these conditions is met, with confidence scores accumulated based on how many conditions are triggered.

Fall Thresholds:

These are minimum conditions beyond which the movements are classified as a fall. This can be further tailored to meet specific client needs.
 
FALL_ANGLE_THRESHOLD = 45  # angle b/w mid shoulder and mid hip points 
FALL_RATIO_THRESHOLD = 0.7  # height/width ratio
MIN_CONFIDENCE = 0.3  # Minimum keypoint confidence








Accuracy Detection:

The system generates text files with the following information:

Evaluation timestamp and duration
Frame processing statistics
Detection counts and confidence values
System performance metrics (FPS, processing time)

Performance Settings:

# How long fall alerts remain visible
DISPLAY_DURATION = 4

# How often to process frames (seconds)
processing_interval = 0.1


Performance Optimization:

Used a smaller YOLO model (yolov8n-pose.pt) for faster inference
Adjusted frame processing interval based on hardware capabilities
Reduced output video resolution if display is not needed

Limitations:

Require clear view of person for keypoint detection
Performance depends on hardware capabilities 

Potential Enhancements:

Alert System: Integrate email/SMS notifications for detected falls
Cloud Storage: Upload results to cloud services for remote monitoring
Multiple Camera Support: Extend to handle multiple video streams
Historical Analysis: Add database storage for long-term trend analysis
Web Interface: Create a dashboard for remote monitoring

