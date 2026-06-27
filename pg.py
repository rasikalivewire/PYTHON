import pygame

pygame.init()

screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("My First Pygame")

running = True

while running:
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 150, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()