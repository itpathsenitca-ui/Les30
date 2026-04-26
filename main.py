import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пакман с врагами и стенами")

# Цвета
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Размеры
player_size = 20
enemy_size = 20
wall_thickness = 20

# Начальные позиции игрока и врагов
player_pos = [WIDTH // 2, HEIGHT // 2]
enemies = [
    [100, 100],
    [700, 100],
    [100, 500],
    [700, 500]
]

# Стены: создадим некоторые, чтобы было интересно
walls = [
    pygame.Rect(200, 150, wall_thickness, 300),
    pygame.Rect(400, 0, wall_thickness, 300),
    pygame.Rect(600, 300, wall_thickness, 300),
    pygame.Rect(0, 250, 300, wall_thickness),
    pygame.Rect(500, 450, 300, wall_thickness)
]

clock = pygame.time.Clock()

# Функция проверки коллизий с стенами
def check_collision(rect, walls):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# Основной цикл
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Передвижение игрока
    new_pos = player_pos.copy()
    speed = 5

    if keys[pygame.K_LEFT]:
        new_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        new_pos[0] += speed
    if keys[pygame.K_UP]:
        new_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        new_pos[1] += speed

    # Создаем rect для проверки коллизий
    player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
    if not check_collision(player_rect, walls):
        player_pos = new_pos

    # Рисуем стены
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall)

    # Рисуем игрока
    pygame.draw.rect(screen, YELLOW, (player_pos[0], player_pos[1], player_size, player_size))

    # Обработка врагов (просто движутся случайно)
    for enemy in enemies:
        # Случайное движение в каждом кадре
        direction = random.choice(['left', 'right', 'up', 'down', 'stay'])
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        new_enemy_pos = enemy.copy()

        if direction == 'left':
            new_enemy_pos[0] -= 2
        elif direction == 'right':
            new_enemy_pos[0] += 2
        elif direction == 'up':
            new_enemy_pos[1] -= 2
        elif direction == 'down':
            new_enemy_pos[1] += 2
        # "stay" — враг не двинется

        enemy_rect_moving = pygame.Rect(new_enemy_pos[0], new_enemy_pos[1], enemy_size, enemy_size)
        # Проверяем столкновение со стенами
        if not check_collision(enemy_rect_moving, walls):
            enemy[0], enemy[1] = new_enemy_pos

        # Рисуем врага
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

        # Проверка столкновения игрока с врагом
        if player_rect.colliderect(enemy_rect_moving):
            print("Вы проиграли!")
            running = False

    pygame.display.flip()

pygame.quit()