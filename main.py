#pgzero
import random

WIDTH = 550
HEIGHT = 600
TITLE = "Escape de las cuevas"
FPS = 30


# FONDO
fondo = Actor("background")


# BARCO
barco = Actor("boat",(275,240))


# PROTAGONISTA
prota = Actor("estandar1",(100,280))
prota.AP = 20
prota.HP = 100
prota.maxHP = 100


# LISTA DE ENEMIGOS
enemigos = []


# GENERAR ENEMIGOS
def generar_enemigos():

    enemigos.clear()

    cantidad = random.randint(2,5)

    for i in range(cantidad):

        x = random.randint(-100,-50)
        y = 290

        enemigo = Actor("idleskel3",(x,y))

        enemigo.speed = random.randint(2,4)
        enemigo.HP = random.randint(40,70)
        enemigo.AP = random.randint(5,10)

        enemigos.append(enemigo)



generar_enemigos()


# DIBUJAR
def draw():

    screen.clear()

    fondo.draw()

    if fondo.image == "background3":
        barco.draw()

    # enemigos
    for enemigo in enemigos:
        enemigo.draw()

    # jugador
    prota.draw()

    # BARRA DE VIDA
    screen.draw.text("HP", (20,20), color="white")

    screen.draw.filled_rect(
        Rect((60,20),(200,20)),
        "red"
    )

    screen.draw.filled_rect(
        Rect((60,20),(200*(prota.HP/prota.maxHP),20)),
        "green"
    )


# MOVIMIENTO ENEMIGOS
def mover_enemigos():

    for enemigo in enemigos:

        if prota.x > enemigo.x:
            enemigo.x += enemigo.speed
            enemigo.image = "skeletright"

        elif prota.x < enemigo.x:
            enemigo.x -= enemigo.speed
            enemigo.image = "skeletleft"

        # ataque enemigo
        if enemigo.colliderect(prota):
            enemigo.image = "ataque"
            prota.HP -= enemigo.AP * 0.02



# ATAQUE DEL JUGADOR
def atacar():

    for enemigo in enemigos[:]:

        if prota.colliderect(enemigo):

            enemigo.HP -= prota.AP

            if enemigo.HP <= 0:
                enemigos.remove(enemigo)



# CONTROLES
def on_key_down(key):

    if key == keys.W:
        prota.y -= 50
        animate(prota, tween="bounce_end", duration=0.5, y=280)

    if key == keys.SPACE:
        atacar()



# UPDATE
def update():

    # MOVIMIENTO JUGADOR
    if keyboard.A and prota.x > 0:
        prota.x -= 5
        prota.image = "left1"

    elif keyboard.D and prota.x < WIDTH:
        prota.x += 5
        prota.image = "right1"

    else:
        prota.image = "estandar1"


    # CAMBIO DE MAPA DERECHA
    if prota.x > 530:

        if fondo.image == "background":
            fondo.image = "background2"

        elif fondo.image == "background2":
            fondo.image = "background4"

        elif fondo.image == "background4":
            fondo.image = "background3"

        prota.x = 10
        generar_enemigos()


    # CAMBIO DE MAPA IZQUIERDA
    elif prota.x < 20:

        if fondo.image == "background2":
            fondo.image = "background"

        elif fondo.image == "background4":
            fondo.image = "background2"

        elif fondo.image == "background3":
            fondo.image = "background4"

        prota.x = 540
        generar_enemigos()


    # GAME OVER
    if prota.HP <= 0:
        print("GAME OVER")


    mover_enemigos()