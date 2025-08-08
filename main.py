#!/usr/bin/env python
# coding: utf-8
# main.py

import sys
import re
from datetime import datetime
from typing import Optional, Dict, Any

from PyQt5.QtCore import Qt, QDate, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QDialog, QFormLayout, QDialogButtonBox, QComboBox, QHBoxLayout, QDateEdit
)

from anto_modulos.anto_conexion import (
    ejecutar_procedimiento_almacenado,
    insertar_nuevo_registro,
    obtener_datos_por_cuil,
    actualizar_registro,
)
from anto_modulos.style import STYLE
from anto_modulos.centrar_ventana import center_on_screen
from anto_modulos.resources import ICON_MAIN, DATE_ARROW_DOWN

# ──────────────────────────────
# Configuración/Constantes
# ──────────────────────────────
DATE_FMT_DB = "yyyy-MM-dd"
DATE_FMT_UI = "dd-MM-yyyy"
PROVINCIAS = [
    "Buenos Aires","Catamarca","Chaco","Chubut","Córdoba","Corrientes","Entre Ríos","Formosa","Jujuy",
    "La Pampa","La Rioja","Mendoza","Misiones","Neuquén","Río Negro","Salta","San Juan","San Luis",
    "Santa Cruz","Santa Fe","Santiago del Estero","Tierra del Fuego","Tucumán","Ciudad Autónoma de Buenos Aires",
]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# ──────────────────────────────
# Helpers debug/log
# ──────────────────────────────
def debug(msg: str, data: Any = None) -> None:
    print(f"[DEBUG] {msg}" + (f" -> {repr(data)}" if data is not None else ""))

def warn(msg: str) -> None:
    print(f"[WARN] {msg}")

def to_qdate(value: datetime) -> QDate:
    return QDate(value.year, value.month, value.day)

def not_empty(text: str) -> bool:
    return bool(text and text.strip())

def keys_of(obj: Any):
    try:
        return list(obj.keys())  # dict-like
    except Exception:
        try:
            return dir(obj)[:10]  # algo representativo si es fila/row
        except Exception:
            return ["<sin claves>"]

