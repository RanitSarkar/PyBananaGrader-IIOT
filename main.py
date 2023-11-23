import cv2
import numpy as np
import serial
import time

def control_servo(ser, angle):
    # Send the command to the Arduino
    command = f'A{angle}\n'
    ser.write(command.encode())
    time.sleep(0.5)  # Add a delay after moving the servo

# Function to detect yellow bananas in an image
def detect_yellow_banana(frame):
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the image to get only yellow pixels
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Find contours in the yellow mask
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours are found
    if contours:
        # Get the bounding box for the largest contour (assumed to be the banana)
        banana_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(banana_contour)

        # Draw a rectangle around the detected banana
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Banana detected
        banana_detected = True
    else:
        # No banana detected
        banana_detected = False

    return frame, banana_detected

# IP webcam URL (replace it with your webcam URL)
url = 'http://192.168.213.38:8080/video'

# Open the video stream
cap = cv2.VideoCapture(url)

# Check if the video stream is opened successfully
if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

# Serial communication with Arduino
ser = serial.Serial('COM7', 9600, timeout=1)  # Change 'COM3' to the actual port of your Arduino

time.sleep(2)  # Allow time for Arduino to initialize
banana_detected_prev = False
while True:
    # Read a frame from the video stream
    # Read a frame from the video stream
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to read frame.")
        break

    # Detect yellow banana in the frame
    frame, banana_detected = detect_yellow_banana(frame)

    # Display the frame
    cv2.imshow('Banana Detection', frame)

    # Check if banana detection status has changed
    if banana_detected != banana_detected_prev:
        # If banana is now detected, move the servo to 90 degrees
        # If banana is not detected, move the servo to 0 degrees
        control_servo(ser, 90 if banana_detected else 0)

    # Update the previous banana detection status
    banana_detected_prev = banana_detected

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream, close all windows, and close the serial connection
cap.release()
cv2.destroyAllWindows()
ser.close()
