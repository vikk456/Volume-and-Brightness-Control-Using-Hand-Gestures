import numpy as np
import time
import cv2
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]


barVol = 400
vol = 0
per = 0
mode = 0
total_modes = 2

pinch_start_time = None
pinch_triggered = False
hold_duration = 1


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if lmList:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[20][1], lmList[20][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        length2 = math.hypot(x3 - x1, y3 - y1)

        if length2 < 50:
            if pinch_start_time is None:
                pinch_start_time = time.time()
                pinch_triggered = False
            else:
                if not pinch_triggered and (time.time() -  pinch_start_time) > hold_duration:
                    mode = (mode + 1) % total_modes
                    pinch_triggered = True
        else:
            pinch_start_time = None
            pinch_triggered = False

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        barVol = np.interp(length, [50, 200], [400, 150])
        per = np.interp(length, [50,200], [0, 100])
        
        if mode == 0:
            vol = np.interp(length, [50, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
        elif mode == 1:
            brightness = np.interp(length, [50, 200], [0, 100])
            sbc.set_brightness(int(brightness))

        



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.rectangle(img, (50,150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(barVol)), (85, 400), (255, 0, 0), cv2.FILLED)
    if mode == 0:
        cv2.putText(img, 'Volume Control', (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif mode == 1:
        cv2.putText(img, 'Brightness Control', (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)