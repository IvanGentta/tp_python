import pygame
import os

class GestorSonidos:
    """
    Gestiona todos los sonidos del juego Maestro Parrillero.
    
    Uso básico:
        sonidos = GestorSonidos()
        sonidos.reproducir("carne_puesta")
        sonidos.reproducir_musica("menu")
    
    Carpeta esperada de archivos:
        sounds/
            carne_puesta.wav
            carne_punto.wav
            carne_quemada.wav
            carbon.wav
            musica_menu.mp3
            musica_juego.mp3
    """

    # Nombres internos → nombre de archivo (sin extensión)
    ARCHIVOS = {
        "carne_puesta":   "carne_puesta",    # Al colocar carne en la parrilla
        "carne_punto":    "carne_punto",      # Al retirar la carne a punto (éxito)
        "carne_quemada":  "carne_quemada",    # Cuando la carne se quema
        "carbon":         "carbon",           # Al agregar carbón
        "ruido_parrilla": "ruido_parrilla",
        "ambiente_juego": "ambiente_juego",
    }

    MUSICAS = {
        "menu":  "musica_menu",
        "juego": "musica_juego",
    }

    # Extensiones a probar en orden
    EXTENSIONES = [".wav", ".mp3", ".ogg"]

    def __init__(self, carpeta_sounds="sounds", volumen_efectos=0.8, volumen_musica=0.5):
        """
        Inicializa el gestor.
        
        Args:
            carpeta_sounds: Ruta a la carpeta con los archivos de audio.
            volumen_efectos: Volumen de efectos de sonido (0.0 a 1.0).
            volumen_musica:  Volumen de la música de fondo (0.0 a 1.0).
        """
        # Inicializa el mixer si no fue inicializado todavía
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.carpeta = carpeta_sounds
        self._volumen_efectos = volumen_efectos
        self._volumen_musica = volumen_musica
        self._muteado = False
        self._musica_actual = None

        # Diccionario donde se guardan los sonidos cargados
        self._sonidos: dict[str, pygame.mixer.Sound] = {}

        self._cargar_sonidos()

    # ------------------------------------------------------------------ #
    #  Carga                                                               #
    # ------------------------------------------------------------------ #

    def _buscar_archivo(self, nombre_base: str) -> str | None:
        """Busca el archivo probando distintas extensiones. Devuelve la ruta o None."""
        for ext in self.EXTENSIONES:
            ruta = os.path.join(self.carpeta, nombre_base + ext)
            if os.path.isfile(ruta):
                return ruta
        return None

    def _cargar_sonidos(self):
        """Carga todos los efectos de sonido. Los que no se encuentran se omiten con aviso."""
        for clave, nombre_base in self.ARCHIVOS.items():
            ruta = self._buscar_archivo(nombre_base)
            if ruta:
                try:
                    sonido = pygame.mixer.Sound(ruta)
                    sonido.set_volume(self._volumen_efectos)
                    self._sonidos[clave] = sonido
                    print(f"[Sonidos] ✓ Cargado: {ruta}")
                except pygame.error as e:
                    print(f"[Sonidos] ✗ Error al cargar '{ruta}': {e}")
            else:
                print(f"[Sonidos] ⚠ No encontrado: sounds/{nombre_base}.*  → se omite")

    # ------------------------------------------------------------------ #
    #  Efectos de sonido                                                   #
    # ------------------------------------------------------------------ #

    def reproducir(self, clave: str):
        """
        Reproduce un efecto de sonido por su clave.
        
        Claves disponibles:
            "carne_puesta", "carne_punto", "carne_quemada", "carbon"
        
        No hace nada si el sonido no fue cargado o el juego está muteado.
        """
        if self._muteado:
            return
        sonido = self._sonidos.get(clave)
        if sonido:
            sonido.play()
        else:
            print(f"[Sonidos] ⚠ Clave desconocida o no cargada: '{clave}'")

    # ------------------------------------------------------------------ #
    #  Música de fondo                                                     #
    # ------------------------------------------------------------------ #

    def reproducir_musica(self, clave: str, loops: int = -1):
        """
        Reproduce música de fondo en loop.
        
        Args:
            clave:  "menu" o "juego"
            loops:  -1 = infinito, 0 = una vez, N = N veces extra
        
        No reinicia la música si ya está sonando la misma.
        """
        if self._muteado:
            return

        nombre_base = self.MUSICAS.get(clave)
        if not nombre_base:
            print(f"[Sonidos] ⚠ Clave de música desconocida: '{clave}'")
            return

        if self._musica_actual == clave and pygame.mixer.music.get_busy():
            return  # Ya está sonando, no reiniciar

        ruta = self._buscar_archivo(nombre_base)
        if not ruta:
            print(f"[Sonidos] ⚠ Archivo de música no encontrado: sounds/{nombre_base}.*")
            return

        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(self._volumen_musica)
            pygame.mixer.music.play(loops)
            self._musica_actual = clave
            print(f"[Sonidos] ♪ Música: {ruta}")
        except pygame.error as e:
            print(f"[Sonidos] ✗ Error al reproducir música '{ruta}': {e}")

    def reproducir_loop(self, clave: str, volumen: float = None):
        if self._muteado:
            return
        sonido = self._sonidos.get(clave)
        if sonido:
            if volumen is not None:
                sonido.set_volume(volumen)
            sonido.play(loops=-1)

    def detener_loop(self, clave: str):
        sonido = self._sonidos.get(clave)
        if sonido:
            sonido.stop()        

    def detener_musica(self):
        """Detiene la música de fondo."""
        pygame.mixer.music.stop()
        self._musica_actual = None

    def pausar_musica(self):
        """Pausa la música (se puede reanudar con reanudar_musica)."""
        pygame.mixer.music.pause()

    def reanudar_musica(self):
        """Reanuda la música pausada."""
        if not self._muteado:
            pygame.mixer.music.unpause()

    # ------------------------------------------------------------------ #
    #  Volumen                                                             #
    # ------------------------------------------------------------------ #

    def set_volumen_efectos(self, volumen: float):
        """Cambia el volumen de efectos en tiempo real (0.0 a 1.0)."""
        self._volumen_efectos = max(0.0, min(1.0, volumen))
        for sonido in self._sonidos.values():
            sonido.set_volume(self._volumen_efectos)

    def set_volumen_musica(self, volumen: float):
        """Cambia el volumen de la música en tiempo real (0.0 a 1.0)."""
        self._volumen_musica = max(0.0, min(1.0, volumen))
        pygame.mixer.music.set_volume(self._volumen_musica)

    # ------------------------------------------------------------------ #
    #  Mute                                                                #
    # ------------------------------------------------------------------ #

    def toggle_mute(self):
        """Alterna entre muteado y normal. Devuelve el nuevo estado (True = muteado)."""
        self._muteado = not self._muteado
        if self._muteado:
            pygame.mixer.music.set_volume(0)
            for sonido in self._sonidos.values():
                sonido.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self._volumen_musica)
            for sonido in self._sonidos.values():
                sonido.set_volume(self._volumen_efectos)
        return self._muteado

    @property
    def muteado(self) -> bool:
        return self._muteado