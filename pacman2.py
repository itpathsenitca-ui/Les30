import pygame
import random

# --- Настройки ---
WIDTH, HEIGHT = 608, 448        # Размер окна (19x14 клеток по 32px)
CELL = 32
ROWS, COLS = HEIGHT // CELL, WIDTH // CELL

# --- Цвета ---
BLACK = (0, 0, 0)
BLUE = (44, 62, 80)
YELLOW = (255, 255, 100)
RED = (255, 0, 0)
WHITE = (230, 230, 230)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)

# --- Карта уровня ('#' — стена, '.' — еда, ' ' — пусто) ---
LEVEL_MAP = [
    "###################",
    "#........#........#",
    "#.###.###.###.###.#",
    "#.................#",
    "#.###.#.#####.#.###",
    "#.....#...#...#...#",
    "#####.### # ###.###",
    "    #.#   G #.#    ",
    "#####.# #####.#.###",
    "#........#........#",
    "#.###.###.###.###.#",
    "#...#.........#...#",
    "###.#.#.#####.#.###",
    "#........P........#",
    "###################"
]

# --- Подготовка Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

# --- Вспомогательные функции ---
def draw_text(surf, text, pos, color=WHITE):
    txt = font.render(text, True, color)
    surf.blit(txt, pos)

def map_find(char):
    for y, line in enumerate(LEVEL_MAP):
        for x, cell in enumerate(line):
            if cell == char:
                return x, y
    return None

def grid2px(x, y):
    return x * CELL, y * CELL

def px2grid(px, py):
    return px // CELL, py // CELL

def can_move(grid, dx, dy):
    x, y = grid
    nx, ny = x + dx, y + dy
    if 0 <= nx < COLS and 0 <= ny < ROWS:
        return LEVEL_MAP[ny][nx] != '#'
    return False

# --- Классы ---
class Pacman:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.score = 0

    def update(self):
        # Смена направления по запросу, если возможно
        if can_move((self.x, self.y), *self.next_dir):
            self.dir = self.next_dir
        # Движение, если возможно
        if can_move((self.x, self.y), *self.dir):
            self.x += self.dir[0]
            self.y += self.dir[1]

class Enemy:
    def __init__(self, x, y, color=RED):
        self.x, self.y = x, y
        self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.color = color

    def update(self):
        # Случайное движение, избегая стен
        options = []
        for d in [(1,0), (-1,0), (0,1), (0,-1)]:
            if can_move((self.x, self.y), *d):
                options.append(d)
        if options:
            # Иногда меняет направление случайно
            if random.random() < 0.3 or not can_move((self.x, self.y), *self.dir):
                self.dir = random.choice(options)
            if can_move((self.x, self.y), *self.dir):
                self.x += self.dir[0]
                self.y += self.dir[1]

# --- Основная подготовка объектов ---
pac_start = map_find('P')
ghost_starts = [map_find('G')]
for y, row in enumerate(LEVEL_MAP):
    for x, cell in enumerate(row):
        if cell == 'G' and (x, y) not in ghost_starts:
            ghost_starts.append((x, y))

pacman = Pacman(*pac_start)
enemies = [Enemy(x, y) for (x, y) in ghost_starts]

# Еда: в каждой клетке, где '.'
food = set()
for y, line in enumerate(LEVEL_MAP):
    for x, c in enumerate(line):
        if c in '.P':
            food.add((x, y))

running = True
win = lose = False
timer = 0

# --- Главный игровой цикл ---
while running:
    clock.tick(8)  # Пакман идет не очень быстро
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not (win or lose):
            if event.key == pygame.K_LEFT:
                pacman.next_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                pacman.next_dir = (1, 0)
            elif event.key == pygame.K_UP:
                pacman.next_dir = (0, -1)
            elif event.key == pygame.K_DOWN:
                pacman.next_dir = (0, 1)

    if not (win or lose):
        pacman.update()

        for enemy in enemies:
            enemy.update()

        # Съедаем еду
        if (pacman.x, pacman.y) in food:
            food.remove((pacman.x, pacman.y))
            pacman.score += 10

        # Проверка победы
        if not food:
            win = True

        # Проверка проигрыша
        for enemy in enemies:
            if (pacman.x, pacman.y) == (enemy.x, enemy.y):
                lose = True

    # --- Рендер ---
    screen.fill(BLACK)

    # Рисуем карту и стены
    for y, line in enumerate(LEVEL_MAP):
        for x, char in enumerate(line):
            px, py = grid2px(x, y)
            if char == '#':
                pygame.draw.rect(screen, BLUE, (px, py, CELL, CELL))
            else:
                pygame.draw.rect(screen, BLACK, (px, py, CELL, CELL))

    # Рисуем еду
    for (x, y) in food:
        px, py = grid2px(x, y)
        pygame.draw.circle(screen, WHITE, (px + CELL//2, py + CELL//2), 5)

    # Рисуем пакмана
    px, py = grid2px(pacman.x, pacman.y)
    pygame.draw.circle(screen, YELLOW, (px + CELL//2, py + CELL//2), CELL//2 - 2)

    # Рисуем врагов
    for enemy in enemies:
        ex, ey = grid2px(enemy.x, enemy.y)
        pygame.draw.circle(screen, enemy.color, (ex + CELL//2, ey + CELL//2), CELL//2 - 4)

    # Счет
    draw_text(screen, f"Счет: {pacman.score}", (10, 5))

    # Сообщения победы/проигрыша
    if win:
        draw_text(screen, "ПОБЕДА!", (WIDTH // 2 - 60, HEIGHT // 2), GREEN)
    if lose:
        draw_text(screen, "ВЫ ПОПАЛИСЬ!", (WIDTH // 2 - 100, HEIGHT // 2), RED)

    pygame.display.flip()

    # Если кончилась игра — ждем для показа сообщения
    if win or lose:
        pygame.time.wait(2000)
        running = False

pygame.quit()