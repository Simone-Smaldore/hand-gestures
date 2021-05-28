import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from subprocess import call


wCam, hCam = 1280, 720

distance_factor = 1;

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


detector = htm.HandDetector(detection_confidence=0.7)


while True:
    success, img = cap.read()

    img = detector.draw_hands_on_image(img)
    landmark_list = detector.find_position(img, 0)
    if len(landmark_list) != 0:

        #print(img.shape[1]/2)

        print(landmark_list[0])
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 20, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 20, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        volume = np.interp(length, [distance_factor * 100, distance_factor * 300], [0,100])
        volume_str = str(int(volume)) + "%"

        # TODO Prevedere una strategia migliore per il detection della mano(In questo momento prende solo le gesture
        # TODO prima parte dello schermo) magari con la face detection di mediapipe
        if(landmark_list[0][1] > img.shape[1]/2):
            print("Volume non controllato")
            continue
        # TODO verificare il funzionamento su windows e mac
        # TODO usare la libreria pyinput per simulare le shortcut da tastiera
        call(["amixer", "-D", "pulse", "sset", "Master", volume_str])
        print(volume)

        #print(length)

    cv2.imshow("Img", img)
    cv2.waitKey(1)