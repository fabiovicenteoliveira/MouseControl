import cv2
import mediapipe as mp


class ArmDetection:
    def __init__(self, coefficient=0.7):
        self.results = []
        self.lmList = []

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(False, 1, coefficient, coefficient)

    def convert_to_rgb(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def find_arm(self, imgRGB):
        self.results = self.hands.process(imgRGB)
        if not self.results.multi_hand_landmarks:
            return False
        return True

    def two_or_three_fingers(self, b, y1, y2, y3):
        # Two, Three or zero fingers up
        if (y3 < (b - 20)) and (y2 < (b-20)) and (y1 < (b-20)):
            return "THREE"
        elif (y2 < (b-20)) and (y1 < (b-20)):
            return "TWO"
        return "DOWN"

    def finger_up_or_down(self, y1, y2):
        # Finger up or down
        if y1 < (y2 - 20):
            return "UP"
        elif y1 > (y2 + 20):
            return "DOWN"
        return "MIDDLE"

    def click_arm(self, y1, y2):
        # Left click: Arm in vertical -90
        # Right click: Arm in vertical +90
        # print("Y1: ", y1, " Y2: ", y2)

        if y2+25 < y1 < y2 + 40:
            return "LEFT"
        elif y1 > y2 + 45:
            return "RIGHT"
        return "NONE"

    def find_all_positions(self, img):
        # Find all positions of all 21 points
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

                # Draw
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.circle(img, (cx, cy), 4, (255, 0, 255), cv2.FILLED)

        return self.lmList, img
