import pyxel
import random
import time

# ----------------------------
# Réglages (sprite 16x16 retro)
# ----------------------------
WIDTH = 384
HEIGHT = 384
GRID = 32          # 32 px "monde" -> 16 px écran (avec SCALE=2)
SCALE = 2

pyxel.init(WIDTH // SCALE, HEIGHT // SCALE, title="Snake Game par Nicholas, Hafid et Micah", fps=30)
pyxel.load("res.pyxres")

# Couleurs grille (comme avant)
GREEN_DARK = 0
GREEN_LIGHT = 7
WHITE = 3
# ----------------------------
# Sprites (LE res.pyxres)
# ----------------------------
SPR_W = 16
SPR_H = 16
CELL = GRID // SCALE          # 16
OFFSET = (CELL - SPR_W) // 2  # 0

# Bank image 0
SPR = {
    # nourriture
    "FOOD": (0, 0),

    # UP (u=16)
    "HEAD_U": (16, 0),
    "BODY_V_U": (16, 16),
    "TAIL_U": (16, 32),

    # DOWN (u=32)
    "TAIL_D": (32, 0),
    "BODY_V_D": (32, 16),
    "HEAD_D": (32, 32),

    # LEFT (v=56)
    "HEAD_L": (0, 56),
    "BODY_H_L": (16, 56),
    "TAIL_L": (32, 56),

    # RIGHT (v=72)
    "TAIL_R": (0, 72),
    "BODY_H_R": (16, 72),
    "HEAD_R": (32, 72),
}

# ----------------------------
# Variables (style original)
# ----------------------------
snake_pos = [WIDTH // 2, HEIGHT // 2]
snake_body = [list(snake_pos)]
direction = "STOP"
change_to = direction

food_pos = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]

score = 0
high_score = 0
delay = 10
frame_counter = 0


# ----------------------------
# Utilitaires
# ----------------------------
def sgn(a: int) -> int:
    return (a > 0) - (a < 0)

def cell_of(px: int, py: int):
    return px // GRID, py // GRID

def blt_cell(cx: int, cy: int, key: str):
    u, v = SPR[key]
    x = cx * CELL + OFFSET
    y = cy * CELL + OFFSET
    pyxel.blt(x, y, 0, u, v, SPR_W, SPR_H, colkey=0)

def show_score():
    txt = f"Score: {score}  High Score: {high_score}"
    pyxel.text((WIDTH // SCALE) // 2 - len(txt) * 2, 5, txt, WHITE)

def spawn_food():
    while True:
        p = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]
        if p not in snake_body:
            return p

def game_over():
    global snake_body, snake_pos, direction, change_to, score, delay
    time.sleep(0.6)
    snake_pos[:] = [WIDTH // 2, HEIGHT // 2]
    snake_body[:] = [list(snake_pos)]
    direction = "STOP"
    change_to = "STOP"
    score = 0
    delay = 10


# ----------------------------
# Update (gameplay)
# ----------------------------
def update():
    global direction, change_to, snake_pos, score, high_score, food_pos, frame_counter, delay

    # quitter
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # touches (comme original)
    if pyxel.btnp(pyxel.KEY_UP) and direction != "DOWN":
        change_to = "UP"
    if pyxel.btnp(pyxel.KEY_DOWN) and direction != "UP":
        change_to = "DOWN"
    if pyxel.btnp(pyxel.KEY_LEFT) and direction != "RIGHT":
        change_to = "LEFT"
    if pyxel.btnp(pyxel.KEY_RIGHT) and direction != "LEFT":
        change_to = "RIGHT"

    # si STOP, on n'applique pas une direction "STOP" sur la queue
    direction = change_to

    # temps
    frame_counter += 1
    if frame_counter < delay:
        return
    frame_counter = 0

    # STOP = on ne bouge pas (évite bugs / collisions chelou au départ)
    if direction == "STOP":
        return

    # mouvement
    if direction == "UP":
        snake_pos[1] -= GRID
    elif direction == "DOWN":
        snake_pos[1] += GRID
    elif direction == "LEFT":
        snake_pos[0] -= GRID
    elif direction == "RIGHT":
        snake_pos[0] += GRID

    # ajouter tête
    snake_body.insert(0, list(snake_pos))

    # manger nourriture
    if snake_pos == food_pos:
        score += 10
        delay = max(3, delay - 1)
        food_pos = spawn_food()
        if score > high_score:
            high_score = score
    else:
        snake_body.pop()

    # collision bords
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over()
        return

    # collision corps
    for block in snake_body[1:]:
        if block == snake_pos:
            game_over()
            return

def draw():
    pyxel.cls(0)

    # grille, QUADRILLAGE
    for y in range(0, HEIGHT // SCALE, GRID // SCALE):
        for x in range(0, WIDTH // SCALE, GRID // SCALE):
            color = GREEN_LIGHT if (x // (GRID // SCALE) + y // (GRID // SCALE)) % 2 == 0 else GREEN_DARK
            pyxel.rect(x, y, GRID // SCALE, GRID // SCALE, color)

    # nourriture
    fx, fy = cell_of(food_pos[0], food_pos[1])
    blt_cell(fx, fy, "FOOD")


    cells = [cell_of(b[0], b[1]) for b in snake_body]

    # TÊTE
    hx, hy = cells[0]
    if direction == "UP":
        blt_cell(hx, hy, "HEAD_U")
    elif direction == "DOWN":
        blt_cell(hx, hy, "HEAD_D")
    elif direction == "LEFT":
        blt_cell(hx, hy, "HEAD_L")
    else:
        blt_cell(hx, hy, "HEAD_R")

    # --- CORPS ---
    if len(cells) >= 3:
        for i in range(1, len(cells) - 1):
            px, py = cells[i - 1]
            cx, cy = cells[i]
            nx, ny = cells[i + 1]

            dx1, dy1 = sgn(cx - px), sgn(cy - py)
            dx2, dy2 = sgn(nx - cx), sgn(ny - cy)

            # tout droit horizontal
            if dy1 == 0 and dy2 == 0:
                # petit "feeling" : on prend la variante qui correspond au sens dominant
                key = "BODY_H_R" if dx2 >= 0 else "BODY_H_L"
                blt_cell(cx, cy, key)

            # tout droit vertical
            elif dx1 == 0 and dx2 == 0:
                key = "BODY_V_D" if dy2 >= 0 else "BODY_V_U"
                blt_cell(cx, cy, key)

            # virage
            else:
                # si on tourne vers vertical -> body vertical, sinon horizontal
                if dy2 != 0:
                    key = "BODY_V_D" if dy2 > 0 else "BODY_V_U"
                else:
                    key = "BODY_H_R" if dx2 > 0 else "BODY_H_L"
                blt_cell(cx, cy, key)

    # QUEUE
    if len(cells) >= 2:
        bx, by = cells[-2]
        tx, ty = cells[-1]
        dx, dy = sgn(tx - bx), sgn(ty - by)

        # Ici : on choisit la queue qui "pointe" vers le segment précédent (bien orientée)
        if dx == 1:
            blt_cell(tx, ty, "TAIL_L")
        elif dx == -1:
            blt_cell(tx, ty, "TAIL_R")
        elif dy == 1:
            blt_cell(tx, ty, "TAIL_U")
        else:
            blt_cell(tx, ty, "TAIL_D")

    show_score()
pyxel.run(update, draw)
