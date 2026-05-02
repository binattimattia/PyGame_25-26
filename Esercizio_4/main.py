import pygame
import sys
import time

from ball   import Ball
from paddle import Paddle

# ------------------------------------------------------------------ #
# COSTANTI                                                             #
# ------------------------------------------------------------------ #

SCREEN_W  = 800
SCREEN_H  = 600
FPS       = 60

COUNTDOWN = 60        # secondi per vincere
MAX_LIVES =  3        # vite iniziali

BG_COLOR      = ( 20,  20,  40)
TEXT_COLOR    = (220, 220, 220)
COLOR_WIN     = ( 80, 220, 120)
COLOR_LOSE    = (220,  80,  80)

# ------------------------------------------------------------------ #
# INIZIALIZZAZIONE                                                     #
# ------------------------------------------------------------------ #

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Non farcela cadere!")
clock      = pygame.time.Clock()
font_large  = pygame.font.SysFont("Arial", 56, bold=True)
font_medium = pygame.font.SysFont("Arial", 30)
font_small  = pygame.font.SysFont("Arial", 20)

# ------------------------------------------------------------------ #
# CARICAMENTO SPRITE CUORE                                             #
# ------------------------------------------------------------------ #

def load_heart(size: int = 28) -> pygame.Surface:
    """
    Carica heart.png dalla cartella assets/ e la ridimensiona.
    Se il file non esiste usa un cerchio rosso come placeholder.
    """
    import os
    path = os.path.join(os.path.dirname(__file__), "assets", "heart.png")
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (size, size))
    # Placeholder: cerchio rosso su superficie trasparente
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (220, 60, 60), (size // 2, size // 2), size // 2)
    return surf

heart_img = load_heart()

# ------------------------------------------------------------------ #
# FUNZIONI — timer (già viste nella tappa 3)                          #
# ------------------------------------------------------------------ #

def time_remaining(start: float, duration: int) -> float:
    return max(0.0, duration - (time.time() - start))

def is_expired(start: float, duration: int) -> bool:
    return time.time() - start >= duration

# ------------------------------------------------------------------ #
# FUNZIONI — disegno HUD                                              #
# ------------------------------------------------------------------ #

def draw_hud(surface: pygame.Surface, remaining: float, lives: int):
    """
    TODO — Disegna il HUD (heads-up display) in cima allo schermo.

    Deve mostrare:
    1. Il timer: il numero di secondi rimanenti, centrato in alto.
       Usa font_medium e TEXT_COLOR.
       Suggerimento: surf.get_rect(centerx=SCREEN_W // 2, top=10)

    2. Le vite: disegna tante copie di heart_img quante sono le vite
       rimaste, allineate in alto a destra.
       Suggerimento: per ogni i in range(lives) calcola la x
       partendo da destra. La larghezza di heart_img è heart_img.get_width().

       Esempio con lives=3 e margine=10:
           x = SCREEN_W - 10 - (i + 1) * (heart_img.get_width() + 4)
           surface.blit(heart_img, (x, 10))
    """
    timer_text = str(int(remaining))
    timer_surf = font_medium.render(timer_text, True, TEXT_COLOR)
    timer_rect = timer_surf.get_rect(centerx=SCREEN_W // 2, top=10)
    surface.blit(timer_surf, timer_rect)

    margin = 10  # Margine dal bordo destro
    spacing = 4  # Spazio tra un cuore e l'altro
    heart_w = heart_img.get_width()

    for i in range(lives):
        x = SCREEN_W - margin - (i + 1) * (heart_w + spacing)
        y = 10
        surface.blit(heart_img, (x, y))


def draw_timer_bar(surface: pygame.Surface,
                   remaining: float, duration: int):
    """
    TODO — Disegna la barra del timer sotto il testo del countdown.
    Riusa la logica della tappa 3:
      - Sfondo: Rect(50, 48, SCREEN_W - 100, 10), colore (80, 40, 40)
      - Riempimento: larghezza proporzionale a remaining/duration,
        colore (80, 200, 80), stessa altezza e y.
    Usa border_radius=4.
    """
    bg_rect = pygame.Rect(50, 48, SCREEN_W - 100, 10)
    pygame.draw.rect(surface, (80, 40, 40), bg_rect, border_radius=4)


def draw_end_screen(surface: pygame.Surface, won: bool):
    """Schermata finale — già fornita."""
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    msg   = "Hai vinto!" if won else "Hai perso!"
    color = COLOR_WIN    if won else COLOR_LOSE
    surf  = font_large.render(msg, True, color)
    surface.blit(surf, surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 40)))

    hint = font_medium.render("Premi R per rigiocare", True, TEXT_COLOR)
    surface.blit(hint, hint.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40)))

