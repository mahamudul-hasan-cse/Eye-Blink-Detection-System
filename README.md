# Eye Blink Detection System

A real-time eye blink detection system using Python, OpenCV, and computer vision techniques. The system detects blinks through your webcam and can simulate keyboard actions (like pressing "Enter") when blinks are detected.

## Features

- **Real-time blink detection** using webcam input
- **Automatic keyboard simulation** (Enter key press on blink detection)
- **Multiple interfaces**: Command-line and GUI versions
- **Modular architecture** for easy customization
- **Adjustable sensitivity** and detection parameters
- **Visual feedback** with blink count and eye detection status
- **Safety features** including PyAutoGUI failsafe

## Project Structure

```
Eye blink detection/
├── main.py                    # Main command-line application
├── gui_app.py                 # GUI application using Tkinter
├── eye_tracker.py             # Eye tracking and blink detection logic
├── utils.py                   # Utility functions and helper classes
├── blink_detection_opencv.py  # Standalone OpenCV-based detection
├── detect_blinks_mine.py      # Original dlib-based script (with issues)
├── requirements.txt           # Python dependencies
├── shape_predictor_68_face_landmarks.dat  # Facial landmark model
└── README.md                  # This file
```

**###Screenshot**
<img width="795" height="635" alt="Screenshot_1" src="https://github.com/user-attachments/assets/496a9fcb-5f2e-4538-af52-b94c1bae650c" />


## Installation

### Prerequisites

- Python 3.11.9 (recommended)
- Windows 10/11 (tested)
- Webcam connected to your computer

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

Run the main application:
```bash
python main.py
```

**Controls:**
- `q` - Quit the application
- `s` - Toggle Enter key simulation ON/OFF
- `r` - Reset blink counter

### GUI Interface

Run the GUI application:
```bash
python gui_app.py
```

**Features:**
- Start/Stop detection with button
- Toggle Enter key simulation with checkbox
- Adjust blink sensitivity with slider
- View real-time statistics
- Activity log with timestamps
- Reset counter functionality

### Standalone Version

For a simple standalone version:
```bash
python blink_detection_opencv.py
```

## How It Works

1. **Face Detection**: Uses OpenCV's Haar cascade classifiers to detect faces
2. **Eye Detection**: Detects eyes within detected face regions
3. **Blink Detection**: Monitors the number of detected eyes over consecutive frames
4. **Action Trigger**: When a blink is detected (eyes closed for specified frames), triggers keyboard action

### Detection Algorithm

- When fewer than 2 eyes are detected, the system considers it a potential blink
- A blink is confirmed when eyes remain closed for a configurable number of consecutive frames (default: 3)
- Upon blink confirmation, the system can simulate an Enter key press

## Configuration

### Adjustable Parameters

In `eye_tracker.py`:
- `blink_threshold`: Sensitivity threshold (not used in current OpenCV implementation)
- `consecutive_frames`: Number of frames needed to confirm a blink (default: 3)

In `utils.py`:
- Camera source index (default: 0)
- Frame width for processing (default: 600px)
- PyAutoGUI settings (pause, failsafe)

## Troubleshooting

### Camera Issues

If you encounter camera problems:

1. **Check camera connection** and ensure it's not being used by another application
2. **Try different camera sources** by changing `src=0` to `src=1` in the code
3. **Verify camera permissions** in Windows settings
4. **Test camera** with Windows Camera app first

### Performance Issues

- **Reduce frame width** in `CameraManager` for faster processing
- **Adjust consecutive frames** threshold for more/less sensitive detection
- **Close other applications** that might be using system resources

### Detection Issues

- **Ensure good lighting** for better face/eye detection
- **Position yourself** properly in front of the camera
- **Adjust sensitivity** using the GUI slider or modifying parameters in code

## Safety Features

- **PyAutoGUI Failsafe**: Move mouse to top-left corner to immediately stop all automation
- **Toggle functionality**: Easily enable/disable keyboard simulation
- **Visual feedback**: Always shows current status and detection count

## Dependencies

- `opencv-python`: Computer vision and image processing
- `imutils`: Image processing utilities
- `numpy`: Numerical computing
- `pyautogui`: Keyboard and mouse automation
- `scipy`: Scientific computing (for distance calculations)
- `pillow`: Image processing for GUI

## Known Issues

- **dlib compatibility**: The original dlib-based implementation has compatibility issues with some Windows systems
- **Lighting sensitivity**: Detection accuracy depends on lighting conditions
- **False positives**: May detect blinks when looking away or during rapid eye movements

## Future Improvements

- [ ] Add support for custom key mappings
- [ ] Implement mouse click simulation
- [ ] Add calibration mode for personalized detection
- [ ] Support for multiple action types
- [ ] Add data logging and analytics
- [ ] Implement machine learning-based detection

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source and available under the MIT License.

## Acknowledgments

- OpenCV community for computer vision tools
- PyAutoGUI for automation capabilities
- imutils library for image processing utilities
