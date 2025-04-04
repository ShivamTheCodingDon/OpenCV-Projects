import pygame,sys
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



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
        print(fingers1)


        if fingers1[0] == 1 and fingers1[2] == 0 and x > vel:
                x -= vel
        if fingers1[4] == 1 and  fingers1[2] == 0 and fingers1[3] == 0 and x < 500 - width - vel:
                x += vel
        if fingers1[1] == 1 and fingers1[2] == 1 and fingers1[3] == 0 and y > vel:
                y -= vel
        if fingers1[3] == 1 and fingers1[0] == 0 and y < 500 - height - vel:
                y += vel

        win.fill((0,0,0))
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()



    cv2.imshow("Image", img)
    cv2.waitKey(1)