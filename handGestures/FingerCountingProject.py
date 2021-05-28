import cv2
import time
import os
#import HandTrackingModule as hm
#TO DO Completare prima il progetto di Hand Tracking

wCam, hCam = 1640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
myList.sort()
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}') # magia della formattazione f
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0
while True:
    success, img = cap.read()

    img[0:200, 0:200] = cv2.resize(overlayList[5], (200, 200))  #slicing per mostrare l'immagine delle dita


    cv2.imshow("Image", img)
    cv2.waitKey(1)




