import pygame
import random
import math

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-Mindustry")
clock = pygame.time.Clock()

# Цвета
WHITE = (255,255,255)
GRAY = (100,100,100)
DARK_GRAY = (50,50,50)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)

# Карта
tile_size = 40
rows = HEIGHT // tile_size
cols = WIDTH // tile_size

# Простая карта
map_data = []
for y in range(rows):
    row = []
    for x in range(cols):
        if y > rows//2:
            row.append("ground")
        else:
            row.append("water")
    map_data.append(row)

# Блоки строений
buildings = []

# Объекты ресурсов
resources = {
    "metal": 0,
    "energy": 0
}

# Предметы
class Block:
    def __init__(self, x, y, type):
        self.x, self.y = x, y
        self.type = type
        self.health = 100
        self.max_health = 100

    def draw(self):
        px = self.x*tile_size
        py = self.y*tile_size
        if self.type == "factory":
            color = DARK_GRAY
        elif self.type == "power":
            color = YELLOW
        elif self.type == "assembler":
            color = GRAY
        else:
            color = WHITE

        pygame.draw.rect(screen, color, (px+2, py+2, tile_size-4, tile_size-4))
        # здоровье
        health_bar_w = tile_size * (self.health / self.max_health)
        pygame.draw.rect(screen, RED, (px, py - 5, tile_size, 3))
        pygame.draw.rect(screen, GREEN, (px, py - 5, health_bar_w, 3))

# Враги
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.speed = 1
        self.target = (cols//2, rows//2)
        self.path = []

    def move(self):
        if not self.path:
            self.path = a_star((self.x, self.y), self.target)
        if self.path:
            next_pos = self.path.pop(0)
            self.x, self.y = next_pos

    def draw(self):
        px = self.x * tile_size
        py = self.y * tile_size
        pygame.draw.circle(screen, RED, (px+tile_size//2, py+tile_size//2), tile_size//3)

# ------------------------------------------
# Алгоритм поиска пути (A*)
def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < cols and 0 <= ny < rows:
            if map_data[ny][nx] != "water":
                neighbors.append((nx, ny))
    return neighbors

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

import heapq

def a_star(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start:0}
    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        for neighbor in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current
    if goal not in came_from:
        return []
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Игрок
player_pos = [cols//2, rows//2]
player_action = None

# Создаём врагов
enemies = [Enemy(0,0), Enemy(cols-1,0)]

# Основной цикл
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Обработка ввода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_action = (0,-1)
            elif event.key == pygame.K_s:
                player_action = (0,1)
            elif event.key == pygame.K_a:
                player_action = (-1,0)
            elif event.key == pygame.K_d:
                player_action = (1,0)

    # Передвижение игрока
    if player_action:
        nx, ny = player_pos[0]+player_action[0], player_pos[1]+player_action[1]
        if 0 <= nx < cols and 0 <= ny < rows:
            if map_data[ny][nx] != "water":
                player_pos = [nx, ny]
        player_action = None

    # Обновление врагов
    for enemy in enemies:
        enemy.move()

        # Если враг достиг базы, наносим урон
        if enemy.x == cols//2 and enemy.y == rows//2:
            resources["metal"] -= 1  # пример атаки

        # Враг атакует, если рядом
        if abs(enemy.x - player_pos[0]) <=1 and abs(enemy.y - player_pos[1])<=1:
            resources["metal"] -= 1

    # Рисуем карту
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            if map_data[y][x] == "water":
                pygame.draw.rect(screen, DARK_GRAY, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Рисуем здания
    for b in buildings:
        b.draw()

    # Рисуем врагов
    for enemy in enemies:
        enemy.draw()

    # Рисуем игрок
    pygame.draw.rect(screen, GREEN, (player_pos[0]*tile_size+5, player_pos[1]*tile_size+5, tile_size-10, tile_size-10))

    # Отображение ресурсов
    font = pygame.font.SysFont(None, 24)
    res_text = font.render(f"Metal: {resources['metal']} Energy: {resources['energy']}", True, WHITE)
    screen.blit(res_text, (10, 10))

    pygame.display.flip()

pygame.quit()
class Drone:
    def __init__(self, x, y):
        self.x = x + 0.5  # позиция как точка для плавных передвижений
        self.y = y + 0.5
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 0.05  # скорость плавного перемещения
        self.angle = random.uniform(0, 2*math.pi)

    def update(self):
        # случайное движение в пределах карты
        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 0.1:
            self.target_x = random.uniform(0, cols)
            self.target_y = random.uniform(0, rows)

        # движение к цели
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self):
        px = self.x * tile_size
        py = self.y * tile_size
        pygame.draw.circle(screen, BLUE, (int(px), int(py)), 8)
        # можно добавить визуальные эффекты или указывать направление

# Инициализация дронов
drones = [Drone(cols//4, rows//4), Drone(3*cols//4, rows//4)]

# В основном цикле
while running:
    # ... остальной код ...

    # Обновление и рисование дронов
    for drone in drones:
        drone.update()
        drone.draw()
# Персонаж
player_char = {
    "x": cols // 2,
    "y": rows // 2,
    "size": 20,
    "color": (255, 200, 0),
    "speed": 0.2,
    "vx": 0,
    "vy": 0
}

# Обработка управления
keys_pressed = {"up":False, "down":False, "left":False, "right":False}

# В основном цикле обработки событий добавим обработку стрелок
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running=False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            keys_pressed["up"] = True
        elif event.key == pygame.K_s:
            keys_pressed["down"] = True
        elif event.key == pygame.K_a:
            keys_pressed["left"] = True
        elif event.key == pygame.K_d:
            keys_pressed["right"] = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            keys_pressed["up"] = False
        elif event.key == pygame.K_s:
            keys_pressed["down"] = False
        elif event.key == pygame.K_a:
            keys_pressed["left"] = False
        elif event.key == pygame.K_d:
            keys_pressed["right"] = False

# Обновляем позицию персонажа с учетом нажатий
if keys_pressed["up"]:
    player_char["vy"] = -player_char["speed"]
elif keys_pressed["down"]:
    player_char["vy"] = player_char["speed"]
else:
    player_char["vy"] = 0

if keys_pressed["left"]:
    player_char["vx"] = -player_char["speed"]
elif keys_pressed["right"]:
    player_char["vx"] = player_char["speed"]
else:
    player_char["vx"] = 0

# Передвижение персонажа
player_char["x"] += player_char["vx"]
player_char["y"] += player_char["vy"]

# Ограничение выхода за границы
player_char["x"] = max(0, min(cols-1, player_char["x"]))
player_char["y"] = max(0, min(rows-1, player_char["y"]))

# В рисовании добавим персонажа
px = int(player_char["x"] * tile_size)
py = int(player_char["y"] * tile_size)
pygame.draw.rect(screen, player_char["color"],
                 (px + 4, py + 4, tile_size - 8, tile_size - 8))