import pygame
import sys

# ------------------------------------------------------------------ #
# COSTANTI                                                             #
# ------------------------------------------------------------------ #

SCREEN_W = 800
SCREEN_H = 600
FPS      = 60

BALL_RADIUS = 30
BALL_SPEED  = 4          # pixel per frame (tastiera)

BG_COLOR   = ( 30,  30,  30)
TEXT_COLOR = (200, 200, 200)

# Colori disponibili per il cambio al clic
COLORS = [
    (220,  80,  80),   # rosso
    ( 80, 180, 220),   # azzurro
    ( 80, 220, 120),   # verde
    (220, 200,  80),   # giallo
    (180,  80, 220),   # viola
]

# ------------------------------------------------------------------ #
# INIZIALIZZAZIONE                                                     #
# ------------------------------------------------------------------ #

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Pallina interattiva")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 22)

# ------------------------------------------------------------------ #
# STATO                                                                #
# ------------------------------------------------------------------ #

ball_x      = SCREEN_W // 2
ball_y      = SCREEN_H // 2
color_index = 0                      # indice corrente in COLORS
ball_color  = COLORS[color_index]

# ------------------------------------------------------------------ #
# FUNZIONI DI SUPPORTO                                                 #
# ------------------------------------------------------------------ #

def clamp(value: int, min_val: int, max_val: int) -> int:
    """
    Restituisce value se è compreso tra min_val e max_val,
    altrimenti restituisce il limite più vicino.

    Esempi:
        clamp(10, 0, 100)  → 10
        clamp(-5, 0, 100)  → 0
        clamp(150, 0, 100) → 100
    """
    return max(min_val, min(value, max_val))


def point_in_circle(px: int, py: int,
                    cx: int, cy: int, radius: int) -> bool:
    """
    TODO — Restituisce True se il punto (px, py) si trova
    all'interno del cerchio con centro (cx, cy) e raggio radius.

    Suggerimento: usa il teorema di Pitagora per calcolare
    la distanza tra il punto e il centro, poi confrontala
    con il raggio.
    Ricorda: puoi evitare la radice quadrata confrontando
    i quadrati delle distanze.
    """
    dx = px - cx 
    dy = py - cy
    return dx * dx + dy * dy <= radius * radius


def next_color(current_index: int) -> tuple:
    """
    TODO — Restituisce la tupla (nuovo_indice, nuovo_colore)
    passando al colore successivo nella lista COLORS.
    Quando si raggiunge l'ultimo colore si riparte dal primo
    (comportamento circolare).

    Parametri:
        current_index: indice attuale in COLORS

    Valore restituito:
        una tupla (int, tuple) con il nuovo indice e il colore
        corrispondente.

    Suggerimento: l'operatore % (modulo) è utile per il
    comportamento circolare.
    """
    next_index = (current_index + 1) % len(COLORS)
    return next_index, COLORS[next_index]

# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                      #
# ------------------------------------------------------------------ #

running = True

while running:

    # ---- 1. EVENTI ------------------------------------------------ #

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # -- Clic del mouse --
        # TODO — Gestisci l'evento pygame.MOUSEBUTTONDOWN:
        #   - controlla che sia il tasto sinistro (event.button == 1)
        #   - usa point_in_circle() per verificare se il clic
        #     è avvenuto dentro la pallina
        #   - se sì, chiama next_color() e aggiorna
        #     color_index e ball_color
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if point_in_circle(event.pos[0], event.pos[1], ball_x, ball_y, BALL_RADIUS):
                    color_index, ball_color = next_color(color_index)


    # ---- 2. AGGIORNA ---------------------------------------------- #

    # -- Tastiera --
    # pygame.key.get_pressed() restituisce una sequenza di booleani
    # indicizzata dai codici dei tasti. Esempio:
    #   keys[pygame.K_LEFT]  → True se il tasto ← è premuto ora
    #
    # A differenza degli eventi (che arrivano una volta sola),
    # get_pressed() fotografa lo stato istantaneo della tastiera
    # ed è pensato per il movimento continuo.

    keys = pygame.key.get_pressed()

    # TODO — Muovi la pallina in base ai tasti freccia (o WASD):
    #   - freccia sinistra / A  → ball_x -= BALL_SPEED
    #   - freccia destra  / D  → ball_x += BALL_SPEED
    #   - freccia su      / W  → ball_y -= BALL_SPEED
    #   - freccia giù     / S  → ball_y += BALL_SPEED
    #
    # Dopo aver aggiornato la posizione, usa clamp() per impedire
    # alla pallina di uscire dallo schermo. Ricorda di tenere conto
    # di BALL_RADIUS!
    #   ball_x = clamp(ball_x, ..., ...)
    #   ball_y = clamp(ball_y, ..., ...)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= BALL_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ball_x += BALL_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        ball_y -= BALL_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ball_y += BALL_SPEED


    # ---- 3. DISEGNA ----------------------------------------------- #

    screen.fill(BG_COLOR)

    # TODO — Disegna la pallina con pygame.draw.circle().
    # Usa ball_color come colore e BALL_RADIUS come raggio.
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), BALL_RADIUS)

    # HUD: istruzioni a schermo (già fornito)
    hints = [
        "Frecce / WASD: muovi la pallina",
        "Clic sinistro sulla pallina: cambia colore",
    ]
    for i, line in enumerate(hints):
        surf = font.render(line, True, TEXT_COLOR)
        screen.blit(surf, (10, 10 + i * 28))

    pygame.display.flip()
    clock.tick(FPS)

# ------------------------------------------------------------------ #
# USCITA                                                               #
# ------------------------------------------------------------------ #

pygame.quit()
sys.exit()
