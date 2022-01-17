import pygame
from pygame.locals import *
import sys
import random
import time
import os

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

pygame.mixer.music.load('soundtrack.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

sound1 = pygame.mixer.Sound('pryshok.mp3')

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


bg = pygame.transform.scale(load_image('fon_dodle.png'), (WIDTH, HEIGHT))
background_rect = bg.get_rect()


def start_screen():
    fon = pygame.transform.scale(load_image('Start_Fon.png'), (WIDTH, HEIGHT))
    displaysurface.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # (148, 217), (267, 271)
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 217 <= \
                    pygame.mouse.get_pos()[1] <= 271:
                return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 297 <= \
                    pygame.mouse.get_pos()[1] <= 353:
                print(1)

        pygame.display.flip()
        FramePerSec.tick(FPS)


class Player(pygame.sprite.Sprite):

    score = 0

    def __init__(self):
        super().__init__()
        self.char = load_image('character_2.png')
        self.surf = pygame.transform.scale(self.char, (50, 50))
        self.surf.blit(self.char, (0, 0))
        self.rect = self.surf.get_rect()
        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        global score

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        global score
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        Player.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


font_name = pygame.font.match_font('arial')
WHITE = (255, 255, 255)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    displaysurface.blit(bg, background_rect)
    draw_text(displaysurface, "Провал!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(displaysurface, "Ваш счёт составил: {}".format(Player.score), 18,
              WIDTH / 2, HEIGHT / 2)
    draw_text(displaysurface, "Начать заново", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True

    while waiting:
        FramePerSec.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 297 <= \
                    pygame.mouse.get_pos()[1] <= 353:
                print(1)

            pygame.display.flip()
            FramePerSec.tick(FPS)



class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("platform.png")
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 60),
                                               random.randint(0, HEIGHT - 30)))
        self.speed = random.randint(-1, 2)

        self.point = True
        self.moving = True

    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH


def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False


def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = platform()
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)


PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((100, 100, 100))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

PT1.moving = False
PT1.point = False  ##

for x in range(random.randint(4, 5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

start_screen()

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
                sound1.play()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            show_go_screen()
            pygame.display.update()
            time.sleep(1)

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    plat_gen()
    displaysurface.blit(bg, (0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123, 255, 0))
    displaysurface.blit(g, (WIDTH / 2, 10))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
