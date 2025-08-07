"""
Main application for Eye Blink Detection System
"""

from eye_tracker import EyeTracker
from utils import CameraManager, ActionSimulator, DisplayManager, print_instructions, handle_key_press


def main():
    """Main application function"""
    
    # Print instructions
    print_instructions()
    
    # Initialize components
    try:
        print("[INFO] Initializing components...")
        
        # Initialize eye tracker
        eye_tracker = EyeTracker(
            blink_threshold=0.5,
            consecutive_frames=3
        )
        
        # Initialize camera manager
        camera = CameraManager(src=0, width=600)
        
        # Initialize action simulator
        action_simulator = ActionSimulator(enabled=True)
        
        # Initialize display manager
        display = DisplayManager("Eye Blink Detection System")
        
        print("[INFO] All components initialized successfully!")
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize components: {e}")
        return
    
    # Start camera
    try:
        camera.start()
    except Exception as e:
        print(f"[ERROR] Camera initialization failed: {e}")
        print("Please check:")
        print("1. Camera is connected")
        print("2. Camera is not being used by another application")
        print("3. Camera permissions are granted")
        return
    
    print("[INFO] Starting main detection loop...")
    print("[INFO] Press 'q' to quit, 's' to toggle simulation, 'r' to reset counter")
    
    # Main detection loop
    try:
        while True:
            # Read frame from camera
            frame = camera.read_frame()
            
            if frame is None:
                print("[WARNING] No frame captured from camera")
                continue
            
            # Detect faces and eyes
            faces, eyes, processed_frame = eye_tracker.detect_faces_and_eyes(frame)
            
            # Process blink detection
            blink_detected = eye_tracker.process_blink_detection(eyes)
            
            # Handle blink action
            if blink_detected:
                success = action_simulator.press_enter()
                if success:
                    stats = eye_tracker.get_stats()
                    print(f"[ACTION] Blink #{stats['total_blinks']} detected! Enter key pressed.")
            
            # Draw statistics and info
            additional_info = {
                "Enter Sim": "ON" if action_simulator.enabled else "OFF",
                "Faces": len(faces)
            }
            processed_frame = eye_tracker.draw_stats(processed_frame, additional_info)
            
            # Display frame
            display.show_frame(processed_frame)
            
            # Handle key presses
            key = display.wait_key(1)
            if not handle_key_press(key, eye_tracker, action_simulator):
                break
                
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    
    finally:
        # Cleanup
        print("[INFO] Cleaning up...")
        camera.stop()
        display.cleanup()
        
        # Print final statistics
        stats = eye_tracker.get_stats()
        print(f"\n[INFO] Session Summary:")
        print(f"  Total blinks detected: {stats['total_blinks']}")
        print(f"  Thank you for using Eye Blink Detection System!")


if __name__ == "__main__":
    main()
