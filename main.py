import cv2
import time
from core.hand_detector import HandDetector
from core.gesture_controller import GestureController
from core.media_controller import MediaController
from utils.camera import Camera
from utils.display import Display

def main():
    # Initialize components
    camera = Camera()
    hand_detector = HandDetector()
    gesture_controller = GestureController()
    media_controller = MediaController()
    display = Display()

    # Variables for gesture tracking
    gesture_cooldown = 1  # seconds between gesture recognition
    last_gesture_time = 0

    while camera.is_opened():
        # Read frame
        image = camera.read_frame()
        if image is None:
            print("Ignoring empty camera frame.")
            continue

        # Process frame
        results = hand_detector.process_frame(image)
        image_height, image_width, _ = image.shape

        # Update display
        display.update_fps(image)
        display.show_status(image, media_controller.is_playing)
        display.show_instructions(image)

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = hand_handedness.classification[0].label
                
                # Draw hand landmarks
                hand_detector.draw_landmarks(image, hand_landmarks)

                # Detect gesture
                gesture, x, y = gesture_controller.detect_gesture(hand_landmarks, image_height, image_width, hand_label)

                # Execute action if cooldown has passed
                current_time = time.time()
                if gesture and (current_time - last_gesture_time) > gesture_cooldown:
                    last_gesture_time = current_time

                    if gesture == "VOLUME_UP":
                        media_controller.volume_up()
                        display.show_gesture_text(image, "Volume Up", x, y)

                    elif gesture == "VOLUME_DOWN":
                        media_controller.volume_down()
                        display.show_gesture_text(image, "Volume Down", x, y)

                    elif gesture == "PLAY_PAUSE":
                        media_controller.toggle_play_pause()
                        display.show_gesture_text(image, "Play/Pause", x, y)

                    elif gesture == "NEXT_TRACK":
                        media_controller.next_track()
                        display.show_gesture_text(image, "Next Track", x, y)

                    elif gesture == "PREV_TRACK":
                        media_controller.previous_track()
                        display.show_gesture_text(image, "Previous Track", x, y)

        # Show volume bar
        display.show_volume_bar(image, media_controller.get_current_volume())

        # Show the image
        cv2.imshow('Hand Gesture Media Controller', image)

        # Exit on 'q' press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 