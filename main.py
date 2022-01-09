import pygame
import os


pygame.init()

win = pygame.display.set_mode((720, 390))
pygame.display.set_caption("First Game")

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


walkRight = [load_image('R1.png'), load_image('R2.png'), load_image('R3.png'),
             load_image('R4.png'), load_image('R5.png'), load_image('R6.png'),
            load_image('R7.png'), load_image('R8.png'), load_image('R9.png')]
walkLeft = [load_image('L1.png'), load_image('L2.png'), load_image('L3.png'),
            load_image('L4.png'), load_image('L5.png'), load_image('L6.png'),
            load_image('L7.png'), load_image('L8.png'), load_image('L9.png')]

bg = pygame.transform.scale(load_image('fon.png'), (720, 390))
char = load_image('standing.png')
char = pygame.transform.scale(char, (120, 200))


x = 50
y = 94
width = 40
height = 60
vel = 5

clock = pygame.time.Clock()

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0


def redrawGameWindow():
    global walkCount

    win.blit(bg, (0, 0))
    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount // 3], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount // 3], (x, y))
        walkCount += 1
    else:
        win.blit(char, (x, y))
        walkCount = 0

    pygame.display.update()


run = True

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False

    elif keys[pygame.K_RIGHT] and x < 500 - vel - width:
        x += vel
        left = False
        right = True

    else:
        left = False
        right = False
        walkCount = 0

    if not (isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
            left = False
            right = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            jumpCount = 10
            isJump = False

    redrawGameWindow()

pygame.quit()