import cv2
import numpy as np
import serial
import time

# Banner
print("""
============================================================
       HandWave Light Controller
       Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan
============================================================
""")

# Initialize variables
hand_detected = False
wave_count = 0
last_wave_time = 0
light_state = False
WAVE_THRESHOLD = 2  # Number of waves to toggle light
TIME_THRESHOLD = 2  # Seconds between valid waves

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Initialize serial (modify port and baud rate as needed)
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Wait for serial connection
except:
    print("Warning: Serial port not connected. Running in simulation mode.")
    ser = None

# Create background subtractor for hand detection
fgbg = cv2.createBackgroundSubtractorMOG2()

def toggle_light(state):
    """Toggle light state via serial (placeholder for actual hardware control)"""
    if ser:
        try:
            ser.write(str(int(state)).encode())
            print(f"Light {'ON' if state else 'OFF'}")
        except:
            print("Error: Failed to send serial command")
    else:
        print(f"Simulated: Light {'ON' if state else 'OFF'}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Convert to grayscale and apply background subtraction
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)

    # Apply threshold and find contours
    _, thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    current_time = time.time()
    hand_present = False

    for contour in contours:
        # Filter small contours
        if cv2.contourArea(contour) > 1000:
            hand_present = True
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

            if not hand_detected and (current_time - last_wave_time) > TIME_THRESHOLD:
                wave_count += 1
                last_wave_time = current_time
                print(f"Wave detected: {wave_count}")

                if wave_count >= WAVE_THRESHOLD:
                    light_state = not light_state
                    toggle_light(light_state)
                    wave_count = 0

    hand_detected = hand_present

    # Display status
    status = f"Light: {'ON' if light_state else 'OFF'} | Waves: {wave_count}"
    cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show video feed
    cv2.imshow('HandWave Light Controller', frame)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()