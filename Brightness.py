import numpy as np
import time
import cv2
import HandTrackingModule as htm
import math
import screen_brightness_control as sbc

wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)




barVol = 400
brightness = 50
per = 0


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if lmList:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        #print(length)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        
        brightness = np.interp(length, [50, 200], [0, 100])
        barVol = np.interp(length, [50, 200], [400, 150])
        per = np.interp(length, [50,200], [0, 100])
        sbc.set_brightness(int(brightness))

        



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.rectangle(img, (50,150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(barVol)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'Brightness: {int(per)}%', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)