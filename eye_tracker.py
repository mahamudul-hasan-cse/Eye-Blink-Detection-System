"""
Eye Tracker Module
Handles eye detection and blink detection logic
"""

import cv2
import numpy as np


class EyeTracker:
    def __init__(self, blink_threshold=0.5, consecutive_frames=3):
        """
        Initialize the eye tracker
        
        Args:
            blink_threshold (float): Threshold for determining blinks
            consecutive_frames (int): Number of consecutive frames needed to confirm blink
        """
        # Initialize cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Blink detection parameters
        self.blink_threshold = blink_threshold
        self.consecutive_frames = consecutive_frames
        
        # State variables
        self.frame_counter = 0
        self.total_blinks = 0
        self.eye_closed_frames = 0
        self.last_eye_count = 0
        
    def reset_counters(self):
        """Reset all counters"""
        self.frame_counter = 0
        self.total_blinks = 0
        self.eye_closed_frames = 0
        
    def detect_faces_and_eyes(self, frame):
        """
        Detect faces and eyes in the frame
        
        Args:
            frame: Input frame from camera
            
        Returns:
            tuple: (faces, all_eyes, processed_frame)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        all_eyes = []
        
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Extract face region for eye detection
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            
            # Detect eyes in face region
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
            
            # Draw rectangles around eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                # Convert eye coordinates to global frame coordinates
                global_eye = (x + ex, y + ey, ew, eh)
                all_eyes.append(global_eye)
        
        return faces, all_eyes, frame
    
    def process_blink_detection(self, eyes):
        """
        Process blink detection based on eye count
        
        Args:
            eyes: List of detected eyes
            
        Returns:
            bool: True if a blink was detected, False otherwise
        """
        blink_detected = False
        
        # Consider it a potential blink if less than 2 eyes are detected
        if len(eyes) < 2:
            self.eye_closed_frames += 1
        else:
            # Eyes are open, check if we had enough closed frames for a blink
            if self.eye_closed_frames >= self.consecutive_frames:
                self.total_blinks += 1
                blink_detected = True
            
            # Reset closed frames counter
            self.eye_closed_frames = 0
        
        self.last_eye_count = len(eyes)
        return blink_detected
    
    def get_stats(self):
        """
        Get current tracking statistics
        
        Returns:
            dict: Dictionary containing tracking stats
        """
        return {
            'total_blinks': self.total_blinks,
            'eye_closed_frames': self.eye_closed_frames,
            'last_eye_count': self.last_eye_count,
            'consecutive_frames_threshold': self.consecutive_frames
        }
    
    def draw_stats(self, frame, additional_info=None):
        """
        Draw statistics on the frame
        
        Args:
            frame: Frame to draw on
            additional_info: Additional information to display
        """
        stats = self.get_stats()
        
        # Draw basic stats
        cv2.putText(frame, f"Blinks: {stats['total_blinks']}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Eyes: {stats['last_eye_count']}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Closed frames: {stats['eye_closed_frames']}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Draw additional info if provided
        if additional_info:
            y_offset = 120
            for key, value in additional_info.items():
                cv2.putText(frame, f"{key}: {value}", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                y_offset += 30
        
        return frame
