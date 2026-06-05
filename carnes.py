
#carnes = [chorizo, paty, pollo, chuleton_cerdo, bife_chorizo, bife_angosto]

import pygame
import random

# Diccionarios base con la configuración de cada alimento.
# No les ponemos imágenes ni rectángulos acá para no sobrecargar la memoria al clonarlos.
DATOS_BASE_CARNES = [
    {"nombre": "Chorizo", "img_cruda_path": "img/chorizo_crudo.png", "img_cocida_path": "img/chorizo_cocido.png", "puntaje_maximo": 90.0},
    {"nombre": "Paty", "img_cruda_path": "img/paty_crudo.png", "img_cocida_path": "img/paty_cocido.png", "puntaje_maximo": 100.0},
    {"nombre": "Pollo", "img_cruda_path": "img/pollo_crudo.png", "img_cocida_path": "img/pollo_cocido.png", "puntaje_maximo": 120.0},
    {"nombre": "Chuleton de Cerdo", "img_cruda_path": "img/chuleton_cerdo_crudo.png", "img_cocida_path": "img/chuleton_cerdo_cocido.png", "puntaje_maximo": 120.0},
    {"nombre": "Bife de Chorizo", "img_cruda_path": "img/bife_de_chorizo_crudo.png", "img_cocida_path": "img/bife_de_chorizo_cocido.png", "puntaje_maximo": 150.0},
    {"nombre": "Bife Angosto", "img_cruda_path": "img/bife_angosto_crudo.png", "img_cocida_path": "img/bife_angosto_cocido.png", "puntaje_maximo": 110.0}
]

def precargar_imagenes_carnes():
    """Carga las 12 texturas cocido/crudo en la memoria una sola vez"""
    for base in DATOS_BASE_CARNES:
        base["img_cruda"] = pygame.image.load(base["img_cruda_path"]).convert_alpha()
        base["img_cocida"] = pygame.image.load(base["img_cocida_path"]).convert_alpha()
        

def crear_carne_aleatoria(x_slot, y_slot, indice_slot):
    """Genera, carga y devuelve un objeto de carne aleatorio asignado a un slot específico"""
    
    # Elegimos un tipo de carne al azar de la lista
    base = random.choice(DATOS_BASE_CARNES)
    
    # Creamos la nueva carne reciclando las imágenes ya cargadas en 'base'
    nueva_carne = {
        "nombre": base["nombre"],
        "puntaje_maximo": base["puntaje_maximo"],
        "img_cruda": base["img_cruda"],   # <- Referencia a la imagen maestra en RAM
        "img_cocida": base["img_cocida"], # <- Referencia a la imagen maestra en RAM
        "puntaje_coccion": 0.0,
        "estado_crudo": True,
        "estado_cocido": False,
        "lado_b": False,
        "tiempo_en_mitad": 0.0,
        "ubicacion": "slots",
        "slot_origen": indice_slot
    }
    
    

    
    # Creamos su rectángulo físico centrado en el slot asignado
    nueva_carne["rect"] = nueva_carne["img_cruda"].get_rect(center=(x_slot, y_slot))
    
    return nueva_carne


def actualizar_logica_carnes(lista_carnes, dt):
    """Controla la cocción de las carnes que están en la parrilla"""
    for carne in lista_carnes:
        if carne["ubicacion"] == "slots":
            continue # Si está arriba esperando, no pasa nada
        
        # NUEVO: Ignorar si la carne ya está quemada
        if not carne["estado_crudo"] and not carne["estado_cocido"]:
            continue
        
        if carne["puntaje_coccion"] < carne["puntaje_maximo"]:
            carne["puntaje_coccion"] += 15 * dt  
            mitad = carne["puntaje_maximo"] / 2
            
            if carne["puntaje_coccion"] >= mitad and not carne["lado_b"]:
                carne["tiempo_en_mitad"] += dt
                if carne["tiempo_en_mitad"] > 2.0:
                    carne["puntaje_coccion"] -= 8 * dt  
                if carne["tiempo_en_mitad"] >= 5.0:
                    quemar_alimento(carne)
                    
        if carne["puntaje_coccion"] >= (carne["puntaje_maximo"]+2):
            quemar_alimento(carne)

def voltear_carne(carne):
    if not carne["lado_b"]:
        carne["lado_b"] = True
        carne["estado_crudo"] = False
        carne["estado_cocido"] = True
        print(f"¡Volteaste el {carne['nombre']}!")

def quemar_alimento(carne):
    carne["puntaje_coccion"] = 0.0
    carne["estado_crudo"] = False
    carne["estado_cocido"] = False
    print(f"¡El {carne['nombre']} se quemó por completo!")
    
#def servir(carne): 
    #Debe guardar los puntos del jugador

#def remover(carne):
    #debe remover la carne quemada