import pygame
import sys

# Inicializa todos los módulos de pygame
pygame.init()

# Ancho y alto de la ventana
ANCHO = 1000
ALTO = 700

# Crea la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
# Titulo ventana
pygame.display.set_caption("Maestro Parrillero")

# FPS?
reloj = pygame.time.Clock()

# Fuentes
fuente_titulo = pygame.font.SysFont("arial", 60, bold=True)
fuente_boton = pygame.font.SysFont("arial", 40)

# Botones Parámetros: (pos_x, pos_y, ancho, alto)
boton_jugar = pygame.Rect(350, 200, 350, 90)
boton_instrucciones = pygame.Rect(350, 350, 350, 90)
boton_salir = pygame.Rect(350, 500, 350, 90)

# Variable que controla el bucle principal
# Mientras sea True el programa sigue abierto
ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if boton_jugar.collidepoint(evento.pos):
                print("Iniciar juego")

            if boton_salir.collidepoint(evento.pos):
                ejecutando = False

    # Fondo
    pantalla.fill((160, 139, 34))

    # Título
    titulo = fuente_titulo.render(
        "MAESTRO PARRILLERO",
        True,
        (255, 255, 255)
    )

    rect_titulo = titulo.get_rect(
        center=(ANCHO // 2, 90)
    )

    pantalla.blit(
        titulo,
        rect_titulo
    )

    ANCHO_BOTON = 350
    ALTO_BOTON = 90

    # Botón jugar
    pygame.draw.rect(
        pantalla,
        (200, 200, 200),
        boton_jugar,
        border_radius=10
    )

    texto_jugar = fuente_boton.render(
        "JUGAR",
        True,
        (0, 0, 0)
    )

    rect_texto_jugar = texto_jugar.get_rect(
        center=boton_jugar.center
    )

    pantalla.blit(
        texto_jugar,
        rect_texto_jugar
    )

    # Botón instrucciones
    pygame.draw.rect(
        pantalla,
        (200, 200, 200),
        boton_instrucciones,
        border_radius=10
    )

    texto_instrucciones = fuente_boton.render(
        "INSTRUCCIONES",
        True,
        (0, 0, 0)
    )

    rect_texto_instrucciones = texto_instrucciones.get_rect(
        center=boton_instrucciones.center
    )

    pantalla.blit(
        texto_instrucciones,
        rect_texto_instrucciones
    )

    # Botón salir
    pygame.draw.rect(
        pantalla,
        (200, 200, 200),
        boton_salir,
        border_radius=10
    )

    texto_salir = fuente_boton.render(
        "SALIR",
        True,
        (0, 0, 0)
    )

    rect_texto_salir = texto_salir.get_rect(
        center=boton_salir.center
    )

    pantalla.blit(
        texto_salir,
        rect_texto_salir
    )

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()