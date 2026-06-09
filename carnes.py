import pygame
import juego
import sonidos
import random
from rutas import recurso

# Diccionarios base con la configuración de cada alimento.

DATOS_BASE_CARNES = [
    {"nombre": "Chorizo", "img_cruda_path": "img/chorizo_crudo.png", "img_cocida_path": "img/chorizo_cocido.png", "coccion_maxima": 90.0},
    {"nombre": "Paty", "img_cruda_path": "img/paty_crudo.png", "img_cocida_path": "img/paty_cocido.png", "coccion_maxima": 100.0},
    {"nombre": "Pollo", "img_cruda_path": "img/pollo_crudo.png", "img_cocida_path": "img/pollo_cocido.png", "coccion_maxima": 120.0},
    {"nombre": "Chuleton de Cerdo", "img_cruda_path": "img/chuleton_cerdo_crudo.png", "img_cocida_path": "img/chuleton_cerdo_cocido.png", "coccion_maxima": 120.0},
    {"nombre": "Bife de Chorizo", "img_cruda_path": "img/bife_de_chorizo_crudo.png", "img_cocida_path": "img/bife_de_chorizo_cocido.png", "coccion_maxima": 150.0},
    {"nombre": "Bife Angosto", "img_cruda_path": "img/bife_angosto_crudo.png", "img_cocida_path": "img/bife_angosto_cocido.png", "coccion_maxima": 110.0}
]

def precarga_imagenes_carnes():
    """Carga las 12 texturas cocido/crudo en la memoria una sola vez"""
    for base in DATOS_BASE_CARNES:
        base["img_cruda"] = pygame.image.load(recurso(base["img_cruda_path"])).convert_alpha()
        base["img_cocida"] = pygame.image.load(recurso(base["img_cocida_path"])).convert_alpha()
        

def spawnear_carne(x_slot, y_slot, indice_slot):
    """Genera, carga y devuelve un objeto de carne aleatorio asignado a un slot específico"""
    
    # Elegimos un tipo de carne al azar de la lista
    base = random.choice(DATOS_BASE_CARNES)

    nueva_carne = {
        "nombre": base["nombre"],
        "img_cruda": base["img_cruda"],
        "img_cocida": base["img_cocida"], 
        "coccion_maxima": base["coccion_maxima"],
        "cocinando": 0.0, 
        "estado_crudo": True,
        "estado_cocido": False,
        "estado_quemado": False,
        "lado_b": False,
        "servido": False,
        "ubicacion": "slots",
        "mi_lugar" : "ninguno",
        "slot_origen": indice_slot,
        "puntaje" : 0.0
    }  

    # Creamos su rectángulo físico centrado en el slot asignado
    nueva_carne["rect"] = nueva_carne["img_cruda"].get_rect(center=(x_slot, y_slot))
    
    return nueva_carne


def actualizar_logica_carnes(spawn_de_carnes, dt, nivel_carbon):
    """Controla la cocción de las carnes que están en la parrilla"""
    for carne in spawn_de_carnes:
        if carne["ubicacion"] == "slots":
            continue # Si está arriba esperando, no pasa nada
        
        if carne["cocinando"] < carne["coccion_maxima"]*1.2:
            #aqui agergaria distintos valores para fuego alto/mediano/bajo.
            if nivel_carbon > 75:
                carne["cocinando"] += 25 * dt  #se multiplica por dt para sumar 15 puntos por cada segundo real (si no estuviera *dt , se agregaria por fotograma)
            elif nivel_carbon > 55:		
                carne["cocinando"] += 15 * dt
            else:
                carne["cocinando"] += 10 * dt
                
            if carne["cocinando"] >= (carne["coccion_maxima"] *0.65) and not carne["lado_b"]:
                    chamuscar(carne)
        else:
            chamuscar(carne)

def voltear_carne(carne, jugador):
        #vuelta en tiempos correctos
    if carne["cocinando"] >= carne["coccion_maxima"]*0.45 and carne["cocinando"] <= carne["coccion_maxima"] *0.55 :
        carne["lado_b"] = True  #se dio vuelta
        carne["estado_crudo"] = False
        carne["estado_cocido"] = True
        jugador["resultado"] += carne["coccion_maxima"] *10 * 0.25
        
        #vuelta muy temprana o muy tarde (cerca de chamuscarse)
    elif carne["cocinando"] < carne["coccion_maxima"]*0.4 or carne["cocinando"] > carne["coccion_maxima"]*0.6:
        carne["lado_b"] = True  #se dio vuelta
        carne["estado_crudo"] = False
        carne["estado_cocido"] = True
        jugador["resultado"] += carne["coccion_maxima"] *10 * 0.1
        
        #vuelta un poco antes o un poco despues del tiempo correcto
    else:
        carne["lado_b"] = True  #se dio vuelta
        carne["estado_crudo"] = False
        carne["estado_cocido"] = True
        jugador["resultado"] += carne["coccion_maxima"] *10 * 0.15
            

def chamuscar(carne):
    carne["cocinando"] = 0
    carne["estado_crudo"] = False
    carne["estado_cocido"] = False
    carne["estado_quemado"] = True
    carne["puntaje"] = 0.0
    sonidos.reproducir("carne_quemada")
    
def servir(carne, spawn_de_carnes, jugador):
    #si sirve la carne entre el 90% y 110% está ok y recibe todos los puntos.
    if carne["cocinando"] >= carne["coccion_maxima"] *0.9 and carne["cocinando"] < carne["coccion_maxima"] *1.1:
        jugador["resultado"] += carne["coccion_maxima"]*10
        remover(carne, spawn_de_carnes, jugador)
        
    #si sirve la carne por deajo del 90% o por encima del 110% recibe tres cuartas partes de los puntos.
    elif carne["cocinando"] < carne["coccion_maxima"] *0.9 or carne["cocinando"] > carne["coccion_maxima"] * 1.1 :
        jugador["resultado"] += carne["coccion_maxima"] *10 * 0.75
        remover(carne, spawn_de_carnes, jugador)


def remover(carne, spawn_de_carnes, jugador):
    jugador["resultado"] += carne["puntaje"]
    if "mi_lugar" in carne and carne["mi_lugar"] != "ninguno":
        carne["mi_lugar"]["en_uso"] = False
    spawn_de_carnes.remove(carne)
    
    """if "mi_lugar_parrilla" in carne:
        carne["mi_lugar_parrilla"]["en_uso"] = False
    spawn_de_carnes.remove(carne)"""