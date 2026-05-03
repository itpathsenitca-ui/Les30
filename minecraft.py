import pygame
import random
import math

# --- Инициализация ---
pygame.init()
W, H = 800, 600
TILE = 40
REACH = 150  # Радиус действия (невидимый)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("2D Minecraft: Empty Inventory")
clock = pygame.time.Clock()

# --- Блоки ---
BLOCKS = {
    0: {"name": "Air", "color": None, "dur": 0},
    1: {"name": "Grass", "color": (34, 139, 34), "dur": 15},
    2: {"name": "Dirt", "color": (139, 69, 19), "dur": 15},
    3: {"name": "Stone", "color": (105, 105, 105), "dur": 40},
    4: {"name": "Sand", "color": (238, 214, 175), "dur": 10},
    5: {"name": "Wood", "color": (101, 67, 33), "dur": 20},
    6: {"name": "Leaves", "color": (40, 100, 40), "dur": 5}
}

# --- Мир ---
world_w, world_h = 200, 60
world = [[0 for _ in range(world_w)] for _ in range(world_h)]

# --- ГЕНЕРАЦИЯ ---
seed = random.random() * 1000
for c in range(world_w):
    height_offset = math.sin(c * 0.1 + seed) * 3
    height_offset += math.sin(c * 0.05 + seed) * 5
    g_y = int(30 + height_offset)

    for r in range(max(0, g_y), world_h):
        if r == g_y:
            world[r][c] = 4 if height_offset < -4 else 1
        elif r < g_y + 4:
            world[r][c] = 2
        else:
            world[r][c] = 3

# Деревья
for c in range(5, world_w - 5):
    for r in range(world_h):
        if world[r][c] == 1:
            if random.random() < 0.1:
                h = random.randint(3, 5)
                for i in range(1, h + 1): world[r - i][c] = 5
                for lr in range(r - h - 3, r - h):
                    for lc in range(c - 2, c + 3):
                        if 0 <= lr < world_h and 0 <= lc < world_w:
                            if world[lr][lc] == 0: world[lr][lc] = 6
            break

# --- Игрок и Физика ---
player = pygame.Rect(400, 20 * TILE, 26, 50)
v_y = 0
scroll_x = player.x - W // 2
scroll_y = player.y - H // 2

# ПРЕДМЕТЫ УБРАНЫ (все по 0)
inventory = {i: 0 for i in range(1, 7)}
selected_slot = 1


def get_nearby_blocks(rect):
    nearby = []
    for r in range(max(0, rect.top // TILE), min(world_h, rect.bottom // TILE + 1)):
        for c in range(max(0, rect.left // TILE), min(world_w, rect.right // TILE + 1)):
            if world[r][c] != 0:
                nearby.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))
    return nearby


# --- Цикл ---
run = True
breaking_pos = None
breaking_timer = 0
font = pygame.font.SysFont("Arial", 16, bold=True)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_6: selected_slot = int(event.unicode)

    # Движение
    keys = pygame.key.get_pressed()
    v_x = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
    player.x += v_x
    for block in get_nearby_blocks(player):
        if player.colliderect(block):
            if v_x > 0: player.right = block.left
            if v_x < 0: player.left = block.right

    v_y += 0.8
    if v_y > 15: v_y = 15
    player.y += v_y
    on_ground = False
    for block in get_nearby_blocks(player):
        if player.colliderect(block):
            if v_y > 0:
                player.bottom = block.top
                v_y = 0
                on_ground = True
            elif v_y < 0:
                player.top = block.bottom
                v_y = 0
    if keys[pygame.K_SPACE] and on_ground: v_y = -14

    # Камера
    scroll_x += (player.centerx - W // 2 - scroll_x) / 15
    scroll_y += (player.centery - H // 2 - scroll_y) / 15

    # Взаимодействие (с радиусом)
    mx, my = pygame.mouse.get_pos()
    world_mx, world_my = mx + scroll_x, my + scroll_y
    m_c, m_r = int(world_mx // TILE), int(world_my // TILE)
    m_btn = pygame.mouse.get_pressed()

    dist = math.hypot(player.centerx - world_mx, player.centery - world_my)
    in_reach = dist <= REACH

    if in_reach and 0 <= m_c < world_w and 0 <= m_r < world_h:
        if m_btn[2]:  # Строить
            if world[m_r][m_c] == 0 and inventory[selected_slot] > 0:
                if not player.colliderect(pygame.Rect(m_c * TILE, m_r * TILE, TILE, TILE)):
                    world[m_r][m_c] = selected_slot
                    inventory[selected_slot] -= 1

        if m_btn[0]:  # Ломать
            if world[m_r][m_c] != 0:
                if breaking_pos == (m_c, m_r):
                    breaking_timer += 1
                    if breaking_timer >= BLOCKS[world[m_r][m_c]]["dur"]:
                        inventory[world[m_r][m_c]] += 1
                        world[m_r][m_c] = 0
                        breaking_timer = 0
                else:
                    breaking_pos = (m_c, m_r);
                    breaking_timer = 0
        else:
            breaking_timer = 0
    else:
        breaking_timer = 0

    # Отрисовка
    screen.fill((135, 206, 235))
    s_col, e_col = int(scroll_x // TILE), int((scroll_x + W) // TILE + 1)
    s_row, e_row = int(scroll_y // TILE), int((scroll_y + H) // TILE + 1)

    for r in range(max(0, s_row), min(world_h, e_row)):
        for c in range(max(0, s_col), min(world_w, e_col)):
            bid = world[r][c]
            if bid != 0:
                dx, dy = int(c * TILE - scroll_x), int(r * TILE - scroll_y)
                pygame.draw.rect(screen, BLOCKS[bid]["color"], (dx, dy, TILE, TILE))
                pygame.draw.rect(screen, (0, 0, 0), (dx, dy, TILE, TILE), 1)
                if breaking_pos == (c, r) and in_reach:
                    p = breaking_timer / BLOCKS[bid]["dur"]
                    pygame.draw.rect(screen, (255, 0, 0), (dx, dy + TILE - 5, int(TILE * p), 5))

    # Игрок
    pygame.draw.rect(screen, (220, 20, 60),
                     (int(player.x - scroll_x), int(player.y - scroll_y), player.width, player.height))

    # Отрисовка инвентаря
    for i in range(1, 7):
        ix = (W // 2 - 165) + (i - 1) * 55
        # Фон ячейки
        pygame.draw.rect(screen, (30, 30, 30), (ix, H - 70, 50, 50))
        # Рамка выбора
        if selected_slot == i:
            pygame.draw.rect(screen, (255, 255, 255), (ix, H - 70, 50, 50), 2)

        # Отображаем блок и количество, только если они есть
        if inventory[i] > 0:
            pygame.draw.rect(screen, BLOCKS[i]["color"], (ix + 10, H - 60, 30, 30))
            txt = font.render(str(inventory[i]), True, (255, 255, 255))
            screen.blit(txt, (ix + 5, H - 65))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()