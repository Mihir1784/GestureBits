import cv2
import time

class Display:
    def __init__(self):
        self.prev_time = 0
        self.instructions = [
            "One finger up: Volume up",
            "Two fingers up: Volume down",
            "Open palm: Play/pause",
            "Swipe right: Next track",
            "Swipe left: Previous track"
        ]

    def update_fps(self, image):
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time) if (current_time - self.prev_time) > 0 else 0
        self.prev_time = current_time
        cv2.putText(image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return fps

    def show_status(self, image, is_playing):
        status_text = "Playing" if is_playing else "Paused"
        cv2.putText(image, f"Status: {status_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def show_instructions(self, image):
        for i, instruction in enumerate(self.instructions):
            cv2.putText(image, instruction, (10, 120 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def show_volume_bar(self, image, current_vol):
        image_height, image_width, _ = image.shape
        vol_bar_height = int(150 * current_vol)
        cv2.rectangle(image, (image_width - 50, 150), (image_width - 20, 300), (0, 255, 0), 3)
        cv2.rectangle(image, (image_width - 50, 300 - vol_bar_height), (image_width - 20, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(image, f"{int(current_vol * 100)}%", (image_width - 60, 330), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def show_gesture_text(self, image, text, x, y):
        cv2.putText(image, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 