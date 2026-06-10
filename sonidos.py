import pygame
import os
from rutas import recurso

# ------------------------------------------------------------------ #
#  Configuración y estado global                                       #
# ------------------------------------------------------------------ #

CARPETA = "sounds"
EXTENSIONES = [".wav", ".mp3", ".ogg"]

ARCHIVOS = {
    "carne_puesta":   "carne_puesta",
    "carne_punto":    "carne_punto",
    "carne_quemada":  "carne_quemada",
    "carbon":         "carbon",
    "ambiente_juego": "ambiente_juego",
    "ladrido": "ladrido",
    "risa": "risa",
    "victoria":       "victoria",
    "derrota":        "derrota",
}

MUSICAS = {
    "menu":  "musica_menu",
    "juego": "musica_juego",
}

_sonidos = {}
_volumen_efectos = 0.8
_volumen_musica = 0.5
_muteado = False
_musica_actual = None

# ------------------------------------------------------------------ #
#  Inicialización                                                      #
# ------------------------------------------------------------------ #

def inicializar(carpeta="sounds", volumen_efectos=0.8, volumen_musica=0.5):
    global CARPETA, _volumen_efectos, _volumen_musica

    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    CARPETA = carpeta
    _volumen_efectos = volumen_efectos
    _volumen_musica = volumen_musica

    _cargar_sonidos()

# ------------------------------------------------------------------ #
#  Carga                                                               #
# ------------------------------------------------------------------ #

def _buscar_archivo(nombre_base):
    for ext in EXTENSIONES:
        ruta = recurso(
            os.path.join(CARPETA, nombre_base + ext)
        )

        if os.path.isfile(ruta):
            return ruta

    return None

def _cargar_sonidos():
    global _sonidos
    for clave, nombre_base in ARCHIVOS.items():
        ruta = _buscar_archivo(nombre_base)
        if ruta:
            try:
                sonido = pygame.mixer.Sound(ruta)
                sonido.set_volume(_volumen_efectos)
                _sonidos[clave] = sonido
                print(f"[Sonidos] ✓ Cargado: {ruta}")
            except pygame.error as e:
                print(f"[Sonidos] ✗ Error al cargar '{ruta}': {e}")
        else:
            print(f"[Sonidos] ⚠ No encontrado: sounds/{nombre_base}.*  → se omite")

# ------------------------------------------------------------------ #
#  Efectos de sonido                                                   #
# ------------------------------------------------------------------ #

def reproducir(clave):
    if _muteado:
        return
    sonido = _sonidos.get(clave)
    if sonido:
        sonido.play()
    else:
        print(f"[Sonidos] ⚠ Clave desconocida o no cargada: '{clave}'")

# ------------------------------------------------------------------ #
#  Música de fondo                                                     #
# ------------------------------------------------------------------ #

def reproducir_musica(clave, loops=-1):
    global _musica_actual
    if _muteado:
        return

    nombre_base = MUSICAS.get(clave)
    if not nombre_base:
        print(f"[Sonidos] ⚠ Clave de música desconocida: '{clave}'")
        return

    if _musica_actual == clave and pygame.mixer.music.get_busy():
        return

    ruta = _buscar_archivo(nombre_base)
    if not ruta:
        print(f"[Sonidos] ⚠ Archivo de música no encontrado: sounds/{nombre_base}.*")
        return

    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(_volumen_musica)
        pygame.mixer.music.play(loops)
        _musica_actual = clave
        print(f"[Sonidos] ♪ Música: {ruta}")
    except pygame.error as e:
        print(f"[Sonidos] ✗ Error al reproducir música '{ruta}': {e}")

def reproducir_loop(clave, volumen=None):
    if _muteado:
        return
    sonido = _sonidos.get(clave)
    if sonido:
        if volumen is not None:
            sonido.set_volume(volumen)
        sonido.play(loops=-1)

def detener_loop(clave):
    sonido = _sonidos.get(clave)
    if sonido:
        sonido.stop()

def detener_musica():
    global _musica_actual
    pygame.mixer.music.stop()
    _musica_actual = None

def pausar_musica():
    pygame.mixer.music.pause()

def reanudar_musica():
    if not _muteado:
        pygame.mixer.music.unpause()
