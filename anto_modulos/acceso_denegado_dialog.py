# anto_modulos/acceso_denegado_dialog.py
# Ventana de acceso denegado con tema coherente con la aplicación.

from __future__ import annotations
import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
)

from anto_modulos.resources import GIF_DENEGADO

_NO_HELP      = Qt.WindowType.WindowContextHelpButtonHint  # type: ignore[attr-defined]
_ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter               # type: ignore[attr-defined]
_ALIGN_LEFT   = Qt.AlignmentFlag.AlignLeft                 # type: ignore[attr-defined]
_ALIGN_TOP    = Qt.AlignmentFlag.AlignTop                  # type: ignore[attr-defined]
_RICH_TEXT    = Qt.TextFormat.RichText                     # type: ignore[attr-defined]


class AccesoDenegadoDialog(QDialog):
    def __init__(self, usuario: str, perfil: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acceso denegado")
        self.setModal(True)
        self.setFixedWidth(440)
        self.setWindowFlags(self.windowFlags() & ~_NO_HELP)  # type: ignore[arg-type]

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(28, 20, 28, 24)

        # ── GIF animado ──
        gif_label = QLabel(self)
        gif_label.setAlignment(_ALIGN_CENTER)
        if os.path.isfile(GIF_DENEGADO):
            self._movie = QMovie(GIF_DENEGADO)
            # Escalar a altura fija (150px) manteniendo proporción
            self._movie.jumpToFrame(0)
            orig = self._movie.currentPixmap().size()
            if orig.height() > 0:
                target_h = 150
                target_w = int(orig.width() * target_h / orig.height())
                self._movie.setScaledSize(QSize(target_w, target_h))
            gif_label.setMovie(self._movie)
            self._movie.start()
        layout.addWidget(gif_label)

        # ── Título ──
        titulo = QLabel("🚫  Acceso denegado", self)
        titulo.setAlignment(_ALIGN_CENTER)
        font_titulo = QFont()
        font_titulo.setPointSize(15)
        font_titulo.setBold(True)
        titulo.setFont(font_titulo)
        layout.addWidget(titulo)

        # ── Mensaje principal ──
        msg = QLabel(
            f"El usuario <b>{usuario}</b> no tiene permisos para acceder "
            "al módulo de <b>Gestión de Proveedores</b>.<br><br>"
            "Se requiere asignación activa al área "
            "<b>720002 – Mesa de Entradas/Salidas</b> "
            "con habilitación de impresión.",
            self,
        )
        msg.setWordWrap(True)
        msg.setAlignment(_ALIGN_LEFT | _ALIGN_TOP)  # type: ignore[arg-type]
        msg.setTextFormat(_RICH_TEXT)
        layout.addWidget(msg)

        # ── Datos del perfil (si los hay) ──
        if perfil:
            sep = QLabel("Datos de perfil del usuario:", self)
            sep.setStyleSheet("color: #8d99ae; font-size: 12px;")
            layout.addWidget(sep)

            campos = [
                ("Nombre",    str(perfil.get("descripcion", ""))),
                ("Username",  str(perfil.get("username", ""))),
                ("Área asig", str(perfil.get("area", 0))),
                ("Imprime",   "Sí" if perfil.get("imprime") == 1 else "No"),
                ("Estado",    "Activo" if perfil.get("estado") == 1 else "Inactivo"),
            ]
            for etiqueta, valor in campos:
                item = QLabel(f"  <b>{etiqueta}:</b>  {valor}", self)
                item.setTextFormat(_RICH_TEXT)
                item.setStyleSheet("font-size: 12px;")
                layout.addWidget(item)
        else:
            sin_perfil = QLabel(
                "No se encontró perfil de usuario en el sistema.", self
            )
            sin_perfil.setStyleSheet("color: #8d99ae; font-size: 12px;")
            layout.addWidget(sin_perfil)

        layout.addSpacing(8)

        # ── Botón Cerrar ──
        btn_cerrar = QPushButton("Cerrar", self)
        btn_cerrar.setFixedWidth(120)
        btn_cerrar.clicked.connect(self.accept)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_cerrar)
        layout.addLayout(btn_row)
