import pygame
import sys
import random
from carnes import crear_carne_aleatoria, actualizar_logica_carnes, voltear_carne, precargar_imagenes_carnes

def iniciar_juego():

    ANCHO = 1200
    ALTO = 900
    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    # Precargamos los imagenes una sola vez en la memoria
    precargar_imagenes_carnes()
    fondo = pygame.image.load("img/patio.png").convert()
    carbon = pygame.image.load("img/carbon.png").convert_alpha()
    parrilla = pygame.image.load("img/parrilla_media.png").convert_alpha()
    img_quemada = pygame.image.load("img/quemado.png").convert_alpha()
    
    carbon = pygame.transform.scale(carbon, (164, 242))
    parrilla = pygame.transform.scale(parrilla, (972, 700))
    fondo = pygame.transform.scale(fondo,(ANCHO, ALTO))

    reloj = pygame.time.Clock()

    # --- CONFIGURACIÓN DE LOS SLOTS SUPERIORES ---
    # Guardamos las coordenadas X fijas de cada uno de los 4 slots de preparación
    slots_preparacion = [
        {"x": 175, "y": 100, "ocupado": False},
        {"x": 375, "y": 100, "ocupado": False},
        {"x": 575, "y": 100, "ocupado": False},
        {"x": 825, "y": 100, "ocupado": False}
    ]
    
    # --- CONFIGURACIÓN DE LA PARRILLA ---
    puestos_parrilla = [
        {"x": 175, "y": 750, "ocupado": False},
        {"x": 375, "y": 750, "ocupado": False},
        {"x": 575, "y": 750, "ocupado": False},
        {"x": 825, "y": 750, "ocupado": False},
        
        {"x": 175, "y": 550, "ocupado": False},
        {"x": 375, "y": 550, "ocupado": False},
        {"x": 575, "y": 550, "ocupado": False},
        {"x": 825, "y": 550, "ocupado": False},
        
        {"x": 175, "y": 350, "ocupado": False},
        {"x": 375, "y": 350, "ocupado": False},
        {"x": 575, "y": 350, "ocupado": False},
        {"x": 825, "y": 350, "ocupado": False}
    ]
    
    # Lista dinámica donde se guardarán todas las carnes que están vivas en pantalla
    carnes_activas = []
    
    # Al empezar el juego rellenamos los 4 slots inmediatamente para arrancar con comida
    for i in range(4):
        nueva_carne = crear_carne_aleatoria(slots_preparacion[i]["x"], slots_preparacion[i]["y"], i)
        carnes_activas.append(nueva_carne)
        slots_preparacion[i]["ocupado"] = True

    # --- TEMPORIZADOR DE GENERACIÓN INFINITA ---
    # Definimos en cuántos segundos se generará el próximo alimento (entre 5.0 y 10.0)
    timer_generacion = random.uniform(2.5, 6.5)

    ejecutando = True

    while ejecutando:
        
        # Calculamos el delta time (dt) para manejar el tiempo real de cocción
        dt = reloj.tick(60) / 1000.0    # Tiempo en fracciones de segundo
        
        # --- LÓGICA DE GENERACIÓN AUTOMÁTICA DE CARNES ---
        timer_generacion -= dt
        if timer_generacion <= 0:
            # Buscamos qué slots superiores están vacíos actualmente
            slots_libres = [i for i, s in enumerate(slots_preparacion) if not s["ocupado"]]
            
            # Si hay al menos un slot vacío arriba, generamos una carne
            if slots_libres:
                slot_elegido_idx = random.choice(slots_libres) # Elegimos un slot vacío al azar
                slot = slots_preparacion[slot_elegido_idx]
                
                # Creamos de forma infinita una carne aleatoria y la sumamos al juego
                nueva_carne = crear_carne_aleatoria(slot["x"], slot["y"], slot_elegido_idx)
                carnes_activas.append(nueva_carne)
                slot["ocupado"] = True
                print(f"--> ¡Apareció un nuevo {nueva_carne['nombre']} en el slot {slot_elegido_idx + 1}!")
                
            # Reiniciamos el temporizador con otro tiempo al azar entre 5 y 10 segundos
            timer_generacion = random.uniform(2.5, 6.5)
        
        # --- DETECCIÓN DE EVENTOS DE CLIC ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for carne in carnes_activas:
                    if carne["rect"].collidepoint(evento.pos):
                        
                        # CASO A: El jugador clickea una carne de ARRIBA para bajarla
                        if carne["ubicacion"] == "slots":
                            # Buscamos lugar libre en la parrilla caliente
                            for puesto in puestos_parrilla:
                                if not puesto["ocupado"]:
                                    # Movemos visualmente el rect abajo
                                    carne["rect"].center = (puesto["x"], puesto["y"])
                                    carne["ubicacion"] = "parrilla"
                                    puesto["ocupado"] = True
                                    
                                    # CRUCIAL: Liberamos el slot superior donde estaba para que pueda nacer otra carne ahí
                                    idx_slot_viejo = carne["slot_origen"]
                                    slots_preparacion[idx_slot_viejo]["ocupado"] = False
                                    break
                                    
                        # CASO B: Clickea una carne que ya está ABAJO (Lógica para voltear)
                        elif carne["ubicacion"] == "parrilla":
                            voltear_carne(carne)
                        
                        #CASO C: Clickea una carne para servir
                        #elif carne["ubicacion"] == "parrilla":
                            #servir(carne)
                        
                        #CASO D: Clickea una carne quemada para desechar
                        #elif carne["ubicacion"] == "parrilla":
                            #remover(carne)
        
        # --- ACTUALIZACIÓN ---
        actualizar_logica_carnes(carnes_activas, dt)
        
        # --- DIBUJO ---
        pantalla.fill((40, 40, 40))
        
        # 1. PRIMERO DIBUJAMOS EL FONDO (La capa más profunda)
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(carbon, (1020, 650))
        pantalla.blit(parrilla, (10, 190))
        
        # Dibujamos visualmente las siluetas fijas de los 4 slots de arriba
        for s in slots_preparacion:
            pygame.draw.rect(pantalla, (60, 60, 60), (s["x"] - 50, s["y"] - 50, 100, 100), 2, border_radius=5)
            
                
        # Renderizado de las carnes activas en pantalla
        for carne in carnes_activas:
            if carne["estado_crudo"]:
                pantalla.blit(carne["img_cruda"], carne["rect"])
            elif carne["estado_cocido"]:
                pantalla.blit(carne["img_cocida"], carne["rect"])
            elif carne["estado_crudo"] == False and carne["estado_cocido"] == False:
                # Dibujo de comida quemada
                pantalla.blit(img_quemada, carne["rect"])
            
            # Barras de cocción 
            if carne["ubicacion"] == "parrilla" and carne["puntaje_coccion"] > 0:
                ancho_total_barra = 100
                ancho_actual = (carne["puntaje_coccion"] / carne["puntaje_maximo"]) * ancho_total_barra
                
                x_barra = carne["rect"].x
                y_barra = carne["rect"].y - 15
                
                # Color de fondo de barra
                pygame.draw.rect(pantalla, (128, 0, 0), (x_barra, y_barra, ancho_total_barra, 8))
                #Color de coccion buena
                color_barra = (0, 255, 0)
                #Color de alerta
                if carne["puntaje_coccion"] >= (carne["puntaje_maximo"] / 2) and not carne["lado_b"]:
                    color_barra = (255, 200, 0)
                elif carne["puntaje_coccion"] >= (carne["puntaje_maximo"]):
                    color_barra = (255, 200, 0)
                    
                pygame.draw.rect(pantalla, color_barra, (x_barra, y_barra, ancho_actual, 8))
        

        pygame.display.flip()
        reloj.tick(60)