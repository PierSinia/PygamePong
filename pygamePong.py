import pygame
from os import path
import time

WIDTH = 800
HEIGHT = 600
FPS = 60

scoreA = 0
scoreB = 0

# Scherm maken
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # maakt een scherm
pygame.display.set_caption("Pong!") # maakt een naam voor het scherm
clock = pygame.time.Clock() # houdt de snelheid bij en de juiste FPS

# de kleuren

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

paddle_size = (10, 130)

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
score_sound = pygame.mixer.Sound(path.join(snd_dir, 'score.wav'))

background = pygame.image.load(path.join(img_dir, "background2.png")).convert()

class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20)) # Hoe een sprite eruit ziet
        self.image.fill(WHITE)
        self.rect = self.image.get_rect() # kijkt wat de rect van de image is
        self.rect.center = (WIDTH -50, HEIGHT / 2)
        self.y_speed = 8.7
        self.x_speed = 10

    def update(self):
        global scoreA
        global scoreB
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.bottom > HEIGHT:
            self.y_speed *= -1
            hit_sound.play()


        if self.rect.right > WIDTH:
            scoreA += 1
            score_sound.play()
            self.rect.center = (WIDTH-100, HEIGHT /2)
            self.y_speed *= -1
            self.x_speed *= -1
            hit_sound.play()


        if self.rect.top < 0:
            self.y_speed *= -1
            hit_sound.play()

        if self.rect.left < 0:
            scoreB += 1
            score_sound.play()
            self.rect.center = (100, HEIGHT / 2)
            hit_sound.play()
            self.y_speed *= -1
            self.x_speed *= -1


        hit_paddleA = pygame.sprite.collide_rect(paddlea, ball)
        if hit_paddleA:
            self.x_speed *= -1
            hit_sound.play()


        hit_paddleB = pygame.sprite.collide_rect(paddleb, ball)
        if hit_paddleB:
            self.x_speed *= -1
            hit_sound.play()


class paddleA(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(paddle_size ) # Hoe een sprite eruit ziet
        self.image.fill(WHITE)
        self.rect = self.image.get_rect() # kijkt wat de rect van de image is
        self.rect.center = (0 + 50, HEIGHT / 2)

    def update(self):
        self.speedy = 0
        key = pygame.key.get_pressed() # lijst die alle toetsen aangeeft waar op gedrukt word
        if key[pygame.K_s]:
            self.speedy += 6
        if key[pygame.K_w]:
            self.speedy -= 6

        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

class paddleB(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(paddle_size ) # Hoe een sprite eruit ziet
        self.image.fill(WHITE)
        self.rect = self.image.get_rect() # kijkt wat de rect van de image is
        self.rect.center = (WIDTH - 50, HEIGHT / 2)


    def update(self):
        self.speedy = 0
        key = pygame.key.get_pressed() # lijst die alle toetsen aangeeft waar op gedrukt word
        if key[pygame.K_DOWN]:
            self.speedy += 6
        if key[pygame.K_UP]:
            self.speedy -= 6



        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

all_sprites = pygame.sprite.Group() # collectie van sprites
ball = ball()
paddlea = paddleA()
paddleb = paddleB()
all_sprites.add(paddlea, paddleb, ball)

# Game loop
running = True
while running:


    # keep loop running at the right speed
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update() # Elke sprite updaten

    # Draw / render
    backgroundrect = background.get_rect() # vraag afmetingen van het bordplaatje op
    screen.blit(background, backgroundrect) # teken het bord
    all_sprites.draw(screen)
    draw_text(screen, str(scoreA), 55, WIDTH / 4, 10 )
    draw_text(screen, str(scoreB), 55, 600, 10)

    if scoreA >= 10:
        screen.fill(BLACK)
        draw_text(screen, "Player A wins!", 60, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press escape to exit the game", 30, WIDTH /2, HEIGHT -130)
        ball.kill()

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            running = False

    if scoreB >= 10:
        screen.fill(BLACK)
        draw_text(screen, "Player B wins!", 60, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press escape to exit the game", 30, WIDTH /2, HEIGHT -130)
        key = pygame.key.get_pressed()
        ball.kill()

        if key[pygame.K_ESCAPE]:
            running = False

    # Na het tekenen van alles update het scherm
    pygame.display.flip()

pygame.quit()
