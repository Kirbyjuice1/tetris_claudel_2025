import pyxel
import random
import time

# --- INITIALISATION ---
WIDTH = 600
HEIGHT = 600
GRID = 20

# Pyxel ne supporte pas 600x600, donc on crée un ratio 1:1 visuellement
# en réduisant l'écran et en multipliant les coordonnées au dessin
SCALE = 2
pyxel.init(WIDTH // SCALE, HEIGHT // SCALE, title="Snake Game par Nicholas, Hafid et Micah", fps=60)

# Couleurs Pyxel (0 à 15)
GREEN = 3
BLACK = 0
RED = 8
GREY = 5
WHITE = 7

# --- VARIABLES ---
snake_pos = [300, 300]
snake_body = [[300, 300]]

direction = "STOP"
change_to = direction

food_pos = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]

score = 0
high_score = 0
delay = 10     # vitesse (nombre de frames entre mouvements)
frame_counter = 0


# --- FONCTIONS ---
def game_over():
    global snake_body, snake_pos, direction, score, delay
    time.sleep(1)

    snake_pos[:] = [300, 300]
    snake_body[:] = [[300, 300]]
    direction = "STOP"
    score = 0
    delay = 10


def show_score():
    txt = f"Score: {score}  High Score: {high_score}"
    pyxel.text((WIDTH // SCALE) // 2 - len(txt)*2, 5, txt, WHITE)


# --- UPDATE ---
def update():
    global direction, change_to, snake_pos, score, high_score, food_pos, frame_counter, delay

    # Quitter
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # Contrôles (mêmes touches)
    if pyxel.btnp(pyxel.KEY_W) and direction != "DOWN":
        change_to = "UP"
    if pyxel.btnp(pyxel.KEY_S) and direction != "UP":
        change_to = "DOWN"
    if pyxel.btnp(pyxel.KEY_A) and direction != "RIGHT":
        change_to = "LEFT"
    if pyxel.btnp(pyxel.KEY_D) and direction != "LEFT":
        change_to = "RIGHT"

    direction = change_to

    # Gestion du temps (équivalent de clock.tick())
    frame_counter += 1
    if frame_counter < delay:
        return
    frame_counter = 0

    # Mouvement
    if direction == "UP":
        snake_pos[1] -= GRID
    if direction == "DOWN":
        snake_pos[1] += GRID
    if direction == "LEFT":
        snake_pos[0] -= GRID
    if direction == "RIGHT":
        snake_pos[0] += GRID

    # Ajout tête
    snake_body.insert(0, list(snake_pos))

    # Collision nourriture
    if snake_pos == food_pos:
        score += 10
        delay = max(3, delay - 1)
        food_pos = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]

        if score > high_score:
            high_score = score
    else:
        snake_body.pop()

    # Collision bords
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over()

    # Collision corps
    for block in snake_body[1:]:
        if block == snake_pos:
            game_over()


# --- DRAW ---
def draw():
    pyxel.cls(GREEN)

    # Dessiner nourriture
    px = food_pos[0] // SCALE
    py = food_pos[1] // SCALE
    pyxel.rect(px, py, GRID // SCALE, GRID // SCALE, RED)

    # Dessiner serpent
    for block in snake_body:
        bx = block[0] // SCALE
        by = block[1] // SCALE
        pyxel.rect(bx, by, GRID // SCALE, GRID // SCALE, BLACK)

    show_score()


# Lancement
pyxel.run(update, draw)

