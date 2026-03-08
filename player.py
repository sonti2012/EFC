from pgzero.builtins import Actor
from constants import PLAYER_START_X, PLAYER_START_Y, PLAYER_AP, PLAYER_HP


def crear_jugador() -> Actor:
    """Crea y devuelve el actor del protagonista con sus atributos iniciales."""
    jugador = Actor("estandar1", (PLAYER_START_X, PLAYER_START_Y))
    jugador.AP    = PLAYER_AP
    jugador.HP    = PLAYER_HP
    jugador.maxHP = PLAYER_HP
    return jugador
