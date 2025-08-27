LED Panel Analyzer:

This project is a Python-based tool for analyzing LED panels by comparing the brightness and color of individual LEDs in an image. It uses OpenCV to process images and allows users to interactively select LEDs for comparison.

Overview:

1. The LED Panel Analyzer helps technicians and engineers:
2. Compare the brightness of different LEDs on a panel
3. Analyze color differences between LEDs
4. Determine which LEDs are functioning properly (ON) and which might be faulty (OFF)

Key Functions:
The script performs the following operations:
1. Image Loading: Reads an image file named "panel.jpeg"
2. Image Resizing: Resizes the image to 800x600 pixels for consistent display
3. Color Space Conversion: Converts the image from BGR to HSV color space for better brightness analysis
4. Interactive Selection: Allows users to click on two different LEDs in the image
5. Analysis: Compares the RGB values and brightness (Value channel in HSV) of the selected LEDs
6. Status Determination: Determines which LED is ON and which is OFF based on brightness comparison

Comparison Logic:
1. When two clicks are registered, it compares the two LEDs
2. Calculates the absolute difference in RGB values
3. Determines which LED is ON based on which has higher brightness

Usage:
1.Place an image of your LED panel in the same directory as the script, named "panel.jpeg"
2. Run the script: python leddetector.py
3. Click on two different LEDs in the displayed image
4. View the comparison results in the console output

Sample Output:
Clicked at (150, 200) → RGB: (255, 200, 50), Brightness (V): 220
Clicked at (300, 250) → RGB: (100, 150, 80), Brightness (V): 120
--- LED RGB & Brightness Comparison ---
LED 1 @ (150, 200) → RGB: (255, 200, 50), V = 220
LED 2 @ (300, 250) → RGB: (100, 150, 80), V = 120
RGB Difference: (155, 50, 30)
LED 1 is ON
LED 2 is OFF

Requirements:
1. Python 3.x
2. OpenCV (pip install opencv-python)
3. NumPy (pip install numpy)

Applications:
1. Quality control in LED manufacturing
2. Troubleshooting LED panel issues
3. Educational purposes for understanding color spaces and image processing

Limitations:
1. Relies on an accurate image representation of the LED panel
2. Brightness comparison is relative between two LEDs rather than absolute
3. Does not account for ambient lighting conditions that might affect the image

Future Enhancements:
1. Implement absolute brightness thresholds
2. Support for analyzing more than two LEDs at once
3. Batch Processing for multiple images
