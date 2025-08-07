# 🎯 Eye Blink Detection System

**A real-time computer vision application that detects eye blinks and simulates Enter key presses — designed for accessibility, automation, and hands-free interaction.**

---

## 📌 Overview

This project uses a webcam feed to detect human blinks using facial landmarks and Eye Aspect Ratio (EAR). When a blink is detected, it can simulate pressing the **Enter key**. This allows hands-free control of applications like Notepad, PowerPoint, and more.

Built with:
- **Python**
- **OpenCV**
- **dlib**
- **PyAutoGUI**
- **Tkinter (for GUI version)**

---

## 🧠 How It Works

1. **Face Detection** – OpenCV Haar Cascade or Dlib HOG
2. **Eye Landmark Detection** – Dlib's 68-point shape predictor
3. **EAR Calculation** – Computes vertical/horizontal eye distances
4. **Blink Detection** – If EAR falls below threshold for a number of frames
5. **Action** – Simulates pressing Enter key using PyAutoGUI

### 👁️ EAR Formula:

<img width="632" height="142" alt="blink_detection_equation" src="https://github.com/user-attachments/assets/2fd760cc-2942-4929-8cc4-d8b74b607e76" />

---

## 🗂️ File Structure

<img width="614" height="386" alt="image" src="https://github.com/user-attachments/assets/5f43f2d2-5edf-4bfa-afef-8b15c150754d" />


## ⚙️ Features

### ✅ Detection
- Real-time video from webcam
- Face and eye detection using facial landmarks
- Eye Aspect Ratio (EAR) calculation
- Accurate blink detection using threshold and frame count

### 🎮 Controls
| Key | Action |
|-----|--------|
| `q` | Quit application |
| `s` | Toggle Enter key simulation |
| `r` | Reset blink counter |
| `SPACE` | Manual Enter key test |

### 📊 Visual Feedback
- Live EAR value on screen
- Blink count on-screen and in console
- Face: blue rectangle, Eyes: green contours
- Console logs:  
[BLINK DETECTED] Enter key pressed.
---

## 🖥️ Application Modes

### 🟢 GUI Version (`gui_app.py`)
- Start/Stop buttons
- Sensitivity slider
- Activity log
- Toggle key simulation

### 🔵 Command-Line Version (`main.py`)
- Lightweight
- Real-time console output
- Key shortcuts

### ⚪ Standalone Version (`working_blink_detector.py`)
- All-in-one script
- Fastest and most stable
- Ideal for demo

---

## 📦 Requirements

- Python 3.11.9 (recommended)
- Webcam (internal or USB)
- Windows 10/11

### Python Libraries

Install everything with:

pip install -r requirements.txt

Or individually:
pip install opencv-python dlib imutils numpy pyautogui

🚀 How to Run:
1. Activate Virtual Environment
cd path/to/project
.\venv\Scripts\activate

3. Run Any Version
GUI:
python gui_app.py

Command-line:
python main.py

Best All-in-One:
python working_blink_detector.py

Or double-click:
run_blink_detector.bat

🧪 Testing Instructions
Open Notepad or any text editor.

Run the program.

Blink normally in front of the webcam.

Observe:

Blink counter increasing

“Enter key pressed” log in terminal

New lines in the editor when simulation is ON

🔐 Important Notes
The file shape_predictor_68_face_landmarks.dat is required for facial landmark detection but is too large for GitHub.
Download it from here:
🔗 https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2

Extract it and place it in your project folder.

🚫 .gitignore (recommended)
gitignore
venv/*.dat*.pyc__pycache__/*.mp4.DS_Store

📚 Use Cases
♿ Accessibility: Help users control systems with eye blinks.
📽️ Presentations: Advance slides without hands.
🧪 HCI Projects: Use as a real-world input control prototype.
🕹️ Automation: Interact with software using eye movement.

💡 Tips
Ensure good lighting and position webcam at eye level.
Blink gently — system tracks both eyes.
Adjust the frame threshold or EAR sensitivity as needed.

🛡️ Safety Features
PyAutoGUI failsafe: Move your mouse to the top-left corner to immediately abort all automation.
Toggle simulation: Press 's' or use GUI checkbox.

🧑‍💻 Author
This project was developed as part of a university Operating Systems course, with support from AI-based augmentation tools and research into computer vision and user input automation.
