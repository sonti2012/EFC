# ── Configuración de la ventana ───────────────────────────────
WIDTH  = 550
HEIGHT = 600
TITLE  = "Escape de las cuevas"
FPS    = 30

# ── Posición del jugador ──────────────────────────────────────
PLAYER_START_X = 100
PLAYER_START_Y = 280
PLAYER_AP      = 20
PLAYER_HP      = 100

# ── Enemigos ──────────────────────────────────────────────────
ENEMY_COUNT_MIN = 2
ENEMY_COUNT_MAX = 5
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 4
ENEMY_HP_MIN    = 40
ENEMY_HP_MAX    = 70
ENEMY_AP_MIN    = 5
ENEMY_AP_MAX    = 10
ENEMY_START_Y   = 290
ENEMY_SPAWN_X_MIN = -100
ENEMY_SPAWN_X_MAX = -50

# ── Daño por contacto (por frame) ─────────────────────────────
DAMAGE_RATE = 0.02

# ── Bordes de transición de mapa ─────────────────────────────
BORDER_RIGHT = 530
BORDER_LEFT  = 20
SPAWN_LEFT   = 50   # debe ser > BORDER_LEFT para no re-disparar transición
SPAWN_RIGHT  = 500  # debe ser < BORDER_RIGHT para no re-disparar transición

# ── Secuencia de mapas (izquierda → derecha) ──────────────────
MAP_SEQUENCE  = ["background", "background2", "background4", "background3"]
MAP_WITH_BOAT = "background3"

# ── Puntuación ────────────────────────────────────────────────
PUNTOS_ENEMIGO  = 20
PUNTOS_PANTALLA = 20
SCORES_FILE     = "scores.txt"
