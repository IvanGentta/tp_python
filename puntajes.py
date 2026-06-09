import json
import os

ARCHIVO = "puntajes.json"
MAX_PUNTAJES = 10  # Cantidad máxima de puntajes guardados


def cargar_puntajes():
    """Lee el archivo JSON y devuelve la lista de puntajes.
    Si el archivo no existe, devuelve una lista vacía."""
    if not os.path.isfile(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def guardar_puntaje(nombre, puntaje):
    """Agrega un nuevo puntaje, ordena de mayor a menor y guarda solo los TOP 10."""
    puntajes = cargar_puntajes()

    puntajes.append({
        "nombre": nombre.strip() or "Anónimo",
        "puntaje": round(puntaje, 1)
    })

    # Ordena de mayor a menor puntaje
    puntajes.sort(key=lambda x: x["puntaje"], reverse=True)

    # Guarda solo los primeros MAX_PUNTAJES
    puntajes = puntajes[:MAX_PUNTAJES]

    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(puntajes, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[Puntajes] ✗ No se pudo guardar: {e}")
