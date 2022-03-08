# imports
import time
import cv2
import sys
from PyQt5.QtWidgets import QApplication

import EyeDetection as eye
import Mouse
import ArmDetection as arm
import ToolBar as tool
import Controls


class OptionsControl:
    def __init__(self, keyboard, left, right, scroll, gestures, mouse, palm_direction, type_move):
        # Open keyboard
        self.keyboard = keyboard
        # Click with left eye
        self.left_click = left
        # Click with right eye
        self.right_click = right
        # Scroll with finger
        self.scroll = scroll
        # Use two finger to double click and three finger to drag
        self.gestures = gestures
        # Control the pointer of mouse
        self.mouse = mouse
        # Click with palm orientation
        self.palm_direction = palm_direction
        # Type of control
        self.type_move = type_move


class TimerControl:
    def __init__(self, ts_left, ll, ts_right, lr, ts_both, lb, tsup, lup, tsdown, ld, tstup, two_up, tsthup, lthup):
        self.ts_left = ts_left
        self.last_left = ll
        self.left_repeat = True
        self.left_repeat_palm = True
        self.ts_right = ts_right
        self.last_right = lr
        self.ts_both = ts_both
        self.last_both = lb
        self.ts_up = tsup
        self.last_up = lup
        self.ts_down = tsdown
        self.last_down = ld
        self.ts_two_up = tstup
        self.last_two_up = two_up
        self.ts_three_up = tsthup
        self.last_three_up = lthup
        self.ts_hand_hor = 0
        self.last_hand_hor = False
        self.ts_hand_reverse = 0
        self.last_hand_reverse = False


# Options and timers
op = OptionsControl(False, False, False, False, False, False, False, 0)
times = TimerControl(0, False, 0, False, 0, False, 0, False, 0, False, 0, False, 0, False)

# Toolbar
App = QApplication(sys.argv)
window = tool.ToolBar()

# Arm
arm = arm.ArmDetection()

# Iris
number_arms = False
iris_detector = eye.EyeDetection()

# Mouse
press = False
m = Mouse.Mouse()

# Class Controls
control = Controls.Controls(press=False)

# Stream
print("[INFO] starting video stream thread...")
cap = cv2.VideoCapture(0)
ret, img = cap.read()
time.sleep(1.0)


def close():
    cv2.destroyAllWindows()
    sys.exit(App.exec())


# times
times.ts_right = time.time()
times.ts_left = time.time()
times.ts_both = time.time()
times.ts_up = time.time()
times.ts_two_up = time.time()
times.ts_three_up = time.time()
time.ts_hand_hor = time.time()
time.ts_hand_reverse = time.time()


# loop
while True:
    ret, img = cap.read()

    res_iris, times, img = control.iris_control(img, op, times, iris_detector, window, m)

    res_arm, times, img = control.arm_control(img, times, op, m, arm, window)

    if res_iris:
        if res_arm:
            window.printf_msg("Alertas são exibidos aqui!")

    op.keyboard = window.statea()
    op.left_click = window.stateb()
    op.right_click = window.statec()
    op.scroll = window.stated()
    op.gestures = window.statee()
    op.palm_direction = window.statef()
    op.mouse = window.stateg()
    op.type_move = window.option_select()

    window.update()
    window.show()
    cv2.imshow('img', img)

    cv2.waitKey(1)
    window.button.clicked.connect(close)

# Clean
cv2.destroyAllWindows()
sys.exit(App.exec())
