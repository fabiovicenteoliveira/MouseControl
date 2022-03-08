import pynput
import numpy as np


class Mouse:
    def __init__(self):
        self.mo = pynput.mouse.Controller()
        self.Button = pynput.mouse.Button
        self.keyboard = pynput.keyboard.Controller()
        self.key = pynput.keyboard.Key
        self.wScr, self.hScr = (1366, 768)

    def click(self, cl):
        if cl == 'RIGHT':
            self.mo.press(self.Button.right)
            self.mo.release(self.Button.right)
        elif cl == 'LEFT':
            self.mo.press(self.Button.left)
            self.mo.release(self.Button.left)
        elif cl == 'TWO':
            self.mo.click(self.Button.left, 2)

    def open_keyboard(self):
        self.keyboard.press(self.key.cmd)
        self.keyboard.press(self.key.ctrl)
        self.keyboard.press('o')
        self.keyboard.release(self.key.cmd)
        self.keyboard.release(self.key.ctrl)
        self.keyboard.release('o')

    def scroll_down(self):
        self.mo.scroll(0, -5)

    def scroll_up(self):
        self.mo.scroll(0, 5)

    def drag_press(self):
        self.mo.press(self.Button.left)

    def drag_release(self):
        self.mo.release(self.Button.left)

    def move(self, x, y):
        self.mo.position = (self.wScr - x, y)

    def move_mouse(self, x1, y1, img, smoothening=6):
        frameR = 80
        frameRh = 250
        wCam, hCam, c = img.shape
        (plocX, plocY) = self.mo.position
        plocX = self.wScr - plocX
        #print("Wcm: ", wCam, " H: ", hCam)
        #print("y1: ", y1)
        x2 = np.interp(x1, (frameR, wCam - frameR), (0, self.wScr))
        y2 = np.interp(y1, (70, hCam - frameRh), (0, self.hScr))
        #print("y2: ", y2)

        clocX = plocX + (x2 - plocX) / smoothening
        clocY = plocY + (y2 - plocY) / smoothening

        self.mo.position = (self.wScr - clocX, clocY)

    def move_mouse_eye_direction(self, x1, y1, smoothening=10):
        print('X1: ', x1, ' Y1: ', y1)
        (plocX, plocY) = self.mo.position
        plocX = self.wScr - plocX

        x2 = np.interp(x1, (68, 105), (0, self.wScr))  # 64 120
        y2 = np.interp(y1, (52, 58), (0, self.hScr))  # 48 55

        clocX = plocX + (x2 - plocX) / smoothening
        clocY = plocY + (y2 - plocY) / smoothening

        self.mo.position = (self.wScr - clocX, clocY)

    def move_finger_eye(self, img, x, y, lx, ly, smoothening=1):
        frameR = 100  # 100
        frameRh = 150  # 250
        wCam, hCam, c = img.shape
        (plocX, plocY) = self.mo.position
        plocX = self.wScr - plocX

        lx = np.interp(lx, (frameR, wCam - frameR), (0, self.wScr))
        ly = np.interp(ly, (frameRh, hCam - frameRh), (0, self.hScr))

        x2 = np.interp(x, (frameR, wCam - frameR), (0, self.wScr))
        y2 = np.interp(y, (frameRh, hCam - frameRh), (0, self.hScr))

        x3 = plocX + ((x2 - lx)/5)
        y3 = plocY + ((y2 - ly)/3)

        if x3 < 0:
            x3 = 0
        elif x3 > 1366:
            x3 = 1366

        if y3 < 0:
            y3 = 0
        elif y3 > 768:
            y3 = 768

        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        # print('clockY: ', clocY)
        self.mo.position = (self.wScr - clocX, clocY)

