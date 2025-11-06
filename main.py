# code
#du code supplémentaire
import pyxel
from random import randint

x_carre2= randint(0,160)
y_carre2= randint(0,120)
x_carre1= 76
y_carre1= 56
fond=randint(2,15)
def update():
    pass
    global x_carre1, y_carre1, x_carre2, y_carre2, fond
    
#     # Déplacements clavier
#     if pyxel.btn(pyxel.KEY_RIGHT):
#         x_carre1 +=3
#     elif pyxel.btn(pyxel.KEY_LEFT):
#         x_carre1 -=3
#     elif pyxel.btn(pyxel.KEY_UP):
#         y_carre1 -=3
#     elif pyxel.btn(pyxel.KEY_DOWN):
#         y_carre1 +=3

     #collision
    if abs(x_carre1-x_carre2)<8 and abs(y_carre1-y_carre2)<8:
        x_carre2= randint(0,160)
        y_carre2= randint(0,120)
        fond=randint(2,15)

    #deplacement souris
    x_carre1 = pyxel.mouse_x
    y_carre1 = pyxel.mouse_y
    
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        fond=randint(2,15)
     
     
    
    y_carre1= max(0, min(y_carre1,120-8))
    y_carre2= max(0, min(y_carre2, 120-8))
    x_carre1= max(0, min(x_carre1,160-8))
    x_carre2= max(0, min(x_carre2, 160-8))
def draw():
    pyxel.cls(fond)
    pyxel.rect(x_carre1, y_carre1, 8,8, 1)
    pyxel.rect(x_carre2, y_carre2, 8,8, 0)
pyxel.init(160, 120, title="Play Colors with a Square")
pyxel.run(update, draw)
