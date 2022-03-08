import time

import cv2.cv2


class Controls:
    def __init__(self, press, ca=[0, 0]):
        self.press = press
        self.last_coords_finger = ca

    def iris_control(self, img, o, t, iris_detector, window, m):
        imgRGB = iris_detector.convert_to_rgb(img)
        res_find_iris, shape = iris_detector.find_iris(imgRGB)

        if not res_find_iris:
            # In this case shape is msg
            window.printf_msg(shape)
            return False, t, img
        else:
            res_open_closed = iris_detector.left_eye(shape)
            if res_open_closed:
                if not t.last_left:
                    t.ts_left = time.time()
                t.last_left = True
            else:
                t.last_left = False
                t.left_repeat = True

            res_open_closed = iris_detector.right_eye(shape)
            if res_open_closed:
                if not t.last_right:
                    t.ts_right = time.time()
                t.last_right = True
            else:
                t.last_right = False

            res_open_closed, img = iris_detector.both_eye(shape, img)
            if res_open_closed:
                if not t.last_both:
                    t.ts_both = time.time()
                t.last_both = True
            else:
                t.last_both = False

            if o.mouse and o.type_move == 1:
                # Move using nose coords
                x, y = iris_detector.find_position_nose(shape)
                cv2.circle(img, (x, y), 4, (255, 0, 0), cv2.FILLED)
                m.move_mouse(x, y, img)

            if o.mouse and o.type_move == 7:
                # Move using the direction of eye
                x, y = iris_detector.find_position_look(img, shape)
                m.move_mouse_eye_direction(x, y, smoothening=15)

            if o.mouse and o.type_move == 8:
                # Move using eye and finger
                x, y = iris_detector.find_position_look(img, shape)
                m.move_mouse_eye_direction(x, y, smoothening=15)

            tend = time.time()

            if o.keyboard and t.last_both:
                # Open keyboard after 3s
                duration = tend - t.ts_both
                if duration > 3:
                    m.open_keyboard()
                    t.last_both = False
            if o.left_click and t.last_left:
                # Left click after 1.5s or 3s
                duration = tend-t.ts_left
                if duration > 3:
                    m.click('TWO')
                    t.last_left = False
                elif duration > 1.5 and t.left_repeat:
                    m.click('LEFT')
                    t.left_repeat = False

            if o.right_click and t.last_right:
                # Right click with right eye
                duration = tend-t.ts_both
                if duration > 1.5:
                    m.click('RIGHT')
                    t.last_right = False

        return True, t, img

    def arm_control(self, img, t, o, m, arm, window):
        imgRGB = arm.convert_to_rgb(img)
        res_arm = arm.find_arm(imgRGB)
        tend = time.time()

        if res_arm and o.gestures:
            # Two clicks and drag with finger
            lmList, img = arm.find_all_positions(imgRGB)

            ba = lmList[5][2]
            yf = lmList[8][2]
            ys = lmList[12][2]
            yt = lmList[16][2]
            res_two_three = arm.two_or_three_fingers(ba, yf, ys, yt)

            if res_two_three == "TWO":
                # two fingers up -> two clicks
                if not t.last_two_up:
                    t.ts_two_up = time.time()
                    t.last_two_up = True
                elif tend - t.ts_two_up > 1.5:
                    m.click('TWO')
                    t.last_two_up = False
            elif res_two_three == "THREE":
                # 3 fingers up -> drag
                if not t.last_three_up:
                    t.ts_three_up = time.time()
                    t.last_three_up = True
                elif (tend - t.ts_three_up) > 1.5 and not self.press:
                    self.press = True
                    m.drag_press()

            elif res_two_three == "DOWN" and self.press:
                m.drag_release()
                t.last_three_up = False
                self.press = False

        if res_arm and o.scroll:
            # Scroll
            lmList, img = arm.find_all_positions(imgRGB)
            y1 = lmList[20][2]
            y2 = lmList[17][2]
            res_little_finger = arm.finger_up_or_down(y1, y2)
            if res_little_finger == "UP":
                # scroll up
                t.last_down = False
                if not t.last_up:
                    t.last_up = True
                    t.ts_up = time.time()
                else:
                    duration = tend - t.ts_up
                    if duration > 2:
                        m.scroll_up()
                        t.last_up = False
            elif res_little_finger == "DOWN":
                t.last_up = False
                if not t.last_down:
                    t.last_down = True
                    t.ts_down = time.time()
                else:
                    duration = tend - t.ts_down
                    if duration > 2:
                        m.scroll_down()
                        t.last_down = False
            else:
                t.last_up = False
                t.last_down = False

        if res_arm and o.palm_direction:
            # Palm click
            lmList, img = arm.find_all_positions(imgRGB)
            res_palm = arm.click_arm(lmList[1][2], lmList[0][2])
            # print(res_palm)
            if res_palm == "LEFT":
                t.last_hand_reverse = False
                if not t.last_hand_hor:
                    t.last_hand_hor = True
                    t.ts_hand_hor = time.time()
                else:
                    duration = tend - t.ts_hand_hor
                    if duration > 1.5 and t.left_repeat_palm:
                        m.click(res_palm)
                        t.left_repeat_palm = False
                    elif duration > 3:
                        m.click("TWO")
                        t.last_hand_hor = False
            elif res_palm == "RIGHT":
                t.last_hand_hor = False
                t.left_repeat_palm = True
                if not t.last_hand_reverse:
                    t.last_hand_reverse = True
                    t.ts_hand_reverse = time.time()
                else:
                    duration = tend - t.ts_hand_reverse
                    if duration > 1.5:
                        m.click(res_palm)
                        t.last_hand_reverse = False
            else:
                t.last_hand_hor = False
                t.last_hand_reverse = False
                t.left_repeat_palm = True

        if res_arm and o.mouse and o.type_move != 1 and o.type_move != 7:
            lmList, img = arm.find_all_positions(imgRGB)

            if o.type_move == 0:
                # Move using palm
                x1 = lmList[0][1]
                y1 = lmList[0][2]
                m.move_mouse(x1, y1, img)

            if o.type_move == 2:
                # Move using finger
                x1 = lmList[8][1]
                y1 = lmList[8][2]
                m.move_mouse(x1, y1, img)

            if o.type_move == 3:
                # Move using finger
                x1 = lmList[4][1]
                y1 = lmList[4][2]
                m.move_mouse(x1, y1, img)

            if o.type_move == 4:
                # Move using finger
                x1 = lmList[12][1]
                y1 = lmList[12][2]
                m.move_mouse(x1, y1, img)

            if o.type_move == 5:
                # Move using finger
                x1 = lmList[16][1]
                y1 = lmList[16][2]
                m.move_mouse(x1, y1, img)

            if o.type_move == 6:
                # Move using finger
                x1 = lmList[20][1]
                y1 = lmList[20][2]
                m.move_mouse(x1, y1, img)

            if o.type_move == 8:
                xfinger = lmList[8][1]
                yfinger = lmList[8][2]
                # change xfinger and yfinger to coodrs close eye coodrs
                m.move_finger_eye(img, xfinger, yfinger, self.last_coords_finger[0], self.last_coords_finger[1])

                # print('Xfinger: ', int(a), ' Yfinger: ', int(b))
                self.last_coords_finger = (xfinger, yfinger)

        if not res_arm:
            window.printf_msg("Braço não detectado!")
            return False, t, img

        return True, t, img
