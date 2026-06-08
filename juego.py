import pygame
import sys
import random
from carnes import precarga_imagenes_carnes, spawnear_carne, actualizar_logica_carnes, voltear_carne, chamuscar, servir, remover

def iniciar_juego(sonidos):

    ANCHO = 1200
    ALTO = 900
    pantalla = pygame.display.set_mode((ANCHO, ALTO))

<<<<<<< HEAD
    fondo = pygame.image.load("img/patio.png").convert()
    carbon = pygame.image.load("img/carbon.png").convert_alpha()
    parrilla = pygame.image.load("img/parrilla_media.png").convert_alpha()

    carbon = pygame.transform.scale(carbon, (164, 242))
    parrilla = pygame.transform.scale(parrilla, (972, 700))
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    reloj = pygame.time.Clock()

    # Cambia la música al entrar al juego
    sonidos.reproducir_musica("juego")
=======
    # Precargamos los imagenes una sola vez en la memoria
    precarga_imagenes_carnes()
    fondo = pygame.image.load("img/patio.png").convert()
    carbon = pygame.image.load("img/carbon.png").convert_alpha()
    fuego_alto = pygame.image.load("img/parrilla_alta.png").convert_alpha()
    fuego_medio = pygame.image.load("img/parrilla_media.png").convert_alpha()
    fuego_bajo = pygame.image.load("img/parrilla_baja.png").convert_alpha()
    img_quemada = pygame.image.load("img/ceniza.png").convert_alpha()
    
    carbon = pygame.transform.scale(carbon, (164, 242))
    fuego_alto = pygame.transform.scale(fuego_alto, (972, 700))
    fuego_medio = pygame.transform.scale(fuego_medio, (972, 700))
    fuego_bajo = pygame.transform.scale(fuego_bajo, (972, 700))
    fondo = pygame.transform.scale(fondo,(ANCHO, ALTO))
	
	# Lista dinamica de jugador donde se guardan los puntos:
    jugador = {"nombre": "", "resultado": 0.0}
	
    reloj = pygame.time.Clock()

    # --- CONFIGURACIÓN DE LOS SLOTS SUPERIORES ---
    # Guardamos las coordenadas X fijas de cada uno de los 4 slots de preparación
    slots_spawn = [
        {"x": 175, "y": 100, "en_uso": False},
        {"x": 375, "y": 100, "en_uso": False},
        {"x": 575, "y": 100, "en_uso": False},
        {"x": 825, "y": 100, "en_uso": False}
    ]
    
    # --- CONFIGURACIÓN DE LA PARRILLA ---
    lugares_parrilla = [
        {"x": 375, "y": 550, "en_uso": False},
        {"x": 575, "y": 550, "en_uso": False},
        {"x": 175, "y": 550, "en_uso": False},
        {"x": 825, "y": 550, "en_uso": False},
        
        {"x": 375, "y": 750, "en_uso": False},
        {"x": 575, "y": 750, "en_uso": False},
        {"x": 375, "y": 350, "en_uso": False},
        {"x": 575, "y": 350, "en_uso": False},
        
        {"x": 175, "y": 750, "en_uso": False},
        {"x": 825, "y": 750, "en_uso": False},
        {"x": 175, "y": 350, "en_uso": False},
        {"x": 825, "y": 350, "en_uso": False}
    ]
    
    # Lista dinámica donde se guardarán todas las carnes que están vivas en pantalla
    spawn_de_carnes = []

    # Al empezar el juego rellenamos los 3 slots inmediatamente para arrancar con comida
    for i in range(3):
        nueva_carne = spawnear_carne(slots_spawn[i]["x"], slots_spawn[i]["y"], i)
        spawn_de_carnes.append(nueva_carne)
        slots_spawn[i]["en_uso"] = True

    # --- TEMPORIZADOR DE GENERACIÓN INFINITA ---
    # Definimos en cuántos segundos se generará el próximo alimento (entre 5.0 y 10.0)
    timer_generacion = random.uniform(2.5, 6.5)
