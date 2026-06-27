import pygame
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()

# Player
player_width = 50
player_height = 40
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 6

# Bullets
bullets = []
bullet_speed = 8

# Enemies
enemies = []
enemy_speed = 3
spawn_timer = 0

score = 0
font = pygame.font.SysFont(None, 36)

running = True

while running:
    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_width//2 - 2, player_y])

    # Movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(WIDTH - player_width, player_x))

    # Bullet Update
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Enemy Spawn
    spawn_timer += 1
    if spawn_timer > 30:
        enemies.append([random.randint(0, WIDTH - 40), -40])
        spawn_timer = 0

    # Enemy Update
    for enemy in enemies[:]:
        enemy[1] += enemy_speed

        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # Collision
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 40, 40)

        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 4, 12)

            if enemy_rect.colliderect(bullet_rect):
                if enemy in enemies:
                    enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)

                score += 10
                break

    # Draw
    screen.fill(BLACK)

    # Player
    pygame.draw.polygon(screen, GREEN,
                        [(player_x + 25, player_y),
                         (player_x, player_y + 40),
                         (player_x + 50, player_y + 40)])

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE,
                         (bullet[0], bullet[1], 4, 12))

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED,
                         (enemy[0], enemy[1], 40, 40))

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()