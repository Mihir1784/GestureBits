import cv2

class Camera:
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        return cv2.flip(frame, 1)  # Flip horizontally for selfie view

    def release(self):
        self.cap.release()

    def is_opened(self):
        return self.cap.isOpened() 