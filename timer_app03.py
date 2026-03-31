import pygame
import sys
import time

# ------------------------------------------------------------------ #
# COSTANTI                                                             #
# ------------------------------------------------------------------ #

SCREEN_W = 800
SCREEN_H = 600
FPS      = 60

BALL_RADIUS  = 30
BALL_COLOR   = ( 80, 180, 220)
BALL_EXPIRED = ( 80,  80,  80)   # colore quando il tempo è scaduto

COUNTDOWN    = 10                # durata del conto alla rovescia (secondi)

BG_COLOR     = ( 30,  30,  30)
TEXT_COLOR   = (200, 200, 200)
BAR_BG_COLOR = ( 80,  40,  40)
BAR_FG_COLOR = ( 80, 200,  80)

BAR_X = 50
BAR_Y = 20
BAR_W = SCREEN_W - 100
BAR_H = 24

# ------------------------------------------------------------------ #
# INIZIALIZZAZIONE                                                     #
# ------------------------------------------------------------------ #

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Il timer")
clock  = pygame.time.Clock()
font_large  = pygame.font.SysFont("Arial", 48, bold=True)
font_medium = pygame.font.SysFont("Arial", 28)
font_small  = pygame.font.SysFont("Arial", 20)

# ------------------------------------------------------------------ #
# STATO                                                                #
# ------------------------------------------------------------------ #

ball_x     = SCREEN_W // 2
ball_y     = SCREEN_H // 2

# start_time viene impostato al momento dell'avvio del loop;
# lo usiamo per calcolare il tempo trascorso.
start_time = time.time()

# ------------------------------------------------------------------ #
# FUNZIONI — logica del timer                                          #
# ------------------------------------------------------------------ #

def time_elapsed(start: float) -> float:
    """
    TODO — Restituisce i secondi trascorsi da start fino ad ora
    come numero in virgola mobile.

    Parametri:
        start: il timestamp di riferimento (ottenuto con time.time())

    Suggerimento: time.time() restituisce i secondi dall'epoca Unix.
    La differenza tra due chiamate dà il tempo trascorso.
    """
    return time.time() - start


def time_remaining(start: float, duration: int) -> float:
    """
    TODO — Restituisce i secondi rimanenti rispetto a duration.
    Non deve mai restituire un valore negativo.

    Parametri:
        start:    timestamp di inizio
        duration: durata totale in secondi

    Suggerimento: usa time_elapsed() e poi sottrai da duration.
    Usa max() per impedire valori negativi.
    """
    return max(0.0, duration - time_elapsed(start))


def is_expired(start: float, duration: int) -> bool:
    """
    TODO — Restituisce True se il tempo è scaduto.

    Suggerimento: puoi usare time_remaining() oppure
    confrontare direttamente time_elapsed() con duration.
    """
    return time_remaining(start, duration) <= 0.0


def bar_fill_width(remaining: float, duration: int, bar_width: int) -> int:
    """
    TODO — Restituisce la larghezza in pixel della parte
    colorata della barra, proporzionale al tempo rimanente.

    Esempi (con duration=10, bar_width=700):
        remaining=10  → 700   (barra piena)
        remaining= 5  → 350   (barra a metà)
        remaining= 0  →   0   (barra vuota)

    Il risultato non deve mai essere negativo né superare bar_width.
    Suggerimento: calcola il rapporto remaining/duration,
    moltiplicalo per bar_width e converti a intero con int().
    Usa clamp() o max()/min() per i limiti.
    """
    return max(0, min(bar_width, int(remaining / duration * bar_width)))

# ------------------------------------------------------------------ #
# FUNZIONI — disegno                                                   #
# ------------------------------------------------------------------ #

def draw_timer_bar(surface: pygame.Surface,
                   remaining: float, duration: int):
    """
    TODO — Disegna la barra del timer.

    La barra è composta da due rettangoli sovrapposti:
      1. Sfondo (sempre pieno, colore BAR_BG_COLOR)
         Rect: (BAR_X, BAR_Y, BAR_W, BAR_H)
      2. Riempimento (larghezza proporzionale al tempo rimanente,
         colore BAR_FG_COLOR)
         Larghezza: usa bar_fill_width()

    Usa pygame.draw.rect(surface, colore, pygame.Rect(...))
    Aggiungi border_radius=6 per angoli arrotondati.
    Disegna prima lo sfondo, poi il riempimento sopra.
    """
    fill_width = bar_fill_width(remaining, duration, BAR_W)
    pygame.draw.rect(surface, BAR_BG_COLOR, pygame.Rect(BAR_X, BAR_Y, BAR_W, BAR_H), border_radius=6)
    pygame.draw.rect(surface, BAR_FG_COLOR, pygame.Rect(BAR_X, BAR_Y, fill_width, BAR_H), border_radius=6)


def draw_timer_text(surface: pygame.Surface,
                    remaining: float, expired: bool):
    """
    TODO — Disegna il numero dei secondi rimanenti.

    - Mostra i secondi come intero (usa int() o math.ceil())
    - Posiziona il testo centrato orizzontalmente,
      appena sotto la barra (BAR_Y + BAR_H + 10)
    - Se expired è True, mostra "Tempo scaduto!" al posto del numero
    - Usa font_medium per il numero, font_large per il messaggio
      di scadenza

    Suggerimento per centrare il testo:
        surf = font.render(testo, True, colore)
        rect = surf.get_rect(centerx=SCREEN_W // 2, top=y)
        surface.blit(surf, rect)
    """
    if expired:
        text = font_large.render("Tempo scaduto!", True, TEXT_COLOR)
        text_rect = text.get_rect(centerx=SCREEN_W // 2, top=BAR_Y + BAR_H + 10)
        surface.blit(text, text_rect)
    else:
        text = font_medium.render(str(int(remaining)), True, TEXT_COLOR)
        text_rect = text.get_rect(centerx=SCREEN_W // 2, top=BAR_Y + BAR_H + 10)
        surface.blit(text, text_rect)


def draw_ball(surface: pygame.Surface,
              x: int, y: int, expired: bool):
    """
    TODO — Disegna la pallina.

    - Se expired è False: usa BALL_COLOR
    - Se expired è True:  usa BALL_EXPIRED

    Usa pygame.draw.circle().
    """
    color = BALL_EXPIRED if expired else BALL_COLOR
    pygame.draw.circle(surface, color, (x, y), BALL_RADIUS)

# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                      #
# ------------------------------------------------------------------ #

running = True

while running:

    # ---- 1. EVENTI ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- 2. AGGIORNA ---------------------------------------------- #

    # Calcola lo stato del timer (già fornito: usa le tue funzioni)
    remaining = time_remaining(start_time, COUNTDOWN)
    expired   = is_expired(start_time, COUNTDOWN)

    # ---- 3. DISEGNA ----------------------------------------------- #

    screen.fill(BG_COLOR)

    draw_timer_bar(screen, remaining, COUNTDOWN)
    draw_timer_text(screen, remaining, expired)
    draw_ball(screen, ball_x, ball_y, expired)

    # Istruzione a schermo
    hint = font_small.render("Osserva la barra e il numero scendere...", True, TEXT_COLOR)
    screen.blit(hint, hint.get_rect(centerx=SCREEN_W // 2,
                                    bottom=SCREEN_H - 20))

    pygame.display.flip()
    clock.tick(FPS)

# ------------------------------------------------------------------ #
# USCITA                                                               #
# ------------------------------------------------------------------ #

pygame.quit()
sys.exit()
