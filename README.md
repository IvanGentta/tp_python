# Maestro Parrillero

## Autores

- Christian Gustavo Aguirre
- Fernando Bogdanoff
- Iván Gentta

## Descripción

Este proyecto fue desarrollado como TP integrador Python de la materia Laboratorio de Computación II dictada por la profesora Monica Hencek en la Universidad Nacional de San Martín.

Maestro Parrillero es un juego desarrollado en Python utilizando Pygame.

El objetivo es cocinar distintos tipos de carne en la parrilla, administrando correctamente el fuego y los tiempos de cocción para obtener la mayor cantidad de puntos posible antes de que termine el tiempo.

## Requisitos

- Python 3.13
- Pygame
- PyInstaller (opcional para generar el ejecutable)

## Instalación

Instalar dependencias:

pip install pygame

pip install pyinstaller

Generar el ejecutable:

```bash
pyinstaller --onefile --windowed \
--add-data "img:img" \
--add-data "sounds:sounds" \
--add-data "instrucciones:instrucciones" \
main.py
```

El ejecutable se encontrará en la carpeta:

```text
dist/
```

## Estructura

```text
tp_python/
│
├── main.py
├── juego.py
├── carnes.py
├── sonidos.py
├── instrucciones.py
├── highscores.py
├── puntajes.py
├── rutas.py
├── README.md
│
├── img/
├── sounds/
└── instrucciones/
```
