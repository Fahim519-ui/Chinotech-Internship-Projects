LED Panel Analyzer:

This project is a Python-based tool for analyzing LED panels by comparing the brightness and color of individual LEDs in an image. It uses OpenCV to process images and allows users to interactively select LEDs for comparison.

Overview:
The LED Panel Analyzer helps technicians and engineers:
Compare the brightness of different LEDs on a panel
Analyze color differences between LEDs
Determine which LEDs are functioning properly (ON) and which might be faulty (OFF)

Key Functions:
The script performs the following operations:
Image Loading: Reads an image file named "panel.jpeg"
Image Resizing: Resizes the image to 800x600 pixels for consistent display
Color Space Conversion: Converts the image from BGR to HSV color space for better brightness analysis
Interactive Selection: Allows users to click on two different LEDs in the image
Analysis: Compares the RGB values and brightness (Value channel in HSV) of the selected LEDs
Status Determination: Determines which LED is ON and which is OFF based on brightness comparison
Comparison Logic:
When two clicks are registered, it compares the two LEDs
Calculates the absolute difference in RGB values
Determines which LED is ON based on which has higher brightness

Usage:
Place an image of your LED panel in the same directory as the script, named "panel.jpeg"
Run the script
Click on two different LEDs in the displayed image
View the comparison results in the console output

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
Python 3.x
OpenCV (pip install opencv-python)
NumPy (pip install numpy)

Applications:
Quality control in LED manufacturing
Troubleshooting LED panel issues
Educational purposes for understanding color spaces and image processing

Limitations:
Relies on an accurate image representation of the LED panel
Brightness comparison is relative between two LEDs rather than absolute
Does not account for ambient lighting conditions that might affect the image

Future Enhancements:
Implement absolute brightness thresholds
Support for analyzing more than two LEDs at once
Batch Processing for multiple images
