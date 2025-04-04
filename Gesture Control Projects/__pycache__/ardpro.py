import cv2
from time import sleep
import pyfirmata
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np

# cap = cv2.VideoCapture("http://192.168.135.241:4747/video")
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

pTime = 0

pin = 9
buzz_pin = 5
led_pin = 12
port = "COM14"
board = pyfirmata.ArduinoNano(port)

LED = board.digital[pin]
LED.mode = pyfirmata.PWM
BUZZ = board.digital[buzz_pin]
BUZZ.mode = pyfirmata.PWM 


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

        
        fingers1 = detector.fingersUp(hand1)
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            handType2 = hand2["type"]
        
            if handType1 == "Right":
                if fingers1[2] == 0 and fingers1[3] == 0:
                    board.digital[pin].write(0)

                if fingers1[3] == 0 and fingers1[2] == 1:
                    BUZZ.write(0)
        
                if fingers1[4] == 0:
                    board.digital[led_pin].write(fingers1[3])
                    if fingers1[2] == 0:
                        cv2.rectangle(img, (440, 418), (630, 465), (100, 0, 100), 4)
                        cv2.rectangle(img, (440, 418), (630, 465), (0, 220, 0), cv2.FILLED)
                        cv2.putText(img, " Led On ", (450, 448), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 50, 125), 3)
                    

                
            
            if handType2 == "Left" and fingers1[1] == 1 and fingers1[3] == 0:
                length, info, img = detector.findDistance(lmList2[4][0:2], lmList2[8][0:2], img) # with draw
                lendis = np.interp(length, [20, 135], [0, 1])
                if lendis == 0:
                    if fingers1[2] == 0:
                        LED.write(0)
                    BUZZ.write(0)

                elif fingers1[1] == 1 and fingers1[2] == 0:
                    LED.write(lendis)

                    cv2.rectangle(img, (440, 418), (630, 465), (100, 0, 100), 4)
                    cv2.rectangle(img, (440, 418), (630, 465), (0, 220, 0), cv2.FILLED)
                    cv2.putText(img, " Led On ", (450, 448), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 50, 125), 3)
                    
                elif fingers1[2] == 1:
                    BUZZ.write(lendis)
                    cv2.rectangle(img, (440, 418), (630, 465), (100, 0, 100), 4)
                    cv2.rectangle(img, (440, 418), (630, 465), (0, 220, 0), cv2.FILLED)
                    cv2.putText(img, "buzzer On", (450, 448), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 50, 125), 3)
                    

                dis = np.interp(length, [20, 115], [0, 1])
                rou = round(dis, 2)
                pers = int(rou * 100)
                var_bar = np.interp(rou, [0, 1], [0, 250])

                cv2.rectangle(img, (50, 150), (85, 400), (220, 0, 100), 3)
                cv2.rectangle(img, (50, 400), (85, 400 - int(var_bar)), (0, 200, 0), cv2.FILLED)
                cv2.rectangle(img, (30, 428), (150, 470), (0, 220, 0), cv2.FILLED)
                cv2.rectangle(img, (30, 428), (150, 470), (100, 0, 100), 3)
                cv2.putText(img, f'{pers} %', (40, 458), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 50, 125), 2)
                    

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.rectangle(img, (470, 10), (630, 50), (100, 0, 100), 3)
        cv2.rectangle(img, (470, 10), (630, 50), (0, 220, 0), cv2.FILLED)
        cv2.putText(img, f'FPS: {str(int(fps))}', (490, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 50, 125), 2)
        

        
    cv2.imshow("Image", img)
    cv2.waitKey(1)