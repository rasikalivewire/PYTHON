import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Pro")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,150,255)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

score = 0

# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.rect = pygame.Rect(375, 500, 50, 50)
        self.speed = 6
        self.health = 100

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.clamp_ip(screen.get_rect())

    def draw(self):
        pygame.draw.polygon(screen, BLUE,
            [(self.rect.centerx,self.rect.top),
             (self.rect.left,self.rect.bottom),
             (self.rect.right,self.rect.bottom)])

# ---------------- BULLET ----------------
class Bullet:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,5,15)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# ---------------- ENEMY ----------------
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0,750),
            -50,
            40,
            40
        )
        self.speed = random.randint(2,5)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# ---------------- PARTICLE ----------------
class Particle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.life = 20
        self.dx = random.randint(-4,4)
        self.dy = random.randint(-4,4)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen,
                           (255,200,0),
                           (int(self.x),int(self.y)),
                           3)

# ---------------- GAME ----------------
player = Player()

bullets = []
enemies = []
particles = []

enemy_timer = 0
shoot_delay = 250
last_shot = 0

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    now = pygame.time.get_ticks()

    if keys[pygame.K_SPACE]:
        if now - last_shot > shoot_delay:
            bullets.append(
                Bullet(
                    player.rect.centerx,
                    player.rect.top
                )
            )
            last_shot = now

    player.move()

    enemy_timer += 1

    if enemy_timer > 30:
        enemies.append(Enemy())
        enemy_timer = 0

    for bullet in bullets[:]:
        bullet.update()

        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    for enemy in enemies[:]:
        enemy.update()

        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)
            player.health -= 10

    for enemy in enemies[:]:

        for bullet in bullets[:]:

            if enemy.rect.colliderect(bullet.rect):

                score += 10

                for _ in range(20):
                    particles.append(
                        Particle(
                            enemy.rect.centerx,
                            enemy.rect.centery
                        )
                    )

                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    for particle in particles[:]:
        particle.update()

        if particle.life <= 0:
            particles.remove(particle)

    screen.fill(BLACK)

    player.draw()

    for bullet in bullets:
        bullet.draw()

    for enemy in enemies:
        enemy.draw()

    for particle in particles:
        particle.draw()

    pygame.draw.rect(screen, RED,
                     (10,10,200,20))

    pygame.draw.rect(screen, GREEN,
                     (10,10,
                      player.health*2,
                      20))

    score_text = font.render(
        f"Score : {score}",
        True,
        WHITE
    )

    screen.blit(score_text,(10,40))

    if player.health <= 0:
        game_over = font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over,
            (300,250)
        )

    pygame.display.update()

pygame.quit()