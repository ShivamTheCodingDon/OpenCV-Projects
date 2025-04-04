import pygame,sys

pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

dir = "D:/python projects/face rec/pygame poject/Pygame-Images\Game"

walkRight = [pygame.image.load(dir + '/R1.png'), pygame.image.load(dir +'/R2.png'), pygame.image.load(dir +'/R3.png'), pygame.image.load(dir +'/R4.png'), pygame.image.load(dir +'/R5.png'), pygame.image.load(dir +'/R6.png'), pygame.image.load(dir +'/R7.png'), pygame.image.load(dir +'/R8.png'), pygame.image.load(dir +'/R9.png')]
walkLeft = [pygame.image.load(dir +'/L1.png'), pygame.image.load(dir +'/L2.png'), pygame.image.load(dir +'/L3.png'), pygame.image.load(dir +'/L4.png'), pygame.image.load(dir +'/L5.png'), pygame.image.load(dir +'/L6.png'), pygame.image.load(dir +'/L7.png'), pygame.image.load(dir +'/L8.png'), pygame.image.load(dir +'/L9.png')]
bg = pygame.image.load(dir +'/bg.jpg')
char = pygame.image.load(dir +'/standing.png')

clock = pygame.time.Clock()

x = 50
y = 400
width = 64
height = 64
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0


def redrawGameWindow():
    global walkCount
    # win.fill((0,0,0))
    win.blit(bg, (0,0))
    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x,y))

    pygame.display.update()

run = True
while run:
    # pygame.time.delay(50)
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        right = False
        left = True
    elif keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not(isJump):
        # if keys[pygame.K_UP] and y > vel:
        #     y -= vel
        # if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #     y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    redrawGameWindow()

pygame.quit()