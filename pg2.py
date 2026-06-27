import pygame

pygame.init()

screen = pygame.display.set_mode((600, 400))

x = 50

running = True
while running:

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (x, 200), 30)

    x += 2

    if x > 600:
        x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()