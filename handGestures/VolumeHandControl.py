import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detection_confidence=0.7)

while True:
    success, img = cap.read()

    img = detector.draw_hands_on_image(img)
    landmark_list = detector.find_position(img, 0)
    if len(landmark_list) != 0:

        #print(landmark_list[4], landmark_list[12])
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[12][1], landmark_list[12][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 20, (255, 0, 0))
        cv2.circle(img, (x2, y2), 20, (255, 0, 0))
        cv2.circle(img, (cx, cy), 20, (255, 0, 0))
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

    cv2.imshow("Img", img)
    cv2.waitKey(1)