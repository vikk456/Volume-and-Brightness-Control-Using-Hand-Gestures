# Volume and Brightness Control Using Hand Gestures

This project allows you to control your computer's **volume** and **screen brightness** using **hand gestures** detected through your webcam.  
It uses **OpenCV** for video capture, **MediaPipe** for hand tracking, and additional libraries for system volume and brightness control.

---

## 📂 Files in This Repository

- **Brightness.py** → Adjusts **screen brightness** based on the distance between your thumb and index finger.
- **VolumeControl.py** → Adjusts **system volume** based on the distance between your thumb and index finger.
- **HandTrackingModule.py** → A reusable module for detecting hands and landmarks using **MediaPipe**.

---

## ⚙️ Requirements

Install the required Python libraries:

```bash
pip install opencv-python mediapipe numpy pycaw comtypes screen-brightness-control