>>>>>>> 75e8fac061142ace7549ad8e30c0e2d54775a46e

    ejecutando = True

    #logica inicial carbon
    nivel_carbon = 50
    ultimo_tiempo_carbon = pygame.time.get_ticks()
    carbon_rect = carbon.get_rect(topleft=(1020, 650))

    #temporizador de partida
    TIEMPO_PARTIDA = 180
    inicio_partida = pygame.time.get_ticks()
    fuente_timer = pygame.font.SysFont("arial", 40, bold=True)

    while ejecutando:

        #temporizador
        tiempo_transcurrido = (pygame.time.get_ticks() - inicio_partida) // 1000
        tiempo_restante = TIEMPO_PARTIDA - tiempo_transcurrido
        if tiempo_restante <= 0:
            tiempo_restante = 0
            game_over(pantalla,"¡Se termino el tiempo!")
            return

        #funcionalidad del carbon 
        tiempo_actual = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        hover_carbon = carbon_rect.collidepoint(mouse_pos)

        if hover_carbon:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Reducción exponencial del nivel de carbón
        if tiempo_actual - ultimo_tiempo_carbon >= 1000:
            # Usamos una constante (ej. 200). A menor nivel_carbon, mayor es el resultado de la división.
            # IMPORTANTE: Sumamos + 1 al divisor para evitar que yo lance un error fatal de "ZeroDivisionError"
            puntos_a_restar = 600 / (nivel_carbon + 1)
            
            # Restamos esos puntos al total
            nivel_carbon -= puntos_a_restar
            
            # Límite inferior de seguridad
            if nivel_carbon < 1:
                nivel_carbon = 0
                game_over(pantalla,"¡Que mal! Se te apago el fuego :(")
                return
        
            ultimo_tiempo_carbon = tiempo_actual

        #cambios parrilla segun carbon
        if nivel_carbon > 75:
            parrilla_actual = fuego_alto
            color_barra_carbon = (220, 0, 0)

        elif nivel_carbon > 55:
            parrilla_actual = fuego_medio
            color_barra_carbon = (255, 140, 0)

        else:
            parrilla_actual = fuego_bajo
            color_barra_carbon = (120, 120, 120)

        
        # Calculamos el delta time (dt) para manejar el tiempo real de cocción
        dt = reloj.tick(60) / 1000.0    # Tiempo en fracciones de segundo
        
        # --- LÓGICA DE GENERACIÓN AUTOMÁTICA DE CARNES ---
        timer_generacion -= dt
        if timer_generacion <= 0:
            # Buscamos qué slots superiores están vacíos actualmente
            slots_libres = [i for i, s in enumerate(slots_spawn) if not s["en_uso"]]
            
            # Si hay al menos un slot vacío arriba, generamos una carne
            if slots_libres:
                slot_elegido_idx = random.choice(slots_libres) # Elegimos un slot vacío al azar
                slot = slots_spawn[slot_elegido_idx]
                
                # Creamos de forma infinita una carne aleatoria y la sumamos al juego
                nueva_carne = spawnear_carne(slot["x"], slot["y"], slot_elegido_idx)
                spawn_de_carnes.append(nueva_carne)
                slot["en_uso"] = True
                print(f"--> ¡Apareció un nuevo {nueva_carne['nombre']} en el slot {slot_elegido_idx + 1}!")
                
            # Reiniciamos el temporizador para generar una nueva carne dentro de 1.25 y 3.5 segundos
            timer_generacion = random.uniform(1.25, 3.5)
        
        # --- DETECCIÓN DE EVENTOS DE CLIC ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #agregar mas carbon
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if carbon_rect.collidepoint(evento.pos):
                    nivel_carbon += 10
                    if nivel_carbon > 100:
                        nivel_carbon = 100

                for carne in spawn_de_carnes:
                    if carne["rect"].collidepoint(evento.pos):
                        
                        # CASO A: El jugador clickea una carne del slot para bajarla a la parrilla.
                        if carne["ubicacion"] == "slots":
                            # Buscamos un lugar libre en la parrilla
                            for lugar_parrilla in lugares_parrilla:
                                if not lugar_parrilla["en_uso"]:
                                    # Movemos visualmente el rect abajo
                                    carne["rect"].center = (lugar_parrilla["x"], lugar_parrilla["y"])
                                    carne["ubicacion"] = "parrilla"
                                    lugar_parrilla["en_uso"] = True
                                    carne["mi_lugar"] = lugar_parrilla
                                    # Liberamos el slot de spawn para que pueda aparecer una carne nueva ahí
                                    idx_slot_viejo = carne["slot_origen"]
                                    slots_spawn[idx_slot_viejo]["en_uso"] = False
                                    break
                                    
                        # Click a una carne que esta en la parrilla:
                        elif carne["ubicacion"] == "parrilla":
                            
                            if carne["estado_quemado"] == False:
                                # CASO B: Voltear carne
                                if carne["lado_b"] == False:
                                    if carne["cocinando"] >= carne["coccion_maxima"]*0.4:
                                        voltear_carne(carne, jugador)
                                    else:
                                        jugador["resultado"] -= carne["coccion_maxima"]*10 *0.1
                                #CASO C: Servir
                                elif carne["lado_b"] == True:
                                    if carne["cocinando"] >= carne["coccion_maxima"]*0.8:
                                        servir(carne, jugador, spawn_de_carnes)
                                    else:
                                        jugador["resultado"] -= carne["coccion_maxima"] * 10 * 0.1
                            #CASO D: Clickea una carne quemada para desechar
                            elif carne["estado_quemado"] == True:
                                remover(carne, spawn_de_carnes)
        
        # --- ACTUALIZACIÓN ---
        actualizar_logica_carnes(spawn_de_carnes, dt, jugador, nivel_carbon)
        
        # --- DIBUJO ---
        pantalla.fill((40, 40, 40))
        
        # 1. PRIMERO DIBUJAMOS EL FONDO (La capa más profunda)
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(carbon, carbon_rect)

        if hover_carbon:
            pygame.draw.rect(pantalla,(255, 255, 0),carbon_rect,4)
        # Fondo barra carbón
        pygame.draw.rect(pantalla,(80, 80, 80),(940, 50, 250, 30))

        # Nivel actual
        pygame.draw.rect(pantalla,color_barra_carbon,(940, 50, nivel_carbon * 2.5, 30))

        # Borde
        pygame.draw.rect(pantalla,(255, 255, 255),(940, 50, 250, 30),2)
        pantalla.blit(parrilla_actual, (10, 190))
        
        # Dibujamos visualmente las siluetas fijas de los 4 slots de arriba
        for s in slots_spawn:
            pygame.draw.rect(pantalla, (60, 60, 60), (s["x"] - 50, s["y"] - 50, 100, 100), 2, border_radius=5)
            
                
        # Renderizado de las carnes activas en pantalla
        for carne in spawn_de_carnes:
            if carne["estado_crudo"]:
                pantalla.blit(carne["img_cruda"], carne["rect"])
            elif carne["estado_cocido"]:
                pantalla.blit(carne["img_cocida"], carne["rect"])
            elif carne["estado_crudo"] == False and carne["estado_cocido"] == False:
                # Dibujo de comida quemada
                pantalla.blit(img_quemada, carne["rect"])
            
            # Barras de cocción 
            if carne["ubicacion"] == "parrilla" and carne["cocinando"] > 0:
                ancho_total_barra = 100
                ancho_actual = (carne["cocinando"] / carne["coccion_maxima"]) * ancho_total_barra
                
                x_barra = carne["rect"].x
                y_barra = carne["rect"].y - 15
                
                # Color de fondo de barra
                if carne["estado_quemado"] == False:
                    pygame.draw.rect(pantalla, (128, 0, 0), (x_barra, y_barra, ancho_total_barra, 8))
                    
                    color_barra = (0, 255, 0) #verde, coccion bien
                    #Colores de alerta:
                    if carne["cocinando"] >= (carne["coccion_maxima"] *0.5 ) and not carne["lado_b"]:
                        if carne["cocinando"] >= (carne["coccion_maxima"] *0.7 ) and not carne["lado_b"]:
                            color_barra = (255, 0, 0)  #rojo "a punto de chamuscarse"
                        else:
                            color_barra = (255, 200, 0) #amarillo "apresurate"
                    elif carne["cocinando"] >= (carne["coccion_maxima"]):
                        color_barra = (255, 0, 0) #rojo, "cocinado y a punto de chamuscarse"
                    pygame.draw.rect(pantalla, color_barra, (x_barra, y_barra, ancho_actual, 8))
        
        #temporizador
        minutos = tiempo_restante // 60
        segundos = tiempo_restante % 60
        texto_timer = fuente_timer.render(f"{minutos:02}:{segundos:02}",True,(255, 255, 255))
        pantalla.blit(texto_timer, (1080, 10))

        pygame.display.flip()
        reloj.tick(60)

