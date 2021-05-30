import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, track_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(mode, max_hands, detection_confidence, track_confidence)

    def draw_hands_on_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(img_rgb)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_number=0):
        landmark_list = []
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(img_rgb)
        if result.multi_hand_landmarks:
            # TODO implementare strategia per far scegliere la mano destra o sinistra
            selected_hand = result.multi_hand_landmarks[len(result.multi_hand_landmarks) - 1]
            for id, landmark in enumerate(selected_hand.landmark):
                height, width, c = img.shape
                cx, cy, cz = int(landmark.x * width), int(landmark.y * height), landmark.z
                landmark_list.append([id, cx, cy, cz])
        return landmark_list


