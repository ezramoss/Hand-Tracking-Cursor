#Python Version 3.9
#PyAutoGUI Version 0.9.53
#opencv-python Version 4.5.3.56
#mediapipe Version 0.8.6

import math
import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)

screenSize = pyautogui.size()
camWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
camHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
pointOne = (int(0 + (camWidth / 10)), int(0 + (camHeight / 20)))
pointTwo = (int(camWidth - (camWidth/10)), int(camHeight - (camHeight/3)))
newCamWidth = pointTwo[0] - pointOne[0]
newCamHeight = pointTwo[1] - pointOne[1]

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

currentTime = 0
pastTime = 0

def rescale(range1, range2, value):
    return (value * range2) / range1

while True:
    success, image = cap.read()
    flipped = cv2.flip(image, 1)
    imageColor = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = hands.process(imageColor)

    if results.multi_hand_landmarks:
        for MHL in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(flipped, MHL, mpHands.HAND_CONNECTIONS)

            h, w, c = image.shape
            indexX, indexY = int(MHL.landmark[8].x * w), int(MHL.landmark[8].y * h)
            middleX, middleY = int(MHL.landmark[12].x * w), int(MHL.landmark[12].y * h)
            thumbX, thumbY = int(MHL.landmark[4].x * w), int(MHL.landmark[4].y * h)

            cv2.circle(flipped, (indexX, indexY), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(flipped, (middleX, middleY), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(flipped, (thumbX, thumbY), 10, (0, 0, 255), cv2.FILLED)

            #Conditions for movement and clicking

            rClickDistance = math.dist([middleX, middleY], [indexX, indexY])
            lClickDistance = math.dist([indexX, indexY], [thumbY, thumbY])

            mouseX = rescale(newCamWidth, screenSize[0], middleX-pointOne[0])
            mouseY = rescale(newCamHeight, screenSize[1], middleY-pointOne[1])
            if(middleX > pointOne[0] and middleX < pointTwo[0] and middleY > pointOne[1] and middleY < pointTwo[1]):
                pyautogui.moveTo(mouseX, mouseY, _pause=False)
            if rClickDistance < 30:
                pyautogui.click()
            if lClickDistance < 25:
                pyautogui.rightClick()

    currentTime = time.time()
    fps = 1/(currentTime-pastTime)
    pastTime = currentTime

    cv2.putText(flipped,str("FPS: " + str(int(fps))),(10,int(camHeight-50)), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
    cv2.rectangle(flipped, pointOne, pointTwo, (255, 0, 255), 5, cv2.FILLED)

    cv2.imshow("Image", flipped)
    cv2.waitKey(1)