# ──────────────────────────────
# Diálogo Nuevo/Edición
# ──────────────────────────────
class VentanaNuevo(QDialog):
    def __init__(self, cuil_previamente_buscado: str, parent: Optional[QWidget] = None, datos: Optional[Dict] = None):
        super().__init__(parent)

        self.setWindowTitle("Editar Registro" if datos else "Nuevo Registro")
        self.setModal(True)
        self.setFixedWidth(420)

        self.datos = datos or {}
        self._cuil_inicial = cuil_previamente_buscado.strip()
        debug("Init VentanaNuevo con CUIL", self._cuil_inicial)
        debug("Datos recibidos (tipo / claves)", (type(self.datos).__name__, keys_of(self.datos)))

        layout = QFormLayout(self)

        # Razón Social
        self.razon_social = QLineEdit(self); self.razon_social.setPlaceholderText("Ingrese la razón social")
        layout.addRow("Razón Social:", self.razon_social)

        # CUIL (solo lectura)
        self.cuil = QLineEdit(self)
        self.cuil.setText(self._cuil_inicial)
        self.cuil.setReadOnly(True)
        self.cuil.setValidator(QRegExpValidator(QRegExp(r"\d{0,11}"), self))
        layout.addRow("CUIL:", self.cuil)

        # Provincia
        self.provincia = QComboBox(self); self.provincia.addItems(PROVINCIAS)
        layout.addRow("Provincia:", self.provincia)

        # Localidad
        self.localidad = QLineEdit(self); self.localidad.setPlaceholderText("Ingrese la localidad")
        layout.addRow("Localidad:", self.localidad)

        # Calle y Número
        calle_nro_layout = QHBoxLayout()
        self.calle = QLineEdit(self); self.calle.setPlaceholderText("Calle")
        self.calle_nro = QLineEdit(self); self.calle_nro.setPlaceholderText("Nro")
        self.calle_nro.setValidator(QRegExpValidator(QRegExp(r"\d{0,5}"), self))
        calle_nro_layout.addWidget(self.calle); calle_nro_layout.addWidget(self.calle_nro)
        layout.addRow("Calle y Nro:", calle_nro_layout)

        # Dpto y Piso
        dpto_piso_layout = QHBoxLayout()
        self.dpto = QLineEdit(self); self.dpto.setPlaceholderText("Dpto")
        self.piso = QLineEdit(self); self.piso.setPlaceholderText("Piso")
        self.piso.setValidator(QRegExpValidator(QRegExp(r"\d{0,3}"), self))
        dpto_piso_layout.addWidget(self.dpto); dpto_piso_layout.addWidget(self.piso)
        layout.addRow("Dpto y Piso:", dpto_piso_layout)

        # Email
        self.email = QLineEdit(self); self.email.setPlaceholderText("Ingrese el email")
        layout.addRow("Email:", self.email)

        # Combos de condición
        self.condicion_cta = QComboBox(self); self.condicion_cta.addItems(["Activo", "Baja"])
        layout.addRow("Condición CTA:", self.condicion_cta)

        self.condicion_afip = QComboBox(self); self.condicion_afip.addItems([
            "Monotributista", "No Informado", "Condición B", "Exento",
            "Responsable Inscripto", "Responsable No Inscripto", "Código Invalido", "Null"
        ])
        layout.addRow("Condición en AFIP:", self.condicion_afip)

        self.condicion_dgr = QComboBox(self); self.condicion_dgr.addItems([
            "Inscripto", "No Inscripto", "No Informado", "Exento",
            "No Sujeto a Retención", "Convenio Multilateral", "Condición C", "Null"
        ])
        layout.addRow("Condición DGR:", self.condicion_dgr)

        self.condicion_gcia = QComboBox(self); self.condicion_gcia.addItems([
            "Inscripto", "No Inscripto", "No Informado", "Exento",
            "Monotributista", "No Sujeto a Retención", "Convenio Multilateral",
            "Condición D", "Código Inválido", "Null"
        ])
        layout.addRow("Condición GCIA:", self.condicion_gcia)

        self.condicion_empleador = QComboBox(self); self.condicion_empleador.addItems(["Empleador", "No Empleador", "No Informado"])
        layout.addRow("Condición Empleador:", self.condicion_empleador)

        self.forma_juridica = QComboBox(self); self.forma_juridica.addItems([
            "Persona Jurídica","Colectiva","Responsabilidad Limitada","Sociedad Anónima","Mutual",
            "Asociación","No Informado","Asociación Civil","Cooperativa","En Formación",
            "Empresa del Estado","Sociedad de Derecho","No Empleador","Organismo Público",
            "Agrupación de Colaboración Empresaria","Fundación","Unipersonal","Otros"
        ])
        layout.addRow("Forma Jurídica:", self.forma_juridica)

        # Fecha Libre Deuda
        self.fecha_ult_lib_deuda = QDateEdit(self)
        self.fecha_ult_lib_deuda.setDisplayFormat(DATE_FMT_UI)
        self.fecha_ult_lib_deuda.setCalendarPopup(True)
        self.fecha_ult_lib_deuda.setDate(QDate.currentDate())
        layout.addRow("Fecha Libre Deuda:", self.fecha_ult_lib_deuda)

        # Botones OK/Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        self.buttons.accepted.connect(self.guardar_nuevo_registro)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)

        # Cargar datos si es edición
        if self.datos:
            self.cargar_datos(self.datos)

    def showEvent(self, e) -> None:
        super().showEvent(e)
        center_on_screen(self)

    def set_combobox_value(self, combobox: QComboBox, value: str) -> None:
        value_norm = (value or "").strip().lower()
        items_norm = [combobox.itemText(i).strip().lower() for i in range(combobox.count())]
        if value_norm in items_norm:
            combobox.setCurrentIndex(items_norm.index(value_norm))
        else:
            warn(f"Valor '{value}' no coincide con opciones de ComboBox '{combobox.objectName() or combobox.__class__.__name__}'")

    def cargar_datos(self, datos: Dict) -> None:
        debug("cargar_datos() – claves", keys_of(datos))

        # No forzar CUIL desde datos si no existe; mantener el del constructor
        cuil_value = (datos.get("cuil") or "").strip() if hasattr(datos, "get") else ""
        if cuil_value:
            if cuil_value != self._cuil_inicial:
                warn(f"CUIL provisto en datos difiere del buscado: datos={cuil_value} vs buscado={self._cuil_inicial}")
            self.cuil.setText(cuil_value)
        else:
            debug("cargar_datos(): no vino 'cuil' en datos, se mantiene el del constructor", self._cuil_inicial)

        # Campos texto
        for label, widget, key in [
            ("razon_social", self.razon_social, "razon_social"),
            ("localidad", self.localidad, "localidad"),
            ("calle", self.calle, "calle"),
            ("calle_nro", self.calle_nro, "calle_nro"),
            ("dpto", self.dpto, "dpto"),
            ("piso", self.piso, "piso"),
            ("email", self.email, "email"),
        ]:
            val = (datos.get(key) if hasattr(datos, "get") else None) or ""
            widget.setText(str(val))
            debug(f"Set campo {label}", val)

        # Combos
        for (combo, key) in [
            (self.provincia, "provincia"),
            (self.condicion_cta, "condicion_cta"),
            (self.condicion_afip, "condicion_afip"),
            (self.condicion_dgr, "condicion_dgr"),
            (self.condicion_gcia, "condicion_gcia"),
            (self.condicion_empleador, "condicion_empleador"),
            (self.forma_juridica, "forma_juridica"),
        ]:
            val = (datos.get(key) if hasattr(datos, "get") else None) or ""
            self.set_combobox_value(combo, val)
            debug(f"Set combo {key}", val)

        # Fecha
        fecha = (datos.get("fecha_ult_lib_deuda") if hasattr(datos, "get") else None)
        if isinstance(fecha, datetime):
            self.fecha_ult_lib_deuda.setDate(to_qdate(fecha))
            debug("Set fecha desde datetime", fecha)
        elif isinstance(fecha, str):
            qd = QDate.fromString(fecha, DATE_FMT_DB)
            if qd.isValid():
                self.fecha_ult_lib_deuda.setDate(qd)
                debug("Set fecha desde str", fecha)
            else:
                warn("Formato de fecha no válido recibido desde DB.")

    def _email_valido(self, email: str) -> bool:
        return not email or bool(EMAIL_RE.match(email))

    def _validar_formulario(self) -> Optional[str]:
        cuil = self.cuil.text().strip()
        if len(cuil) != 11 or not cuil.isdigit():
            return "El CUIL debe tener exactamente 11 dígitos numéricos."
        if not not_empty(self.razon_social.text()):
            return "La Razón Social no puede estar vacía."
        if not not_empty(self.localidad.text()):
            return "La Localidad no puede estar vacía."
        if not not_empty(self.calle.text()):
            return "La Calle no puede estar vacía."
        if not self._email_valido(self.email.text().strip()):
            return "El Email no es válido."
        return None

    def guardar_nuevo_registro(self) -> None:
        # Validación previa
        msg_error = self._validar_formulario()
        if msg_error:
            QMessageBox.critical(self, "Error", msg_error)
            return

        # Recolectar valores
        cuil = self.cuil.text().strip()
        razon_social = self.razon_social.text().strip()
        provincia = self.provincia.currentText().strip()
        localidad = self.localidad.text().strip()
        calle = self.calle.text().strip()
        calle_nro = self.calle_nro.text().strip()
        dpto = self.dpto.text().strip()
        piso = self.piso.text().strip()
        email = self.email.text().strip()
        condicion_cta = self.condicion_cta.currentText().strip()
        condicion_afip = self.condicion_afip.currentText().strip()
        condicion_dgr = self.condicion_dgr.currentText().strip()
        condicion_gcia = self.condicion_gcia.currentText().strip()
        condicion_empleador = self.condicion_empleador.currentText().strip()
        forma_juridica = self.forma_juridica.currentText().strip()
        fecha_ult_lib_deuda = self.fecha_ult_lib_deuda.date().toString(DATE_FMT_DB)

        # Debug útil
        print("[DEBUG] Guardar -> modo:", "EDICION" if self.datos else "INSERCION")
        print("[DEBUG] Payload ordenado:", cuil, razon_social, provincia, localidad, calle, calle_nro,
              dpto, piso, email, condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
              condicion_empleador, forma_juridica, fecha_ult_lib_deuda)

        try:
            if self.datos:  # EDICIÓN (posicional)
                exito = actualizar_registro(
                    cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email,
                    condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
                    condicion_empleador, forma_juridica, fecha_ult_lib_deuda
                )
            else:  # INSERCIÓN (posicional, con None final si tu función lo requiere)
                exito = insertar_nuevo_registro(
                    cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email,
                    condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
                    condicion_empleador, forma_juridica, fecha_ult_lib_deuda, None
                )
        except TypeError as te:
            print("[ERROR] Firma de función no compatible:", te)
            QMessageBox.critical(self, "Error", f"Parámetros inválidos al guardar: {te}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar: {e}")
            return

        if exito:
            QMessageBox.information(self, "Éxito", "Registro guardado con éxito.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el registro.")

