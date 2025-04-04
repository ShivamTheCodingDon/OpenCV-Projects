import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np
import time
import webbrowser

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

c = 0
chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

def readImg():
    path = 'images'
    images = []
    myList = os.listdir(path)
    # print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        img_shape = curImg.shape
        imgS = cv2.resize(curImg, (int(img_shape[0]*.75), int(img_shape[1]*.75)), interpolation= cv2.INTER_LINEAR)
        images.append(imgS)
    
    return images


while True:
    success, img = cap.read()
    # hands, img = detector.findHands(img)  # With Draw
    hands, img = detector.findHands(img, draw=False)  # No Draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        fingers1 = detector.fingersUp(hand1)

        length, info, _ = detector.findDistance(lmList1[4][0:2], lmList1[7][0:2])
        dis = np.interp(length, [40,100], [0, 10])

        # if fingers1[0] == 1:
        #     x = lmList1[4]
        #     print(int(x[0]))
        # else:
        #     y = lmList1[4]
        #     print(int(y[0]))

        try:
            if fingers1[2] == 0 :
                if int(dis) == 0:
                    c += 1
                cv2.imshow("img", readImg()[c-1])
                cv2.waitKey(1000)
                #print(sum(fingers1[:3]))

            if sum(fingers1[:3]) == 0:
                if c == 1:
                    webbrowser.get(chrome).open_new("https://www.youtube.com/watch?v=60ItHLz5WEA")
                    cv2.waitKey(1000)
                if c == 3:
                    webbrowser.get(chrome).open_new("https://www.youtube.com/watch?v=pS5d77DQHOI")
                    cv2.waitKey(1000) 
                if c == 2:
                    webbrowser.get(chrome).open_new("https://www.youtube.com/watch?v=BddP6PYo2gs")
                    cv2.waitKey(1000) 

                if c == 4:
                    webbrowser.get(chrome).open_new("https://zoro.to/")
                    cv2.waitKey(1000)
                
        
        except IndexError as ie:
            c = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)
