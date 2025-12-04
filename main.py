import pyxel
import random
import time

# initialise
WIDTH = 600
HEIGHT = 600
GRID = 20
SCALE = 4

pyxel.init(WIDTH // SCALE, HEIGHT // SCALE, title="Snake Game par Nicholas, Hafid et Micah", fps=60)


# couleurs 
GREEN_DARK = 3 # vert foncé
GREEN_LIGHT = 11
RED         = 8    # reste pour nourriture
BLACK       = 0
WHITE       = 7    # texte


# variables

snake_pos = [300, 300]
snake_body = [[300, 300]]
direction = "STOP"
change_to = direction
food_pos = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]
score = 0
high_score = 0
delay = 10     # vitesse FPS
frame_counter = 0


# fonctions

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

def update():
    global direction, change_to, snake_pos, score, high_score, food_pos, frame_counter, delay

    # quitter
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # touches
    if pyxel.btnp(pyxel.KEY_W) and direction != "DOWN":
        change_to = "UP"
    if pyxel.btnp(pyxel.KEY_S) and direction != "UP":
        change_to = "DOWN"
    if pyxel.btnp(pyxel.KEY_A) and direction != "RIGHT":
        change_to = "LEFT"
    if pyxel.btnp(pyxel.KEY_D) and direction != "LEFT":
        change_to = "RIGHT"

    direction = change_to

    # temps
    frame_counter += 1
    if frame_counter < delay:
        return
    frame_counter = 0

    # mouvement
    if direction == "UP":
        snake_pos[1] -= GRID
    if direction == "DOWN":
        snake_pos[1] += GRID
    if direction == "LEFT":
        snake_pos[0] -= GRID
    if direction == "RIGHT":
        snake_pos[0] += GRID

    # ajouter une queue
    snake_body.insert(0, list(snake_pos))

    # collision nourriture
    if snake_pos == food_pos:
        score += 10
        delay = max(3, delay - 1)
        food_pos = [random.randrange(0, WIDTH, GRID), random.randrange(0, HEIGHT, GRID)]

        if score > high_score:
            high_score = score
    else:
        snake_body.pop()

    # collision bords
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over()

    # collision corps
    for block in snake_body[1:]:
        if block == snake_pos:
            game_over()


# draw

def draw():
    pyxel.cls(0)  # fond vide

    # Dessiner la grille damier
    for y in range(0, HEIGHT // SCALE, GRID // SCALE):
        for x in range(0, WIDTH // SCALE, GRID // SCALE):
            color = GREEN_LIGHT if (x // (GRID // SCALE) + y // (GRID // SCALE)) % 2 == 0 else GREEN_DARK
            pyxel.rect(x, y, GRID // SCALE, GRID // SCALE, color)

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

pyxel.run(update, draw)
