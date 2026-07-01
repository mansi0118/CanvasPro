import cv2
import mediapipe as mp
class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands # loads hands modules

        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )

        self.mpDraw = mp.solutions.drawing_utils # in built drawing tools


    def find_hands(self, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb_frame)

        landmark_list = []

        if results.multi_hand_landmarks:

            for handLms in results.multi_hand_landmarks:

                h, w, c = frame.shape

                for id, lm in enumerate(handLms.landmark):

                    cx = int(lm.x * w) #normalized to pixel coordinates
                    cy = int(lm.y * h)

                    landmark_list.append((id, cx, cy))

                self.mpDraw.draw_landmarks(
                    frame,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

        return frame, landmark_list