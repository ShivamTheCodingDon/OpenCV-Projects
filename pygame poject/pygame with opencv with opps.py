import pygame,sys
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

dir = "Pygame-Images\Game"

walkRight = [pygame.image.load(dir + '/R1.png'), pygame.image.load(dir +'/R2.png'), pygame.image.load(dir +'/R3.png'), pygame.image.load(dir +'/R4.png'), pygame.image.load(dir +'/R5.png'), pygame.image.load(dir +'/R6.png'), pygame.image.load(dir +'/R7.png'), pygame.image.load(dir +'/R8.png'), pygame.image.load(dir +'/R9.png')]
walkLeft = [pygame.image.load(dir +'/L1.png'), pygame.image.load(dir +'/L2.png'), pygame.image.load(dir +'/L3.png'), pygame.image.load(dir +'/L4.png'), pygame.image.load(dir +'/L5.png'), pygame.image.load(dir +'/L6.png'), pygame.image.load(dir +'/L7.png'), pygame.image.load(dir +'/L8.png'), pygame.image.load(dir +'/L9.png')]
bg = pygame.image.load(dir +'/bg.jpg')
char = pygame.image.load(dir +'/standing.png')

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            # win.blit(char, (self.x,self.y))
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    

def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

run = True

man = player(300, 410, 64, 64)
bullets = []

while run:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    # pygame.time.delay(50)


    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if hands:

        for bullet in bullets:
            if bullet.x < 500 and bullet.x > 0: # bullet have property of x
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        if len(hands) == 2:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmarks points
            bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
            centerPoint1 = hand1["center"]  # center of the hand cx,cy
            handType1 = hand1["type"]  # Hand Type Left or Right

            fingers1 = detector.fingersUp(hand1)
            # print(fingers1)
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right
            fingers2 = detector.fingersUp(hand2)

            print("handType1:",handType1)

            if handType1 == "Left":
                if  sum(fingers1) == 5:
                    if man.left:
                        facing = -1
                    else:
                        facing = 1
                    if len(bullets) < 5:
                        bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0, 0, 0), facing))
            if handType2 == "Right":
                if fingers2[0] == 1 and fingers2[2] == 0 and man.x > man.vel:
                    man.x -= man.vel
                    man.right = False
                    man.left = True
                    man.standing = False
                elif fingers2[4] == 1 and  fingers2[2] == 0 and man.x < 500 - man.width - man.vel:
                    man.x += man.vel
                    man.right = True
                    man.left = False
                    man.standing = False
                else:
                    # man.right = False
                    # man.left = False
                    man.standing = True
                    man.walkCount = 0

                if not(man.isJump):
                    if fingers2[1] == 1 and fingers2[2] == 1 and fingers2[3] == 0:
                        man.isJump = True
                        man.right = False
                        man.left = False
                        man.walkCount = 0
                else:
                    if man.jumpCount >= -10:
                        neg = 1
                        if man.jumpCount < 0:
                            neg = -1
                        man.y -= (man.jumpCount ** 2) * 0.5 * neg
                        man.jumpCount -= 1
                    else:
                        man.isJump = False
                        man.jumpCount = 10

                redrawGameWindow()

    
    cv2.imshow("Image", img)
    cv2.waitKey(1)