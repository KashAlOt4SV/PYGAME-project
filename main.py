import pygame
import os

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('PYGAME project')

x = 50
y = 50
width = 40
hight = 60
speed = 5
coordinates = x, y

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

class Creature(pygame.sprite.Sprite):
    image = load_image("creature.png")


    def __init__(self, group):
        super().__init__(group)
        self.image = Creature.image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

run = True
while run:
    all_sprites = pygame.sprite.Group()
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                win.fill(pygame.Color("black"))
                coordinates = coordinates[0], coordinates[1] - 10
                Creature(all_sprites)
            elif event.key == pygame.K_DOWN:
                win.fill(pygame.Color("black"))
                coordinates = coordinates[0], coordinates[1] + 10
                Creature(all_sprites)
            elif event.key == pygame.K_RIGHT:
                win.fill(pygame.Color("black"))
                coordinates = coordinates[0] + 10, coordinates[1]
                Creature(all_sprites)
            elif event.key == pygame.K_LEFT:
                win.fill(pygame.Color("black"))
                coordinates = coordinates[0] - 10, coordinates[1]
                Creature(all_sprites)
    # pygame.draw.rect(win, (0, 255, 255), (x, y, width, hight))
    Creature(all_sprites)
    all_sprites.draw(win)
    all_sprites.update()
    all_sprites = pygame.sprite.Group().empty()
    pygame.display.flip()
    clock.tick(90)
    pygame.display.update()

pygame.quit()
