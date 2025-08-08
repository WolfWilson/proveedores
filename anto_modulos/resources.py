# anto_modulos/resources.py
from __future__ import annotations
import os
import sys

def _base_dir() -> str:
    """Carpeta base para recursos. Compatible con PyInstaller (_MEIPASS)."""
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def resource_path(*parts: str) -> str:
    """Devuelve una ruta absoluta a un recurso dentro del proyecto/EXE."""
    return os.path.join(_base_dir(), *parts)

# 🔹 Cambiá estos nombres si tu icono de ventana es otro
ICON_MAIN = resource_path("Source", "userprofile4.png")  # o "userprofile4.png" si preferís
# 🔹 Flecha personalizada para el QDateEdit (usa la que ya tenés en /Source)
DATE_ARROW_DOWN = resource_path("Source", "down-arrow_15775882.png")
