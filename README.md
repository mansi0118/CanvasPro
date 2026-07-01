# 🎨 Canvas Pro

Canvas Pro is a real-time AI-powered hand gesture drawing application built using Computer Vision, OpenCV, and MediaPipe.

It allows users to draw on screen using only hand gestures and a webcam — no mouse, no touchscreen, no graphics tablet.

The project started as an experiment to explore hand tracking and real-time video processing, and gradually evolved into a complete interactive drawing system with gesture controls, neon rendering, multiple themes, HSV color selection, undo functionality, and modern UI interactions.

---

# ✨ Features

## 🖐️ Gesture-Based Interaction

* Draw using a single index finger
* Erase using two-finger gesture
* Open hand for navigation mode

## 🎨 Advanced Drawing System

* Smooth real-time drawing
* Dynamic brush sizes
* HSV rainbow color selector
* Unlimited color selection

## 🧠 Smart Interaction Design

* Mode-aware cursor system
* Gesture-state recognition
* Real-time mode detection
* Save notifications
* Undo support

## 🖥️ Modern UI

* Fullscreen responsive layout
* Picture-in-picture webcam preview
* Startup screen with animations
* Theme switching system
* Live mode panels

## 🎭 Multiple Themes

* Black Neon Theme
* Whiteboard Theme
* Grid Theme
* Dark Blue Theme

## 💾 Utility Features

* Save drawings as PNG images
* Undo previous strokes
* Clear canvas
* Adjustable brush size

---

# 🛠️ Technologies Used

| Technology      | Purpose                                |
| --------------- | -------------------------------------- |
| Python          | Core programming language              |
| OpenCV          | Real-time rendering & video processing |
| MediaPipe       | Hand tracking & gesture detection      |
| NumPy           | Canvas & image operations              |
| Computer Vision | Gesture recognition system             |

---

# 📸 Screenshots

Create a folder named:

```text
screenshots/
```

Added screenshots such as:

* Startup Screen
* Drawing Mode
* Eraser Mode
* HSV Color Selector
* Theme Switching
* Save Notification


# 🎮 Controls

## ✍️ Gestures

| Gesture        | Action     |
| -------------- | ---------- |
| ☝️ One Finger  | Draw       |
| ✌️ Two Fingers | Erase      |
| ✋ Open Hand    | Navigation |

---

## ⌨️ Keyboard Shortcuts

| Key     | Action           |
| ------- | ---------------- |
| S       | Save Drawing     |
| Z       | Undo             |
| Q / ESC | Quit Application |
| 1       | Black Theme      |
| 2       | Whiteboard Theme |
| 3       | Grid Theme       |
| 4       | Dark Blue Theme  |

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/mansi0118/CanvasPro.git
```

---

## 2️⃣ Open Project Folder

```bash
cd CanvasPro
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Run Application

```bash
python main.py
```

---

# 📂 Project Structure

```text
Canvas-Pro/
│
├── screenshots/
├── main.py
├── hand_tracker.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🧠 How It Works

Canvas Pro uses MediaPipe Hands to detect and track hand landmarks in real time through the webcam.

The application recognizes specific finger states and gestures:

* One finger → drawing mode
* Two fingers → eraser mode
* Open hand → navigation mode

Finger coordinates are then mapped to a virtual canvas rendered using OpenCV.

The HSV color selector dynamically converts hue values into BGR drawing colors, allowing smooth unlimited color selection.

---

# 🔮 Future Improvements

Planned future upgrades:

* Mobile/Web version
* AI shape smoothing
* Gesture shortcuts
* Layer system
* Multiplayer collaborative drawing
* Cloud save support
* Presentation mode
* Voice commands
* Animated particle brushes

---


# 🤝 Contributing

Contributions, ideas, and improvements are welcome.

Feel free to fork the repository and submit pull requests.

---


# ⭐ Acknowledgements

Special thanks to:

* OpenCV
* MediaPipe
* Python community
* Computer Vision open-source ecosystem

for making projects like this possible.

---

# 💡 Project Highlights

Canvas Pro demonstrates:

✅ Real-Time Computer Vision

✅ AI-Based Hand Tracking

✅ Gesture-State Recognition

✅ Human-Computer Interaction (HCI)

✅ Real-Time Graphics Rendering

✅ UI/UX System Design

✅ State Management Architecture

✅ Interactive Creative Software Design

---

# 👩‍💻 Author

Developed by Mansi Tiwari.
