
import cv2
import numpy as np

# to read the image
img = cv2.imread("panel.jpeg")

# Resizing for display
img = cv2.resize(img, (800, 600))

# Convert from BGR to HSV for brightness analysis
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# List to store click info (location, color, brightness)
clicks = []

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        b, g, r = img[y, x]
        v = hsv[y, x][2]  # Brightness from HSV
        print(f"Clicked at ({x}, {y}) → RGB: ({r}, {g}, {b}), Brightness (V): {v}")
        clicks.append((x, y, (r, g, b), v))

        if len(clicks) == 2:
            rgb1 = clicks[0][2]
            rgb2 = clicks[1][2]
            v1 = clicks[0][3]
            v2 = clicks[1][3]

            diff = tuple(abs(a - b) for a, b in zip(rgb1, rgb2))

            print("\n--- LED RGB & Brightness Comparison ---")
            print(f"LED 1 @ {clicks[0][0:2]} → RGB: {rgb1}, V = {v1}")
            print(f"LED 2 @ {clicks[1][0:2]} → RGB: {rgb2}, V = {v2}")
            print(f"RGB Difference: {diff}")

            threshold = (v1 + v2) // 2 # You can adjust this based on brightness in your panel image
            if v1 > v2:
                print("LED 1 is ON")
            else:
                print("LED 1 is OFF")

            if v2 > v1:
                print("LED 2 is ON")
            else:
                print("LED 2 is OFF")

# Creating GUI window to diplay image and register mouse callback
cv2.imshow("Click on TWO LEDs", img)
cv2.setMouseCallback("Click on TWO LEDs", on_click)

# wait for user interaction
cv2.waitKey(0)

#removing GUI window from screen and memory 
cv2.destroyAllWindows()