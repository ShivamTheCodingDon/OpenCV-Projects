import cv2
import pyfirmata
from cvzone.SerialModule import SerialObject
from time import sleep
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

#arduino = SerialObject("com7")

pin = 6
port = "COM7"
board = pyfirmata.Arduino(port)

LED = board.digital[pin]
LED.mode = pyfirmata.PWM

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
        
            # if handType1 == "Right":
            #     arduino.sendData(fingers1)

            length, info, img = detector.findDistance(lmList2[4][0:2], lmList2[8][0:2], img) # with draw
            lendis = int(length)
            if lendis <= 15 :
                LED.write(0)
            for i in range(15, lendis, 25):
                LED.write(i/125)
                if fingers1[4] == 1:
                    LED.write(i/125)
                    break
                print(i)
            
            



        #print(fingers1)
        # print(handType1)
        # hT1 = len(handType1)
        # print(hT1)
        #print(lmList1[8][0:2])
        #length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img) # with draw
        #length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw
        # length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[4][0:2], img)
        # print(length)
        # print(info)
        # print(img)

        
    cv2.imshow("Image", img)
    cv2.waitKey(1)
