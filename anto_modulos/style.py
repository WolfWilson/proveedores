# anto_modulos/style.py
# Estilo global y utilidades de UI (PyQt5)

from __future__ import annotations
from typing import Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QApplication,
    QGraphicsDropShadowEffect,
)

# ─────────────────────────────────────────────────────────────────────
# Builder de hoja de estilo (parametrizable)
# ─────────────────────────────────────────────────────────────────────
def build_style(
    *,
    bg: str = "#2b2d42",
    fg: str = "#edf2f4",
    font_family: str = "Segoe UI, sans-serif",
    font_size_px: int = 14,
    card_radius: int = 16,
    control_radius: int = 8,
    border: str = "#8d99ae",
    input_bg: str = "#1a1c2c",
    button_bg: str = "#8d99ae",
    button_text: str = "#2b2d42",
    button_bg_hover: str = "#a8b5cf",
    button_bg_pressed: str = "#6c7a96",
    etiqueta_color: str = "#ff1493",
    progress_chunk: str = "#ef233c",
    # DateEdit
    date_button_bg: str = "#3a3f58",
    date_button_bg_hover: str = "#495377",
    date_button_border: str = "#59628a",
    date_arrow_icon_path: Optional[str] = None,
) -> str:
    """Genera QSS con parámetros. Usa doble llaves {{ }} al ser f-string."""
    arrow_rule = (
        f'image: url("{date_arrow_icon_path}");'
        if date_arrow_icon_path
        else "image: none;"
    )

    return f"""
/* Base */
QDialog, QWidget {{
    background-color: {bg};
    color: {fg};
    border-radius: {card_radius}px;
    font-family: {font_family};
    font-size: {font_size_px}px;
}}

/* Etiqueta fija destacada */
QLabel#etiqueta {{
    color: {etiqueta_color};
    font-weight: 600;
}}

/* Texto general */
QLabel {{
    color: {fg};
    font-weight: 500;
}}

/* Botones base */
QPushButton {{
    background-color: {button_bg};
    color: {button_text};
    border: none;
    padding: 10px 16px;
    border-radius: {control_radius}px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {button_bg_hover};
}}
QPushButton:pressed {{
    background-color: {button_bg_pressed};
}}

/* Inputs */
QLineEdit, QComboBox {{
    background-color: {input_bg};
    color: {fg};
    border: 1px solid {border};
    padding: 6px 8px;
    border-radius: {control_radius}px;
    selection-background-color: {button_bg_hover};
}}
QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {button_bg_hover};
}}

/* QDateEdit */
QDateEdit {{
    background-color: {input_bg};
    color: {fg};
    border: 1px solid {border};
    padding: 4px 8px;
    border-radius: {control_radius}px;
}}
QDateEdit:focus {{
    border: 1px solid {button_bg_hover};
}}
/* Botón de despliegue a la derecha */
QDateEdit::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    background-color: {date_button_bg};
    border-left: 1px solid {date_button_border};
    border-top-right-radius: {control_radius}px;
    border-bottom-right-radius: {control_radius}px;
}}
QDateEdit::drop-down:hover {{
    background-color: {date_button_bg_hover};
}}
/* Flecha */
QDateEdit::down-arrow {{
    width: 14px;
    height: 14px;
    margin-right: 6px;
    {arrow_rule}
}}

/* Barra de progreso */
QProgressBar {{
    border: 1px solid {border};
    border-radius: {control_radius}px;
    background: {input_bg};
    color: {fg};
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {progress_chunk};
    width: 20px;
}}

/* ── ESTADO BOTÓN NUEVO ───────────────────────────────────────── */
QPushButton#btnNuevo:enabled {{
    background-color: #ff1493;   /* fucsia intenso */
    color: #ffffff;
    border: 1px solid #ff7ac8;
    font-weight: 700;
}}
QPushButton#btnNuevo:enabled:hover {{
    background-color: #ff46ad;   /* un toque más claro al hover */
}}
QPushButton#btnNuevo:enabled:pressed {{
    background-color: #d8127f;
}}
QPushButton#btnNuevo:disabled {{
    background-color: #5a2946;   /* fucsia apagado */
    color: #cfa8c3;
    border: 1px dashed #70425c;
}}

/* ── ESTADO BOTÓN EDITAR ──────────────────────────────────────── */
QPushButton#btnEditar:enabled {{
    background-color: #2ecc71;   /* verde éxito */
    color: #0b2a1e;
    border: 1px solid #a3f0c4;
    font-weight: 700;
}}
QPushButton#btnEditar:enabled:hover {{
    background-color: #49d784;
}}
QPushButton#btnEditar:enabled:pressed {{
    background-color: #25b863;
}}
QPushButton#btnEditar:disabled {{
    background-color: #284a39;   /* verde apagado */
    color: #9bb7a6;
    border: 1px dashed #3c6d53;
}}
"""

