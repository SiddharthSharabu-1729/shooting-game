import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define game constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spicy Shooting Game")

# Load game assets
background_img = pygame.image.load("background.png").convert()
player_img = pygame.image.load("player.png").convert_alpha()
enemy_img = pygame.image.load("enemy.png").convert_alpha()
bullet_img = pygame.image.load("bullet.png").convert_alpha()
explosion_imgs = [pygame.transform.scale(pygame.image.load("explosion1.png").convert_alpha(),(50,50)),
                  pygame.transform.scale(pygame.image.load("explosion2.png").convert_alpha(),(50,50)),
                  pygame.transform.scale(pygame.image.load("explosion3.png").convert_alpha(),(50,50))]

# Resize game assets
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 30))

# Game fonts
font_name = pygame.font.match_font("arial")

# Game sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Game variables
score = 0
level = 1
explosion_img = pygame.image.load('explosion1.png').convert_alpha()

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_imgs):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_imgs[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Function to display text on the screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Function to show game over screen
def show_game_over_screen():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "Spicy Shooting Game", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, Space to shoot", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any key to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                waiting = False

# Function to display game over screen
def show_game_over_screen():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "Game Over", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Score: " + str(score), 32, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press R to play again", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    waiting = False

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create enemy objects
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()

    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        explosion_sound.play()
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for player-enemy collision
    if pygame.sprite.spritecollide(player, enemies, False):
        game_over = True

    # Draw objects on the screen
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, "Score: " + str(score), 18, WIDTH / 2, 10)
    draw_text(screen, "Level: " + str(level), 18, WIDTH - 80, 10)

    if game_over:
        show_game_over_screen()
        level = 1
        score = 0
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for _ in range(8):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        game_over = False

    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
