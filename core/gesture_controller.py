class GestureController:
    def __init__(self):
        self.prev_x = 0
        self.swipe_threshold = 100  # pixels

    def count_fingers(self, hand_landmarks, hand_label):
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

    def detect_gesture(self, hand_landmarks, frame_height, frame_width, hand_label):
        index_tip = hand_landmarks.landmark[8]
        index_tip_x, index_tip_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)

        finger_states = self.count_fingers(hand_landmarks, hand_label)

        x_diff = index_tip_x - self.prev_x
        self.prev_x = index_tip_x

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
        elif abs(x_diff) > self.swipe_threshold:
            return ("NEXT_TRACK" if x_diff > 0 else "PREV_TRACK"), index_tip_x, index_tip_y

        return None, index_tip_x, index_tip_y 