# ------------------------------------------------------------------ #
# FUNZIONE — reset partita                                             #
# ------------------------------------------------------------------ #

def reset_game():
    """
    TODO — Crea e restituisce lo stato iniziale della partita:
    (ball, paddle, start_time, lives).

    - ball:       nuova istanza di Ball, centrata orizzontalmente
                  e a 2/3 dell'altezza dello schermo.
    - paddle:     nuova istanza di Paddle.
    - start_time: timestamp attuale (time.time()).
    - lives:      MAX_LIVES.

    Restituisci una tupla: (ball, paddle, start_time, lives)
    """
    ball = Ball(SCREEN_W // 2, SCREEN_H * 2 // 3)
    paddle = Paddle(SCREEN_W, SCREEN_H)
    start_time = time.time()
    lives = MAX_LIVES

    return ball, paddle, start_time, lives

# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                      #
# ------------------------------------------------------------------ #

# TODO — Chiama reset_game() per ottenere lo stato iniziale.
# Decomponi la tupla restituita in quattro variabili:
#   ball, paddle, start_time, lives = reset_game()
#
# Poi dichiara: game_over = False

ball, paddle, start_time, lives = reset_game()
game_over = False
won = False

running = True

while running:

    # ---- 1. EVENTI ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TODO — Gestisci il tasto R per rigiocare:
        # se game_over è True e viene premuto pygame.K_r,
        # chiama reset_game() e reimposta tutte le variabili di stato,
        # incluso game_over = False.
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                ball, paddle, start_time, lives = reset_game()
                game_over = False

    # ---- 2. AGGIORNA ---------------------------------------------- #

    # TODO — Se game_over è False:
    #
    # a) Leggi i tasti con pygame.key.get_pressed() e chiama
    #    paddle.update(keys).
    #
    # b) Chiama ball.update(SCREEN_W, SCREEN_H).
    #
    # c) Chiama ball.bounce_off_paddle(paddle.rect).
    #
    # d) Se ball.alive è diventato False (la pallina è caduta):
    #      - Sottrai 1 a lives.
    #      - Se lives > 0: ricrea solo la pallina (ball = Ball(...))
    #        senza resettare il timer o le vite.
    #      - Se lives == 0: imposta game_over = True.
    #
    # e) Se is_expired(start_time, COUNTDOWN): imposta game_over = True.
    #
    # Suggerimento: won = is_expired(start_time, COUNTDOWN) and lives > 0
    # ti serve per sapere se mostrare "Hai vinto" o "Hai perso".
    if not game_over:
        keys = pygame.key.get_pressed()
        paddle.update(keys)

        ball.update(SCREEN_W, SCREEN_H)

        ball.bounce_off_paddle(paddle.rect)

        if not ball.alive:
            lives -= 1
            if lives > 0:
                ball = Ball(SCREEN_W // 2, SCREEN_H * 2 // 3)
            if lives == 0:
                game_over = True
        
        if is_expired(start_time, COUNTDOWN):
            game_over = True
            won = True

    # ---- 3. DISEGNA ----------------------------------------------- #

    screen.fill(BG_COLOR)

    # TODO — Chiama draw_hud(), draw_timer_bar(), paddle.draw(),
    # ball.draw() nell'ordine corretto.
    # Se game_over è True, chiama anche draw_end_screen(screen, won).
    rem = time_remaining(start_time, COUNTDOWN)
    draw_hud(screen, rem, lives)
    draw_timer_bar(screen, rem, COUNTDOWN)
    paddle.draw(screen)
    ball.draw(screen)

    if game_over:
        draw_end_screen(screen, won)


    pygame.display.flip()
    clock.tick(FPS)

# ------------------------------------------------------------------ #
# USCITA                                                               #
# ------------------------------------------------------------------ #

pygame.quit()
sys.exit()
