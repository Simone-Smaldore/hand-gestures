import cv2
import numpy as np
import HandTrackingModule as htm
import math
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()
wCam, hCam = 1280, 720
#Setto il fattore di distanza che va a considerare
distance_factor = 1;
#Setto la sensibilita che avra lo zoom
sensibility_factor = 5;

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detection_confidence=0.7)

frame_rate = 4
prev = 0

while True:
    time_elapsed = time.time() - prev
    success, img = cap.read()

    img = detector.draw_hands_on_image(img)
    landmark_list = detector.find_position(img, 0)

    if time_elapsed > 1./frame_rate:
        prev = time.time()
        if len(landmark_list) != 0:
            print(landmark_list[8])
            x1, y1 = landmark_list[4][1], landmark_list[4][2]
            x2, y2 = landmark_list[8][1], landmark_list[8][2]

            cv2.circle(img, (x1, y1), 20, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 20, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            length = math.hypot(x2 - x1, y2 - y1)


            # TODO Prevedere una strategia migliore per il detection della mano(In questo momento prende solo le gesture
            # TODO prima parte dello schermo) magari con la face detection di mediapipe
            if(landmark_list[0][1] > img.shape[1]/2):
                print("Mano non controllata")
                continue
            # TODO verificare il funzionamento su windows e mac
            # TODO usare la libreria pyinput per simulare le shortcut da tastiera
            dis = np.interp(length, [distance_factor * 100, distance_factor * 300], [0, 100])

            if dis > 100 - sensibility_factor:
                keyboard.press(Key.ctrl.value)
                keyboard.press('+')
                keyboard.release('+')
                keyboard.release(Key.ctrl.value)
            if(dis < 0 + sensibility_factor):
                keyboard.press(Key.ctrl.value)
                keyboard.press('-')
                keyboard.release('-')
                keyboard.release(Key.ctrl.value)


    cv2.imshow("Img", img)
    cv2.waitKey(1)