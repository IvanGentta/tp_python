
import pygame
import random

# Diccionarios base con la configuración de cada alimento.
# No les ponemos imágenes ni rectángulos acá para no sobrecargar la memoria al clonarlos.
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
        base["img_cruda"] = pygame.image.load(base["img_cruda_path"]).convert_alpha()
        base["img_cocida"] = pygame.image.load(base["img_cocida_path"]).convert_alpha()
        

def spawnear_carne(x_slot, y_slot, indice_slot):
    """Genera, carga y devuelve un objeto de carne aleatorio asignado a un slot específico"""
    
    # Elegimos un tipo de carne al azar de la lista
    base = random.choice(DATOS_BASE_CARNES)
    
    # Creamos la nueva carne reciclando las imágenes ya cargadas en 'base'
    nueva_carne = {
        "nombre": base["nombre"],
        "img_cruda": base["img_cruda"],   # <- Referencia a la imagen maestra en RAM
        "img_cocida": base["img_cocida"], # <- Referencia a la imagen maestra en RAM
        "coccion_maxima": base["coccion_maxima"],
        "cocinando": 0.0, 
        "estado_crudo": True,
        "estado_cocido": False,
        "lado_b": False,
        "tiempo_sin_voltear": 0.0,
        "ubicacion": "slots",
        "slot_origen": indice_slot,
        "puntaje" : base["coccion_maxima"],
        "resultado" : 0.0
    }
     # debemos agregar-> servido(bool); resultado(float);
	# debo pulir la logica de estado_crudo, estado_cocido, quemado.
    

    
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
        
        if carne["cocinando"] < carne["coccion_maxima"]:
            carne["cocinando"] += 15 * dt  
            mitad = carne["coccion_maxima"] / 2
            
            if carne["cocinando"] >= mitad and not carne["lado_b"]:
                carne["tiempo_sin_voltear"] += dt
                if carne["tiempo_sin_voltear"] > 2.0:
                    carne["cocinando"] -= 8 * dt  
                if carne["tiempo_sin_voltear"] >= 5.0:
                    quemar_alimento(carne)
                    
        if carne["cocinando"] >= (carne["coccion_maxima"]+2):
            quemar_alimento(carne)

def voltear_carne(carne):
    if not carne["lado_b"]:
        if carne["tiempo_sin_voltear"] <= 0.0 :
            carne["lado_b"] = True  #se dio vuelta
            carne["estado_crudo"] = False
            carne["estado_cocido"] = True
            carne["puntaje"]-= carne["coccion_maxima"] * 0.2
            print(f"¡Volteaste el {carne['nombre']}!")

def quemar_alimento(carne):
    carne["cocinando"] = 0.0
    carne["estado_crudo"] = False
    carne["estado_cocido"] = False
    carne["puntaje"]= 0.0
    print(f"¡El {carne['nombre']} se quemó por completo!")
    
#def servir(carne): 
    #Debe guardar los puntos del jugador

#def remover(carne):
    #debe remover la carne quemada