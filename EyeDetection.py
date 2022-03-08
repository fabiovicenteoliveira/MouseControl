# imports
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2
from PIL import Image
import numpy as np

## dlib detector: https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2

####
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def eye_aspect_ratio(eye):
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])
    c = dist.euclidean(eye[0], eye[3])
    ear = (a + b) / (2.0 * c)
    return ear


class EyeDetection:
    def __init__(self, both_eye_ar_thresh=0.24, single_eye_thresh=0.27):
        self.single_eye_thresh = single_eye_thresh
        self.both_eye_ar_thresh = both_eye_ar_thresh
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('--shape-predictor.dat')

    def convert_to_rgb(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def find_face(self, gray):
        return self.detector(gray, 0)

    def left_eye(self, shape):
        # return closed or open
        leftEye = shape[lStart:lEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        if leftEAR < self.single_eye_thresh:
            return True
        return False

    def right_eye(self, shape):
        # return closed or open
        rightEye = shape[rStart:rEnd]
        rightEAR = eye_aspect_ratio(rightEye)
        if rightEAR < self.single_eye_thresh:
            return True
        return False

    def both_eye(self, shape, img):
        # return closed or open
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        both_ear = (leftEAR + rightEAR) / 2.0

        # Draw
        """
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(img, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(img, [rightEyeHull], -1, (0, 255, 0), 1)
        for p in range(6):
            cv2.circle(img, tuple(leftEye[p]), 1, (0,0,255), -1)
            cv2.circle(img, tuple(rightEye[p]), 1, (0,0,255), -1)"""

        if both_ear < self.both_eye_ar_thresh:
            return True, img
        return False, img

    def find_iris(self, imgRGB):
        #gray = imutils.resize(imgRGB, width=650)
        gray = imgRGB
        faces = self.find_face(gray)
        if len(faces) == 0:
            return False, 'Sem faces.'
        elif len(faces) > 1:
            return False, 'Muitas faces detectadas!'
        else:
            face = faces[0]
            shape = self.predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            return True, shape

    def find_position_nose(self, shape):
        nose = shape[nStart:nEnd]
        return nose[6][0], nose[6][1]

    def find_position_look(self, img, shape):

        leftEye = shape[lStart:lEnd]
        wmin = leftEye[0][0] - 12
        wmax = leftEye[3][0] + 8
        hmin = leftEye[2][1] - 13
        hmax = leftEye[4][1] + 10

        roi = img[hmin: hmax, wmin: wmax]
        im = Image.fromarray(roi)
        im = im.resize((200, 120))
        imnp = np.asarray(im)
        roi = imnp
        cv2.imshow('Região de interesse', roi)
        rows, cols, _ = roi.shape
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Cinza', gray_roi)

        gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
        cv2.imshow('Desfoque gaussiano', gray_roi)

        _, threshold = cv2.threshold(gray_roi, 18, 255, cv2.THRESH_BINARY_INV)  # 26
        cv2.imshow('Iris', threshold)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        x, y, w, h = 0, 0, 0, 0
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)

            cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
            cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
            break
        coordsX = int(x + w/2)
        coordsY = int(y + h/2)

        cv2.imshow('Resultado', roi) # Uncomment to see eye

        return coordsX, coordsY