# ──────────────────────────────
# Ventana principal
# ──────────────────────────────
class CUILSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Buscar CUIL")
        self.setFixedSize(320, 240)
        self.setWindowIcon(QIcon("userprofile4.png"))

        layout = QVBoxLayout(self)

        self.cuil_input = QLineEdit(self); self.cuil_input.setPlaceholderText("Ingrese el CUIL (11 dígitos)")
        self.cuil_input.setValidator(QRegExpValidator(QRegExp(r"\d{0,11}"), self))
        layout.addWidget(self.cuil_input)

        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.buscar_cuil)
        layout.addWidget(self.search_button)

        self.nuevo_button = QPushButton("Nuevo", self); self.nuevo_button.setObjectName("btnNuevo")
        self.nuevo_button.setEnabled(False); self.nuevo_button.clicked.connect(self.mostrar_ventana_nuevo)
        layout.addWidget(self.nuevo_button)

        self.editar_button = QPushButton("Editar", self); self.editar_button.setObjectName("btnEditar")
        self.editar_button.setEnabled(False); self.editar_button.clicked.connect(self.mostrar_ventana_editar)
        layout.addWidget(self.editar_button)

        self.result_label = QLabel("", self); layout.addWidget(self.result_label)

    def showEvent(self, e) -> None:
        super().showEvent(e)
        center_on_screen(self)

    def buscar_cuil(self) -> None:
        cuil = self.cuil_input.text().strip()
        debug("Buscar CUIL", cuil)
        if len(cuil) != 11:
            self.mostrar_mensaje_error("El CUIL debe tener 11 dígitos.")
            return

        try:
            resultado = ejecutar_procedimiento_almacenado(cuil)
            debug("Resultado SP existe?", resultado)
        except Exception as e:
            self.mostrar_mensaje_error(f"Error al consultar: {e}")
            return

        if resultado == 1:
            self.result_label.setText(f"El CUIL {cuil} existe en la base de datos.")
            self.editar_button.setEnabled(True); self.nuevo_button.setEnabled(False)
        else:
            self.result_label.setText(f"El CUIL {cuil} no existe en la base de datos.")
            self.nuevo_button.setEnabled(True); self.editar_button.setEnabled(False)

    def mostrar_ventana_nuevo(self) -> None:
        cuil = self.cuil_input.text().strip()
        debug("Abrir NUEVO para CUIL", cuil)
        dlg = VentanaNuevo(cuil, self)
        dlg.exec_()

    def mostrar_ventana_editar(self) -> None:
        cuil = self.cuil_input.text().strip()
        debug("Abrir EDITAR para CUIL", cuil)
        try:
            datos = obtener_datos_por_cuil(cuil)
            debug("obtener_datos_por_cuil tipo/claves", (type(datos).__name__, keys_of(datos) if datos else []))
        except Exception as e:
            self.mostrar_mensaje_error(f"Error al obtener datos: {e}")
            return

        if datos:
            dlg = VentanaNuevo(cuil, self, datos=datos)
            dlg.exec_()
        else:
            QMessageBox.critical(self, "Error", "No se pudieron cargar los datos para editar.")

    def mostrar_mensaje_error(self, mensaje: str) -> None:
        QMessageBox.critical(self, "Error", mensaje)

# ──────────────────────────────
# Main
# ──────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)  # opcional, si no te importa el style, comentalo
    win = CUILSearchApp()
    win.setWindowIcon(QIcon(ICON_MAIN))
    win.show()
    sys.exit(app.exec_())  # PyQt5 usa exec_()