def game_over(pantalla, mensaje): #agregar jugador y los puntos obtenidos

    reloj = pygame.time.Clock()

    fuente_titulo = pygame.font.SysFont(
        "arial",
        80,
        bold=True
    )

    fuente_mensaje = pygame.font.SysFont(
        "arial",
        40
    )

    fuente_boton = pygame.font.SysFont(
        "arial",
        40
    )

    boton_menu = pygame.Rect(
        300,     # más a la izquierda
        520,
        600,     # más ancho
        90
    )

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

<<<<<<< HEAD
                # Botón carbón (ajustá el Rect a la posición real de tu imagen)
                rect_carbon = pygame.Rect(1020, 650, 164, 242)
                if rect_carbon.collidepoint(evento.pos):
                    sonidos.reproducir("carbon")

                # Cuando tus compañeros agreguen la lógica de poner/retirar carne,
                # los llamados serán así:
                #   sonidos.reproducir("carne_puesta")   ← al colocar
                #   sonidos.reproducir("carne_punto")    ← al retirar a punto
                #   sonidos.reproducir("carne_quemada")  ← cuando se quema

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(carbon, (1020, 650))
        pantalla.blit(parrilla, (10, 190))
=======
                if boton_menu.collidepoint(evento.pos):
                    return

        pantalla.fill((20, 20, 20))

        # Título
        texto = fuente_titulo.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        rect_texto = texto.get_rect(
            center=(600, 220)
        )

        pantalla.blit(texto, rect_texto)

        # Mensaje personalizado
        texto_mensaje = fuente_mensaje.render(
            mensaje,
            True,
            (255, 255, 255)
        )

        rect_mensaje = texto_mensaje.get_rect(
            center=(600, 340)
        )

        pantalla.blit(
            texto_mensaje,
            rect_mensaje
        )

        # Botón
        pygame.draw.rect(
            pantalla,
            (200, 200, 200),
            boton_menu,
            border_radius=10
        )

        texto_menu = fuente_boton.render(
            "VOLVER AL MENU PRINCIPAL",
            True,
            (0, 0, 0)
        )

        rect_menu = texto_menu.get_rect(
            center=boton_menu.center
        )

        pantalla.blit(
            texto_menu,
            rect_menu
        )
>>>>>>> 75e8fac061142ace7549ad8e30c0e2d54775a46e

        pygame.display.flip()
        reloj.tick(60)