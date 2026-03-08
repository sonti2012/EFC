# main.py — Escape de las cuevas (pgzero)
from __future__ import annotations

import os

from pgzero.builtins import Actor, animate, keyboard, keys
from pgzero.rect import Rect
from pgzero.screen import Screen

from constants import (
    WIDTH, HEIGHT, TITLE, FPS,
    MAP_SEQUENCE, MAP_WITH_BOAT,
    BORDER_RIGHT, BORDER_LEFT,
    SPAWN_LEFT, SPAWN_RIGHT,
    DAMAGE_RATE,
    PLAYER_START_Y,
    PUNTOS_ENEMIGO, PUNTOS_PANTALLA, SCORES_FILE,
)
from player import crear_jugador
from enemies import crear_enemigos

screen: Screen

# ── Estados ───────────────────────────────────────────────────
MENU      = "menu"
JUGANDO   = "jugando"
GAME_OVER = "game_over"

# ── Variables globales ────────────────────────────────────────
estado     = MENU
_mapa_idx  = 0
puntuacion = 0

# ── Botón inicio ──────────────────────────────────────────────
_BTN_W, _BTN_H = 200, 55
_BTN_X = WIDTH  // 2 - _BTN_W // 2
_BTN_Y = HEIGHT // 2 + 20
_btn_rect = Rect((_BTN_X, _BTN_Y), (_BTN_W, _BTN_H))

# ── Actores ───────────────────────────────────────────────────
fondo    = Actor("background")
barco    = Actor("boat", (275, 240))
prota    = crear_jugador()
enemigos = crear_enemigos()


# ── Puntuación ────────────────────────────────────────────────
def _guardar_puntuacion(pts: int) -> None:
    """Añade la puntuación al archivo de scores."""
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{pts}\n")


def _mejor_puntuacion() -> int:
    """Devuelve la mejor puntuación guardada, o 0 si no hay archivo."""
    if not os.path.exists(SCORES_FILE):
        return 0
    with open(SCORES_FILE, encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip().isdigit()]
    return max((int(l) for l in lineas), default=0)


# ── HUD ───────────────────────────────────────────────────────
def _dibujar_hud() -> None:
    # Barra de vida (izquierda)
    screen.draw.text("HP", (20, 20), color="white", fontsize=22)
    screen.draw.filled_rect(Rect((60, 20), (200, 20)), "red")
    ancho_vida = int(200 * max(prota.HP, 0) / prota.maxHP)
    screen.draw.filled_rect(Rect((60, 20), (ancho_vida, 20)), "green")

    # Puntuación (derecha)
    screen.draw.text(
        f"Puntos: {puntuacion}",
        topright=(WIDTH - 15, 15),
        color="white",
        fontsize=22,
    )


