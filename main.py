import pyxel
import random

# ----------------------------
# Réglages
# ----------------------------
WIDTH = 384
HEIGHT = 384
GRID = 32
SCALE = 2

SCREEN_W = WIDTH // SCALE
SCREEN_H = HEIGHT // SCALE
CELL = GRID // SCALE  # 16

pyxel.init(SCREEN_W, SCREEN_H, title="Snake Game", fps=60)
pyxel.load("res1.pyxres")

GREEN_DARK = 3
GREEN_LIGHT = 11
WHITE = 7

# ----------------------------
# Sprites (res1.pyxres - coords que tu utilises)
# ----------------------------
SPR_W = 16
SPR_H = 16
COLKEY = 10

SPR = {
    "FOOD":   (0, 0),

    "HEAD_U": (16, 0),
    "HEAD_D": (16, 32),
    "HEAD_L": (0, 80),
    "HEAD_R": (32, 80),

    "BODY":   (16, 16),   # gros carré bleu répété
}

# ----------------------------
# Variables jeu
# ----------------------------
snake_pos = [WIDTH // 2, HEIGHT // 2]
snake_body = [list(snake_pos)]
direction = "STOP"
change_to = "STOP"

food_pos = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]

score = 0
high_score = 0
delay = 10
frame_counter = 0

# Game over sans freeze (pas de sleep)
GAME_OVER_WAIT = 40
game_over_timer = 0

# ----------------------------
# Utils
# ----------------------------
def cell_of(px: int, py: int):
    return px // GRID, py // GRID

def blt_cell(cx: int, cy: int, key: str):
    u, v = SPR[key]
    x = cx * CELL
    y = cy * CELL
    pyxel.blt(x, y, 0, u, v, SPR_W, SPR_H, colkey=COLKEY)

def draw_checkerboard():
    for y in range(0, SCREEN_H, CELL):
        for x in range(0, SCREEN_W, CELL):
            c = GREEN_LIGHT if ((x // CELL + y // CELL) % 2 == 0) else GREEN_DARK
            pyxel.rect(x, y, CELL, CELL, c)

def show_score():
    txt = f"Score: {score}  High Score: {high_score}"
    pyxel.text(SCREEN_W // 2 - len(txt) * 2, 5, txt, WHITE)

def spawn_food():
    while True:
        p = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]
        if p not in snake_body:
            return p

def reset_game():
    global snake_pos, snake_body, direction, change_to, score, delay, frame_counter, food_pos
    snake_pos[:] = [WIDTH // 2, HEIGHT // 2]
    snake_body[:] = [list(snake_pos)]
    direction = "STOP"
    change_to = "STOP"
    score = 0
    delay = 10
    frame_counter = 0
    food_pos[:] = spawn_food()

# ----------------------------
# Yeux : carré noir + pixel blanc au centre
# (carré 5x5, centre parfait)
# ----------------------------

def draw_head(cx: int, cy: int, dir_: str):
    if dir_ == "UP":
        blt_cell(cx, cy, "HEAD_U")
    elif dir_ == "DOWN":
        blt_cell(cx, cy, "HEAD_D")
    elif dir_ == "LEFT":
        blt_cell(cx, cy, "HEAD_L")
    else:
        blt_cell(cx, cy, "HEAD_R")


# ----------------------------
# Update
# ----------------------------
def update():
    global direction, change_to, snake_pos, snake_body, food_pos
    global score, high_score, delay, frame_counter, game_over_timer

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # attente game over
    if game_over_timer > 0:
        game_over_timer -= 1
        if game_over_timer == 0:
            reset_game()
        return

    # contrôles
    if pyxel.btnp(pyxel.KEY_UP) and direction != "DOWN":
        change_to = "UP"
    if pyxel.btnp(pyxel.KEY_DOWN) and direction != "UP":
        change_to = "DOWN"
    if pyxel.btnp(pyxel.KEY_LEFT) and direction != "RIGHT":
        change_to = "LEFT"
    if pyxel.btnp(pyxel.KEY_RIGHT) and direction != "LEFT":
        change_to = "RIGHT"

    direction = change_to

    # timing
    frame_counter += 1
    if frame_counter < delay:
        return
    frame_counter = 0

    if direction == "STOP":
        return

    # nouvelle position
    new_pos = [snake_pos[0], snake_pos[1]]
    if direction == "UP":
        new_pos[1] -= GRID
    elif direction == "DOWN":
        new_pos[1] += GRID
    elif direction == "LEFT":
        new_pos[0] -= GRID
    elif direction == "RIGHT":
        new_pos[0] += GRID

    # murs
    if new_pos[0] < 0 or new_pos[0] >= WIDTH or new_pos[1] < 0 or new_pos[1] >= HEIGHT:
        game_over_timer = GAME_OVER_WAIT
        return

    # collision corps (avant insertion)
    if new_pos in snake_body:
        game_over_timer = GAME_OVER_WAIT
        return

    # avance
    snake_pos[:] = new_pos
    snake_body.insert(0, list(snake_pos))

    # mange
    if snake_pos == food_pos:
        score += 10
        delay = max(3, delay - 1)
        if score > high_score:
            high_score = score
        food_pos = spawn_food()
        # pas de pop => grandit
    else:
        snake_body.pop()

# ----------------------------
# Draw
# ----------------------------
def draw():
    pyxel.cls(0)
    draw_checkerboard()

    # food
    fx, fy = cell_of(food_pos[0], food_pos[1])
    blt_cell(fx, fy, "FOOD")

    # snake cells
    cells = [cell_of(b[0], b[1]) for b in snake_body]

    # tête
    hx, hy = cells[0]
    if direction == "STOP":
        draw_head(hx, hy, "RIGHT")
    else:
        draw_head(hx, hy, direction)

    # corps = carré bleu répété
    for i in range(1, len(cells)):
        cx, cy = cells[i]
        blt_cell(cx, cy, "BODY")

    show_score()

pyxel.run(update, draw)
