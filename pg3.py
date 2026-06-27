import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake
snake_block = 20
snake_speed = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)

def score_display(score):
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, [10, 10])

def game():
    x = WIDTH // 2
    y = HEIGHT // 2

    x_change = 0
    y_change = 0

    snake = []
    length = 1

    food_x = random.randrange(0, WIDTH - snake_block, snake_block)
    food_y = random.randrange(0, HEIGHT - snake_block, snake_block)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        x += x_change
        y += y_change

        # Game Over at Boundary
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            running = False

        screen.fill(WHITE)

        pygame.draw.rect(screen, RED,
                         [food_x, food_y, snake_block, snake_block])

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)

        snake.append(snake_head)

        if len(snake) > length:
            del snake[0]

        # Self Collision
        for block in snake[:-1]:
            if block == snake_head:
                running = False

        for block in snake:
            pygame.draw.rect(screen, GREEN,
                             [block[0], block[1],
                              snake_block, snake_block])

        score_display(length - 1)

        pygame.display.update()

        # Food Collision
        if x == food_x and y == food_y:
            food_x = random.randrange(
                0, WIDTH - snake_block, snake_block)
            food_y = random.randrange(
                0, HEIGHT - snake_block, snake_block)
            length += 1

        clock.tick(snake_speed)

    pygame.quit()

game()