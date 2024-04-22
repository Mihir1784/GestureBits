# Hand Gesture Media Controller

A Python application that allows you to control media playback using hand gestures captured through your webcam. This project uses computer vision and machine learning to detect hand gestures and translate them into media control commands.

## Features

- Volume control using finger gestures
- Play/Pause control with open palm gesture
- Track navigation with swipe gestures
- Real-time hand tracking visualization
- FPS counter and status display
- Volume level indicator

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI
- pycaw (for Windows volume control)
- comtypes (for Windows volume control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mihir1784/GestureBits.git
cd GestureBits
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Use the following gestures to control media:
   - One finger up: Increase volume
   - Two fingers up: Decrease volume
   - Open palm: Play/Pause
   - Swipe right: Next track
   - Swipe left: Previous track

3. Press 'q' to quit the application

## Project Structure

```
GestureBits/
├── core/
│   ├── hand_detector.py    # Hand detection and landmark processing
│   ├── gesture_controller.py    # Gesture recognition logic
│   └── media_controller.py    # Media control functions
├── utils/
│   ├── camera.py    # Camera setup and management
│   └── display.py    # Display and UI functions
├── main.py    # Main application file
├── requirements.txt    # Project dependencies
└── README.md    # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe for hand tracking
- OpenCV for computer vision
- pycaw for Windows volume control 