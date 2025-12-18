import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1):
        self.hands = mp.solutions.hands.Hands(max_num_hands=max_hands)

    def get_index_finger(self, frame_rgb):
        result = self.hands.process(frame_rgb)
        if not result.multi_hand_landmarks:
            return None

        lm = result.multi_hand_landmarks[0].landmark[8]
        return lm.x, lm.y  # normalized (0–1)