# ── Pantalla de menú ──────────────────────────────────────────
def _dibujar_menu() -> None:
    screen.clear()
    fondo.draw()

    # Título
    screen.draw.text(
        TITLE,
        center=(WIDTH // 2, HEIGHT // 2 - 100),
        fontsize=44,
        color="white",
        shadow=(2, 2),
        scolor="black",
    )

    # Mejor puntuación
    mejor = _mejor_puntuacion()
    if mejor > 0:
        screen.draw.text(
            f"Mejor puntuación: {mejor}",
            center=(WIDTH // 2, HEIGHT // 2 - 30),
            fontsize=26,
            color="yellow",
        )

    # Botón
    screen.draw.filled_rect(_btn_rect, (30, 90, 180))
    screen.draw.rect(_btn_rect, "white")
    screen.draw.text(
        "INICIAR JUEGO",
        center=_btn_rect.center,
        fontsize=26,
        color="white",
    )


# ── Pantalla de Game Over ─────────────────────────────────────
def _dibujar_game_over() -> None:
    screen.draw.text(
        "GAME OVER",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=60,
        color="red",
        shadow=(2, 2),
        scolor="black",
    )
    screen.draw.text(
        f"Puntuación final: {puntuacion}",
        center=(WIDTH // 2, HEIGHT // 2 + 20),
        fontsize=32,
        color="white",
    )
    screen.draw.text(
        f"Mejor puntuación: {_mejor_puntuacion()}",
        center=(WIDTH // 2, HEIGHT // 2 + 65),
        fontsize=26,
        color="yellow",
    )
    screen.draw.text(
        "Presiona R para volver al menú",
        center=(WIDTH // 2, HEIGHT // 2 + 115),
        fontsize=20,
        color="lightgray",
    )


# ── Dibujar ───────────────────────────────────────────────────
def draw() -> None:
    if estado == MENU:
        _dibujar_menu()
        return

    screen.clear()
    fondo.draw()

    if fondo.image == MAP_WITH_BOAT:
        barco.draw()

    for enemigo in enemigos:
        enemigo.draw()

    prota.draw()
    _dibujar_hud()

    if estado == GAME_OVER:
        _dibujar_game_over()


# ── Movimiento de enemigos ────────────────────────────────────
def _mover_enemigos() -> None:
    for enemigo in enemigos:
        if prota.x > enemigo.x:
            enemigo.x += enemigo.speed
            enemigo.image = "skeletright"
        elif prota.x < enemigo.x:
            enemigo.x -= enemigo.speed
            enemigo.image = "skeletleft"

        if enemigo.colliderect(prota):
            enemigo.image = "ataque"
            prota.HP -= enemigo.AP * DAMAGE_RATE


# ── Ataque del jugador ────────────────────────────────────────
def _atacar() -> None:
    global puntuacion
    for enemigo in enemigos[:]:
        if prota.colliderect(enemigo):
            enemigo.HP -= prota.AP
            if enemigo.HP <= 0:
                enemigos.remove(enemigo)
                puntuacion += PUNTOS_ENEMIGO


# ── Cambio de mapa ────────────────────────────────────────────
def _cambiar_mapa(direccion: int) -> None:
    global _mapa_idx, puntuacion
    _mapa_idx = (_mapa_idx + direccion) % len(MAP_SEQUENCE)
    fondo.image = MAP_SEQUENCE[_mapa_idx]
    prota.x = SPAWN_LEFT if direccion > 0 else SPAWN_RIGHT
    enemigos.clear()
    enemigos.extend(crear_enemigos())
    puntuacion += PUNTOS_PANTALLA


# ── Reiniciar juego ───────────────────────────────────────────
def _reiniciar() -> None:
    global estado, _mapa_idx, puntuacion

    _mapa_idx  = 0
    puntuacion = 0
    estado     = MENU

    fondo.image = MAP_SEQUENCE[0]

    prota.x  = 100
    prota.y  = PLAYER_START_Y
    prota.HP = prota.maxHP

    enemigos.clear()
    enemigos.extend(crear_enemigos())


# ── Controles teclado ─────────────────────────────────────────
def on_key_down(key) -> None:
    if estado == GAME_OVER and key == keys.R:
        _reiniciar()
        return

    if estado != JUGANDO:
        return

    if key == keys.W:
        prota.y -= 50
        animate(prota, tween="bounce_end", duration=0.5, y=PLAYER_START_Y)

    if key == keys.SPACE:
        _atacar()


# ── Controles ratón ───────────────────────────────────────────
def on_mouse_down(pos) -> None:
    global estado
    if estado == MENU and _btn_rect.collidepoint(pos):
        estado = JUGANDO


# ── Update ────────────────────────────────────────────────────
def update() -> None:
    global estado

    if estado != JUGANDO:
        return

    # Movimiento del jugador
    if keyboard.A and prota.x > 0:
        prota.x -= 5
        prota.image = "left1"
    elif keyboard.D and prota.x < WIDTH:
        prota.x += 5
        prota.image = "right1"
    else:
        prota.image = "estandar1"

    # Transiciones de mapa
    if prota.x > BORDER_RIGHT:
        _cambiar_mapa(+1)
    elif prota.x < BORDER_LEFT:
        _cambiar_mapa(-1)

    # Game over
    if prota.HP <= 0:
        estado = GAME_OVER
        _guardar_puntuacion(puntuacion)

    _mover_enemigos()