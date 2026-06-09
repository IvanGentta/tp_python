import pygame
import sys

def mostrar_instrucciones(pantalla, reloj):
    # 1. Cargamos las 6 imágenes en una lista
    imagenes = []
    for i in range (1, 7):
        imagenes += [pygame.image.load(f"instrucciones/{i}.jpg").convert()]
    
    # 2. Variables de control
    indice_actual = 0
    leyendo_instrucciones = True
    
    # 3. El Bucle de la Pantalla de Instrucciones
    while leyendo_instrucciones:
        
        # --- DETECCIÓN DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Si el jugador hace clic o presiona la barra ESPACIO
            if evento.type == pygame.MOUSEBUTTONDOWN or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE):
                indice_actual += 1 # Avanzamos a la siguiente imagen
                
                # Si ya pasamos la imagen número 6, salimos del bucle para volver al menú
                if indice_actual >= len(imagenes):
                    leyendo_instrucciones = False
                    
        # --- DIBUJO ---
        pantalla.fill((20, 20, 20))
        
        # Dibujamos la imagen correspondiente al índice actual
        if indice_actual < len(imagenes):
            # Opcional: Centrar la imagen si es más pequeña que 1200x900
            rect_img = imagenes[indice_actual].get_rect(center=(600, 450))
            pantalla.blit(imagenes[indice_actual], rect_img)
            
        pygame.display.flip()
        reloj.tick(60)