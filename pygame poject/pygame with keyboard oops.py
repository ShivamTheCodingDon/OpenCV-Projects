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

man = player(300, 410, 64, 64)
bullets = []
run = True
while run:
    # pygame.time.delay(50)
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0: # bullet have property of x
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0, 0, 0), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.right = False
        man.left = True
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
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
        if keys[pygame.K_UP]:
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

pygame.quit()