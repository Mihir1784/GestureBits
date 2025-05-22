import cv2
import mediapipe as mp
import numpy as np
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

# Initialize MediaPipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize volume control using pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()
min_vol, max_vol = volume_range[0], volume_range[1]

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Variables for gesture tracking
prev_time = 0
gesture_cooldown = 1  # seconds between gesture recognition
last_gesture_time = 0
prev_x = 0
swipe_threshold = 100  # pixels
is_playing = True


# Function to count raised fingers
def count_fingers(hand_landmarks, hand_label):
    finger_states = [0, 0, 0, 0, 0]  # [Thumb, Index, Middle, Ring, Pinky]

    # Thumb
    if hand_label == 'Right':
        finger_states[0] = 1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0
    else:  # Left
        finger_states[0] = 1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0

    # Other fingers
    for i, tip in enumerate([8, 12, 16, 20]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[i + 1] = 1

    return finger_states




def detect_gesture(hand_landmarks, frame_height, frame_width, hand_label):
    global prev_x

    index_tip = hand_landmarks.landmark[8]
    index_tip_x, index_tip_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
    wrist = hand_landmarks.landmark[0]

    finger_states = count_fingers(hand_landmarks, hand_label)

    x_diff = index_tip_x - prev_x
    prev_x = index_tip_x

    # Only index finger up
    if finger_states == [0, 1, 0, 0, 0]:
        return "VOLUME_UP", index_tip_x, index_tip_y

    # Index and middle finger up
    elif finger_states == [0, 1, 1, 0, 0]:
        return "VOLUME_DOWN", index_tip_x, index_tip_y

    # All fingers up
    elif sum(finger_states) == 5:
        return "PLAY_PAUSE", index_tip_x, index_tip_y

    # Swipe gesture
    elif abs(x_diff) > swipe_threshold:
        return ("NEXT_TRACK" if x_diff > 0 else "PREV_TRACK"), index_tip_x, index_tip_y

    return None, index_tip_x, index_tip_y

# Main loop
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    results = hands.process(image_rgb)

    # Draw the hand annotations on the image
    image_height, image_width, _ = image.shape

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
    prev_time = current_time

    # Display FPS
    cv2.putText(image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display current status
    status_text = "Playing" if is_playing else "Paused"
    cv2.putText(image, f"Status: {status_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display instructions
    instructions = [
        "One finger up: Volume up",
        "Two fingers up: Volume down",
        "Open palm: Play/pause",
        "Swipe right: Next track",
        "Swipe left: Previous track"
    ]

    for i, instruction in enumerate(instructions):
        cv2.putText(image, instruction, (10, 120 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = hand_handedness.classification[0].label  # 'Left' or 'Right'
            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Detect gesture
            gesture, x, y = detect_gesture(hand_landmarks, image_height, image_width,hand_label)

            # Execute action if cooldown has passed
            if gesture and (current_time - last_gesture_time) > gesture_cooldown:
                last_gesture_time = current_time

                if gesture == "VOLUME_UP":
                    # Increase volume by 5%
                    current_vol = volume.GetMasterVolumeLevelScalar()
                    new_vol = min(1.0, current_vol + 0.05)
                    volume.SetMasterVolumeLevelScalar(new_vol, None)
                    cv2.putText(image, "Volume Up", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                elif gesture == "VOLUME_DOWN":
                    # Decrease volume by 5%
                    current_vol = volume.GetMasterVolumeLevelScalar()
                    new_vol = max(0.0, current_vol - 0.05)
                    volume.SetMasterVolumeLevelScalar(new_vol, None)
                    cv2.putText(image, "Volume Down", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                elif gesture == "PLAY_PAUSE":
                    # Toggle play/pause
                    pyautogui.press('playpause')
                    is_playing = not is_playing
                    cv2.putText(image, "Play/Pause", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                elif gesture == "NEXT_TRACK":
                    # Next track
                    pyautogui.press('nexttrack')
                    cv2.putText(image, "Next Track", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                elif gesture == "PREV_TRACK":
                    # Previous track
                    pyautogui.press('prevtrack')
                    cv2.putText(image, "Previous Track", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display current volume
    current_vol = volume.GetMasterVolumeLevelScalar()
    vol_bar_height = int(150 * current_vol)
    cv2.rectangle(image, (image_width - 50, 150), (image_width - 20, 300), (0, 255, 0), 3)
    cv2.rectangle(image, (image_width - 50, 300 - vol_bar_height), (image_width - 20, 300), (0, 255, 0), cv2.FILLED)
    cv2.putText(image, f"{int(current_vol * 100)}%", (image_width - 60, 330), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                2)

    # Show the image
    cv2.imshow('Hand Gesture Media Controller', image)

    # Exit on 'q' press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()