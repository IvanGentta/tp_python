import pygame
import sys
from puntajes import cargar_puntajes


def mostrar_highscores(pantalla, reloj):
    """Muestra la pantalla de High Scores. Vuelve al menú al presionar el botón."""

    ANCHO = 1200
    ALTO = 900

    fuente_titulo = pygame.font.SysFont("arial", 70, bold=True)
    fuente_entrada = pygame.font.SysFont("arial", 38)
    fuente_boton = pygame.font.SysFont("arial", 40)
    fuente_vacio = pygame.font.SysFont("arial", 34)

    boton_volver = pygame.Rect(430, 760, 350, 80)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return  # Vuelve al menú

        puntajes = cargar_puntajes()

        pantalla.fill((20, 20, 20))

        # Título
        titulo = fuente_titulo.render("HIGH SCORES", True, (255, 215, 0))
        sombra = fuente_titulo.render("HIGH SCORES", True, (0, 0, 0))
        pantalla.blit(sombra, sombra.get_rect(center=(ANCHO // 2 + 3, 70 + 3)))
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 70)))

        # Línea separadora
        pygame.draw.line(pantalla, (255, 215, 0), (200, 120), (1000, 120), 2)

        if not puntajes:
            texto = fuente_vacio.render("Todavía no hay puntajes guardados.", True, (180, 180, 180))
            pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, 400)))
        else:
            for i, entrada in enumerate(puntajes):
                y = 150 + i * 58

                # Medalla para el top 3
                if i == 0:
                    color_pos = (255, 215, 0)    # oro
                elif i == 1:
                    color_pos = (192, 192, 192)  # plata
                elif i == 2:
                    color_pos = (205, 127, 50)   # bronce
                else:
                    color_pos = (200, 200, 200)

                # Número de posición
                texto_pos = fuente_entrada.render(f"{i + 1}.", True, color_pos)
                pantalla.blit(texto_pos, (220, y))

                # Nombre
                texto_nombre = fuente_entrada.render(entrada["nombre"], True, (255, 255, 255))
                pantalla.blit(texto_nombre, (300, y))

                # Puntaje alineado a la derecha
                texto_puntaje = fuente_entrada.render(str(entrada["puntaje"]), True, color_pos)
                pantalla.blit(texto_puntaje, texto_puntaje.get_rect(right=980, y=y))

                # Línea separadora entre entradas
                pygame.draw.line(pantalla, (60, 60, 60), (200, y + 48), (1000, y + 48), 1)

        # Botón volver
        pygame.draw.rect(pantalla, (200, 200, 200), boton_volver, border_radius=10)
        texto_volver = fuente_boton.render("VOLVER", True, (0, 0, 0))
        pantalla.blit(texto_volver, texto_volver.get_rect(center=boton_volver.center))

        pygame.display.flip()
        reloj.tick(60)
