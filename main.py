import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('PYGAME project')

x = 50
y = 50
width = 40
hight = 60
speed = 5

run = True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= speed
            if event.key == pygame.K_RIGHT:
                x += speed
            if event.key == pygame.K_UP:
                y -= speed
            if event.key == pygame.K_DOWN:
                y += speed
    pygame.draw.rect(win, (0, 255, 255), (x, y, width, hight))
    pygame.display.update()
pygame.quit()
