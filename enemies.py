import random
from typing import List

from pgzero.builtins import Actor
from constants import (
    ENEMY_COUNT_MIN, ENEMY_COUNT_MAX,
    ENEMY_SPEED_MIN, ENEMY_SPEED_MAX,
    ENEMY_HP_MIN,    ENEMY_HP_MAX,
    ENEMY_AP_MIN,    ENEMY_AP_MAX,
    ENEMY_START_Y,
    ENEMY_SPAWN_X_MIN, ENEMY_SPAWN_X_MAX,
)


def crear_enemigos() -> List[Actor]:
    """Genera y devuelve una lista de enemigos con atributos aleatorios."""
    cantidad = random.randint(ENEMY_COUNT_MIN, ENEMY_COUNT_MAX)
    enemigos = []

    for _ in range(cantidad):
        x = random.randint(ENEMY_SPAWN_X_MIN, ENEMY_SPAWN_X_MAX)
        enemigo = Actor("idleskel3", (x, ENEMY_START_Y))
        enemigo.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        enemigo.HP    = random.randint(ENEMY_HP_MIN,    ENEMY_HP_MAX)
        enemigo.AP    = random.randint(ENEMY_AP_MIN,    ENEMY_AP_MAX)
        enemigos.append(enemigo)

    return enemigos
