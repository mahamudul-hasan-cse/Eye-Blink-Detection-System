from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import time
import numpy as np
import imutils
import cv2
import dlib
import pyautogui
import os


def eye_aspect_ratio(eye):
    """Calculate the Eye Aspect Ratio (EAR) for blink detection"""
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear


# Path to the facial landmark predictor
SHAPE_PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"

# Check if the shape predictor file exists
if not os.path.exists(SHAPE_PREDICTOR_PATH):
    print(f"[ERROR] Shape predictor file not found: {SHAPE_PREDICTOR_PATH}")
    print("Please ensure the file is in the current directory.")
    exit()

# Define constants for blink detection
EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold for blink detection
EYE_AR_CONSEC_FRAMES = 3  # Number of consecutive frames the eye must be below threshold

# Initialize counters
COUNTER = 0  # Frame counter for consecutive low EAR frames
TOTAL = 0    # Total number of blinks detected

# Configure pyautogui
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.1      # Small pause between actions

print('[INFO] Loading facial landmark predictor...')
predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)

# Load OpenCV's face detector (Haar cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Get the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

print('[INFO] Starting video stream from webcam...')
vs = VideoStream(src=0).start()
time.sleep(2.0)  # Allow camera sensor to warm up

# Test if camera is working
test_frame = vs.read()
if test_frame is None:
    print("[ERROR] Cannot access camera. Please check if:")
    print("1. Camera is connected and not being used by another application")
    print("2. Camera permissions are granted")
    print("3. Try changing src=0 to src=1 in VideoStream")
    vs.stop()
    exit()
else:
    print(f"[INFO] Camera working! Frame shape: {test_frame.shape}, dtype: {test_frame.dtype}")

print('[INFO] Press "q" to quit, "s" to toggle Enter key simulation')
simulate_enter = True  # Flag to control Enter key simulation

while True:
    frame = vs.read()
    
    # Handle the case where frame is None (camera disconnected)
    if frame is None:
        print("[WARNING] No frame captured from camera")
        continue
        
    # Resize frame for faster processing
    frame = imutils.resize(frame, width=450)
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using OpenCV's Haar cascade
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        # Create a dlib rectangle object from OpenCV detection
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        try:
            # Determine the facial landmarks for the face region
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # Extract the left and right eye coordinates
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # Average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # Compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # Check to see if the eye aspect ratio is below the blink threshold
            if ear < EYE_AR_THRESH:
                COUNTER += 1
            else:
                # If the eyes were closed for a sufficient number of frames
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                    
                    # Trigger keyboard action when blink is detected
                    if simulate_enter:
                        try:
                            pyautogui.press('enter')
                            print(f"[ACTION] Blink #{TOTAL} detected! Enter key pressed.")
                        except Exception as e:
                            print(f"[ERROR] Failed to simulate Enter key: {e}")

                # Reset the eye frame counter
                COUNTER = 0

            # Draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Threshold: {:.2f}".format(EYE_AR_THRESH), (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Show simulation status
            status = "ON" if simulate_enter else "OFF"
            cv2.putText(frame, f"Enter Sim: {status}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                       
        except Exception as e:
            print(f"[WARNING] Landmark detection failed: {e}")
            continue

    # Show the frame
    cv2.imshow("Eye Blink Detection (OpenCV + dlib)", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    # If the `s` key was pressed, toggle Enter key simulation
    elif key == ord("s"):
        simulate_enter = not simulate_enter
        print(f"[INFO] Enter key simulation: {'ON' if simulate_enter else 'OFF'}")

# Cleanup
print("[INFO] Cleaning up...")
cv2.destroyAllWindows()
vs.stop()
