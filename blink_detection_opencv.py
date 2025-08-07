import cv2
import numpy as np
import pyautogui
import time
from imutils.video import VideoStream
import imutils


class BlinkDetector:
    def __init__(self):
        # Initialize face and eye cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Blink detection parameters
        self.blink_threshold = 0.5  # Threshold for eye area ratio
        self.consecutive_frames = 3  # Frames needed to confirm blink
        self.frame_counter = 0
        self.total_blinks = 0
        self.last_eye_area = 0
        self.eye_closed_frames = 0
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        self.simulate_enter = True
        
    def calculate_eye_area_ratio(self, eyes, face_area):
        """Calculate the ratio of eye area to face area"""
        if len(eyes) == 0:
            return 0
        
        total_eye_area = 0
        for (ex, ey, ew, eh) in eyes:
            total_eye_area += ew * eh
            
        return total_eye_area / face_area if face_area > 0 else 0
    
    def detect_blink(self, frame):
        """Detect blinks in the given frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Extract face region
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            
            # Detect eyes in the face region
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
            
            # Calculate face area
            face_area = w * h
            
            # Calculate eye area ratio
            current_eye_ratio = self.calculate_eye_area_ratio(eyes, face_area)
            
            # Draw rectangles around eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            
            # Blink detection logic
            if len(eyes) < 2:  # If less than 2 eyes detected, consider it a potential blink
                self.eye_closed_frames += 1
            else:
                if self.eye_closed_frames >= self.consecutive_frames:
                    self.total_blinks += 1
                    
                    # Trigger keyboard action
                    if self.simulate_enter:
                        try:
                            pyautogui.press('enter')
                            print(f"[ACTION] Blink #{self.total_blinks} detected! Enter key pressed.")
                        except Exception as e:
                            print(f"[ERROR] Failed to simulate Enter key: {e}")
                
                self.eye_closed_frames = 0
            
            # Display information on frame
            cv2.putText(frame, f"Blinks: {self.total_blinks}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"Eyes: {len(eyes)}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Closed frames: {self.eye_closed_frames}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Show simulation status
            status = "ON" if self.simulate_enter else "OFF"
            cv2.putText(frame, f"Enter Sim: {status}", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        return frame


def main():
    print("[INFO] Starting OpenCV-based blink detection...")
    print("[INFO] Press 'q' to quit, 's' to toggle Enter key simulation")
    
    # Initialize blink detector
    detector = BlinkDetector()
    
    # Start video stream
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    
    # Test camera
    test_frame = vs.read()
    if test_frame is None:
        print("[ERROR] Cannot access camera")
        vs.stop()
        return
    
    print(f"[INFO] Camera working! Frame shape: {test_frame.shape}")
    
    while True:
        frame = vs.read()
        
        if frame is None:
            print("[WARNING] No frame captured")
            continue
        
        # Resize for faster processing
        frame = imutils.resize(frame, width=600)
        
        # Detect blinks
        frame = detector.detect_blink(frame)
        
        # Show frame
        cv2.imshow("OpenCV Blink Detection", frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            detector.simulate_enter = not detector.simulate_enter
            print(f"[INFO] Enter simulation: {'ON' if detector.simulate_enter else 'OFF'}")
    
    # Cleanup
    print("[INFO] Cleaning up...")
    cv2.destroyAllWindows()
    vs.stop()


if __name__ == "__main__":
    main()