def build_popup_style(
    *,
    bg: str = "#2b2d42",
    fg: str = "#edf2f4",
    button_bg: str = "#8d99ae",
    button_text: str = "#2b2d42",
    button_bg_hover: str = "#a8b5cf",
    button_bg_pressed: str = "#6c7a96",
    font_family: str = "Segoe UI, sans-serif",
    font_size_px: int = 14,
    control_radius: int = 6,
) -> str:
    return f"""
QMessageBox {{
    background-color: {bg};
    color: {fg};
    font-family: {font_family};
    font-size: {font_size_px}px;
}}
QPushButton {{
    background-color: {button_bg};
    color: {button_text};
    padding: 8px 16px;
    border-radius: {control_radius}px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {button_bg_hover};
}}
QPushButton:pressed {{
    background-color: {button_bg_pressed};
}}
"""

# Hoja de estilo por defecto (podés cambiar parámetros aquí)
STYLE = build_style()
POPUP_STYLE = build_popup_style()

# ─────────────────────────────────────────────────────────────────────
# Ventana base con bordes redondeados, arrastre y sombra opcional
# ─────────────────────────────────────────────────────────────────────
class RoundedWindow(QDialog):
    def __init__(
        self,
        *,
        frameless: bool = False,
        shadow: bool = True,
        shadow_radius: int = 24,
        shadow_color: str = "#000000",
        shadow_opacity: float = 0.3,
        stylesheet: Optional[str] = None,
        parent=None,
    ):
        super().__init__(parent)

        if frameless:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # type: ignore
        else:
            self.setWindowFlags(Qt.Window)  # type: ignore

        self.setStyleSheet(stylesheet or STYLE)

        if shadow:
            effect = QGraphicsDropShadowEffect(self)
            c = QColor(shadow_color); c.setAlphaF(max(0.0, min(1.0, shadow_opacity)))
            effect.setColor(c); effect.setBlurRadius(shadow_radius)
            effect.setXOffset(0); effect.setYOffset(6)
            self.setGraphicsEffect(effect)

        self._drag_enabled = frameless
        self._dragging = False
        self._drag_offset = QPoint()

    def mousePressEvent(self, event):
        if self._drag_enabled and event.button() == Qt.LeftButton:  # type: ignore[attr-defined]
            self._dragging = True
            self._drag_offset = event.globalPos() - self.pos()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_enabled and self._dragging:
            self.move(event.globalPos() - self._drag_offset)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._drag_enabled and self._dragging:
            self._dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)

# ─────────────────────────────────────────────────────────────────────
def show_completion_popup(parent, time_elapsed: float) -> None:
    msg = QMessageBox(parent)
    msg.setWindowTitle("Operación Completada")
    msg.setText(f"La operación finalizó en {time_elapsed:.2f} segundos.")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStyleSheet(POPUP_STYLE)
    msg.exec()

# ─────────────────────────────────────────────────────────────────────
def apply_app_style(
    app: QApplication,
    *,
    date_arrow_icon_path: Optional[str] = None,
    etiqueta_color: str = "#ff1493",
) -> None:
    style = build_style(etiqueta_color=etiqueta_color, date_arrow_icon_path=date_arrow_icon_path)
    app.setStyleSheet(style)
