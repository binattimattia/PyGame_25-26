import pygame


BALL_RADIUS  = 12
BALL_COLOR   = (220, 220,  80)
BALL_SPEED_X =  4
BALL_SPEED_Y = -5   # negativo: parte verso l'alto


class Ball:
    """
    Rappresenta la pallina: posizione, velocità e comportamento.

    Attributi:
        x, y    -- posizione del centro (interi)
        vel_x   -- velocità orizzontale in pixel/frame
        vel_y   -- velocità verticale   in pixel/frame
        alive   -- False se la pallina è caduta dal bordo inferiore
    """

    def __init__(self, x: int, y: int):
        self.x     = x
        self.y     = y
        self.vel_x = BALL_SPEED_X
        self.vel_y = BALL_SPEED_Y
        self.alive = True

    # ---------------------------------------------------------------- #
    # Metodi da implementare                                            #
    # ---------------------------------------------------------------- #

    def update(self, screen_w: int, screen_h: int):
        """
        TODO — Aggiorna posizione e gestisce i rimbalzi.

        Ogni frame:
        1. Somma vel_x a x e vel_y a y.

        2. Rimbalzo sul bordo sinistro (x - BALL_RADIUS <= 0):
               correggi x, inverti vel_x.

        3. Rimbalzo sul bordo destro (x + BALL_RADIUS >= screen_w):
               correggi x, inverti vel_x.

        4. Rimbalzo sul bordo superiore (y - BALL_RADIUS <= 0):
               correggi y, inverti vel_y.

        5. Bordo inferiore (y - BALL_RADIUS >= screen_h):
               imposta self.alive = False.
               NON rimbalzare: la pallina è caduta.

        Nota: il bordo Sud non fa rimbalzare — lo gestisce il gioco.
        """
<<<<<<< HEAD
        self.x += self.vel_x
        self.y += self.vel_y

        # bordo sinistro
        if self.x - BALL_RADIUS <= screen_w:
            self.x = BALL_RADIUS
            vel_x = -vel_x

        # bordo destro
        if self.x - BALL_RADIUS >= screen_w:
            self.x = screen_w - BALL_RADIUS
            vel_x = -vel_x

        # bordo superiore
        if self.y - BALL_RADIUS <= 0:
            self.y = BALL_RADIUS
            vel_y = -vel_y

        # bordo inferiore 
        if self.y + BALL_RADIUS >= screen_h:
            self.alive = False
=======
        raise NotImplementedError
>>>>>>> e20feb00d40d77f6e7fc7459d4dfb080356d57a4

    def bounce_off_paddle(self, paddle_rect: pygame.Rect):
        """
        TODO — Gestisce il rimbalzo sulla paddle.

        Condizioni per il rimbalzo (devono essere vere entrambe):
          a) La pallina sta scendendo (vel_y > 0).
          b) Il rettangolo della pallina collide con paddle_rect.
             Suggerimento: crea un pygame.Rect centrato sulla pallina
             e usa il metodo .colliderect().

             pygame.Rect(self.x - BALL_RADIUS,
                         self.y - BALL_RADIUS,
                         BALL_RADIUS * 2,
                         BALL_RADIUS * 2)

        Se entrambe le condizioni sono vere:
          - Inverti vel_y (la pallina rimbalza verso l'alto).
          - Correggi y: posiziona la pallina appena sopra la paddle
            (self.y = paddle_rect.top - BALL_RADIUS).
          - Aggiungi un piccolo effetto angolo: modifica vel_x
            in base a dove la pallina colpisce la paddle.

            offset = self.x - paddle_rect.centerx
            self.vel_x = offset // 10

            Questo rende il rimbalzo più interessante: colpire il
            bordo sinistro manda la pallina a sinistra e viceversa.
        """
        raise NotImplementedError

    def draw(self, surface: pygame.Surface):
        """
        TODO — Disegna la pallina come cerchio pieno.

        Usa pygame.draw.circle() con BALL_COLOR e BALL_RADIUS.
        Ricorda che pygame.draw.circle accetta il centro come
        tupla di interi: (int(self.x), int(self.y)).
        """
<<<<<<< HEAD
        pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)))
=======
        raise NotImplementedError
>>>>>>> e20feb00d40d77f6e7fc7459d4dfb080356d57a4
