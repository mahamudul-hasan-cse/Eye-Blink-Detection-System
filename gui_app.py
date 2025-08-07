"""
GUI Application for Eye Blink Detection System using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
from eye_tracker import EyeTracker
from utils import CameraManager, ActionSimulator


class BlinkDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Blink Detection System")
        self.root.geometry("800x600")
        
        # Initialize components
        self.eye_tracker = EyeTracker()
        self.camera = CameraManager(src=0, width=400)
        self.action_simulator = ActionSimulator(enabled=True)
        
        # GUI state variables
        self.is_running = False
        self.current_frame = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI layout"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Eye Blink Detection System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Video frame
        self.video_frame = ttk.LabelFrame(main_frame, text="Camera Feed", padding="5")
        self.video_frame.grid(row=1, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.video_label = ttk.Label(self.video_frame, text="Camera not started")
        self.video_label.pack()
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Start/Stop button
        self.start_button = ttk.Button(control_frame, text="Start Detection", 
                                      command=self.toggle_detection)
        self.start_button.pack(pady=5, fill=tk.X)
        
        # Simulation toggle
        self.sim_var = tk.BooleanVar(value=True)
        self.sim_checkbox = ttk.Checkbutton(control_frame, text="Enable Enter Key Simulation",
                                           variable=self.sim_var, command=self.toggle_simulation)
        self.sim_checkbox.pack(pady=5, anchor=tk.W)
        
        # Reset button
        self.reset_button = ttk.Button(control_frame, text="Reset Counter", 
                                      command=self.reset_counter)
        self.reset_button.pack(pady=5, fill=tk.X)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(control_frame, text="Statistics", padding="10")
        stats_frame.pack(pady=10, fill=tk.X)
        
        self.blinks_label = ttk.Label(stats_frame, text="Blinks: 0")
        self.blinks_label.pack(anchor=tk.W)
        
        self.eyes_label = ttk.Label(stats_frame, text="Eyes detected: 0")
        self.eyes_label.pack(anchor=tk.W)
        
        self.status_label = ttk.Label(stats_frame, text="Status: Stopped")
        self.status_label.pack(anchor=tk.W)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(control_frame, text="Settings", padding="10")
        settings_frame.pack(pady=10, fill=tk.X)
        
        # Sensitivity setting
        ttk.Label(settings_frame, text="Blink Sensitivity:").pack(anchor=tk.W)
        self.sensitivity_var = tk.IntVar(value=3)
        self.sensitivity_scale = ttk.Scale(settings_frame, from_=1, to=10, 
                                          variable=self.sensitivity_var,
                                          command=self.update_sensitivity)
        self.sensitivity_scale.pack(fill=tk.X, pady=2)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log text widget with scrollbar
        log_scroll_frame = ttk.Frame(log_frame)
        log_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_scroll_frame, height=8, width=80)
        log_scrollbar = ttk.Scrollbar(log_scroll_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        self.log_message("GUI initialized successfully")
        
    def log_message(self, message):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def toggle_detection(self):
        """Start or stop the detection"""
        if not self.is_running:
            self.start_detection()
        else:
            self.stop_detection()
            
    def start_detection(self):
        """Start the detection process"""
        try:
            self.camera.start()
            self.is_running = True
            self.start_button.config(text="Stop Detection")
            self.status_label.config(text="Status: Running")
            self.log_message("Detection started")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {e}")
            self.log_message(f"Error: {e}")
            
    def stop_detection(self):
        """Stop the detection process"""
        self.is_running = False
        self.camera.stop()
        self.start_button.config(text="Start Detection")
        self.status_label.config(text="Status: Stopped")
        self.video_label.config(image="", text="Camera stopped")
        self.log_message("Detection stopped")
        
    def detection_loop(self):
        """Main detection loop running in separate thread"""
        while self.is_running:
            try:
                frame = self.camera.read_frame()
                if frame is None:
                    continue
                
                # Detect faces and eyes
                faces, eyes, processed_frame = self.eye_tracker.detect_faces_and_eyes(frame)
                
                # Process blink detection
                blink_detected = self.eye_tracker.process_blink_detection(eyes)
                
                # Handle blink action
                if blink_detected and self.sim_var.get():
                    success = self.action_simulator.press_enter()
                    if success:
                        stats = self.eye_tracker.get_stats()
                        self.log_message(f"Blink #{stats['total_blinks']} detected! Enter key pressed.")
                
                # Update GUI
                self.update_gui(processed_frame, len(eyes))
                
                time.sleep(0.03)  # ~30 FPS
                
            except Exception as e:
                self.log_message(f"Detection error: {e}")
                break
                
    def update_gui(self, frame, eye_count):
        """Update GUI elements with current data"""
        # Update video display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_pil)
        
        self.video_label.config(image=frame_tk, text="")
        self.video_label.image = frame_tk  # Keep a reference
        
        # Update statistics
        stats = self.eye_tracker.get_stats()
        self.blinks_label.config(text=f"Blinks: {stats['total_blinks']}")
        self.eyes_label.config(text=f"Eyes detected: {eye_count}")
        
    def toggle_simulation(self):
        """Toggle Enter key simulation"""
        self.action_simulator.enabled = self.sim_var.get()
        status = "enabled" if self.sim_var.get() else "disabled"
        self.log_message(f"Enter key simulation {status}")
        
    def reset_counter(self):
        """Reset the blink counter"""
        self.eye_tracker.reset_counters()
        self.log_message("Blink counter reset")
        
    def update_sensitivity(self, value):
        """Update blink detection sensitivity"""
        sensitivity = int(float(value))
        self.eye_tracker.consecutive_frames = sensitivity
        self.log_message(f"Sensitivity updated to {sensitivity}")
        
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            self.stop_detection()
        self.root.destroy()


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = BlinkDetectionGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
