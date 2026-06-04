import pygame
import sys

def iniciar_juego():

    ANCHO = 1200
    ALTO = 900

    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    fondo = pygame.image.load(
        "img/patio.png"
    ).convert()

    carbon = pygame.image.load(
        "img/carbon.png"
    ).convert_alpha()

    parrilla = pygame.image.load(
        "img/parrilla_media.png"
    ).convert_alpha()

    carbon = pygame.transform.scale(carbon, (164, 242))
    parrilla = pygame.transform.scale(parrilla, (972, 700))

    fondo = pygame.transform.scale(
        fondo,
        (ANCHO, ALTO)
    )

    reloj = pygame.time.Clock()

    ejecutando = True

    while ejecutando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(carbon, (1020, 650))
        pantalla.blit(parrilla, (10, 190))

        pygame.display.flip()
        reloj.tick(60)