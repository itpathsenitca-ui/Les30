import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Персонаж на клавишах")
clock = pygame.time.Clock()

# Параметры персонажа
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_size = 40
player_color = (255, 200, 50)
speed = 5

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= speed
    if keys[pygame.K_s]:
        player_y += speed
    if keys[pygame.K_a]:
        player_x -= speed
    if keys[pygame.K_d]:
        player_x += speed

    # Ограничение по границам экрана
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # Рисуем фон
    screen.fill((30, 30, 30))
    # Рисуем персонажа
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()