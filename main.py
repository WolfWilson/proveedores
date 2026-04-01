#!/usr/bin/env python
# coding: utf-8
# main.py

import sys
import re
from datetime import datetime
from typing import Optional, Dict, Any

from PyQt5.QtCore import Qt, QDate, QRegExp, pyqtSignal
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QFormLayout, QComboBox, QHBoxLayout, QDateEdit, QCheckBox, QScrollArea, QFrame
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
from anto_modulos.acceso import verificar_acceso
from anto_modulos.acceso_denegado_dialog import AccesoDenegadoDialog

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
# Panel de formulario (Nuevo / Edición)
# ──────────────────────────────
class VentanaNuevo(QWidget):
    guardado = pyqtSignal()  # emitido tras un guardado exitoso

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.datos: Dict = {}
        self._cuil_inicial: str = ""
        self._modo: Optional[str] = None  # "nuevo" | "editar"

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

        # Fecha Libre Deuda (opcional — puede enviarse como NULL)
        _SENTINEL_DATE = QDate(1900, 1, 1)  # fecha centinela = "sin valor"
        self.fecha_ult_lib_deuda = QDateEdit(self)
        self.fecha_ult_lib_deuda.setDisplayFormat(DATE_FMT_UI)
        self.fecha_ult_lib_deuda.setCalendarPopup(True)
        self.fecha_ult_lib_deuda.setMinimumDate(_SENTINEL_DATE)
        self.fecha_ult_lib_deuda.setSpecialValueText(" ")  # muestra vacío cuando está en la fecha centinela
        self.fecha_ult_lib_deuda.setDate(_SENTINEL_DATE)   # inicia vacío
        self.fecha_ult_lib_deuda.setDisabled(True)
        self.chk_sin_fecha = QCheckBox("Sin fecha", self)
        self.chk_sin_fecha.setChecked(True)
        self.chk_sin_fecha.toggled.connect(self._toggle_fecha)
        fecha_layout = QHBoxLayout()
        fecha_layout.addWidget(self.fecha_ult_lib_deuda)
        fecha_layout.addWidget(self.chk_sin_fecha)
        layout.addRow("Fecha Libre Deuda:", fecha_layout)

        # Botones Guardar / Cancelar
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar", self)
        self.btn_cancelar = QPushButton("Cancelar", self)
        self.btn_guardar.clicked.connect(self.guardar_nuevo_registro)
        self.btn_cancelar.clicked.connect(self.desactivar)
        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_cancelar)
        layout.addRow(btn_layout)

        # Inicia deshabilitado hasta que se busque un CUIL
        self.setEnabled(False)

    # ── Métodos públicos de activación ──

    def mostrar_datos(self, cuil: str, datos: Optional[Dict]) -> None:
        """Carga datos en el panel sin habilitarlo (solo lectura visual)."""
        self._limpiar_campos()
        self._cuil_inicial = cuil.strip()
        self.cuil.setText(self._cuil_inicial)
        self.datos = datos or {}
        self._modo = None
        if datos:
            self.cargar_datos(datos)
        self.setEnabled(False)
        debug("Formulario mostrando datos (bloqueado)", self._cuil_inicial)

    def activar_nuevo(self, cuil: str) -> None:
        self._limpiar_campos()
        self._cuil_inicial = cuil.strip()
        self.cuil.setText(self._cuil_inicial)
        self.datos = {}
        self._modo = "nuevo"
        self.setEnabled(True)
        self._toggle_fecha(self.chk_sin_fecha.isChecked())
        debug("Formulario activado en modo NUEVO para CUIL", self._cuil_inicial)

    def activar_editar(self, cuil: str, datos: Dict) -> None:
        # El panel ya tiene los datos cargados desde mostrar_datos(); solo habilitarlo
        self._cuil_inicial = cuil.strip()
        self.cuil.setText(self._cuil_inicial)
        self.datos = datos
        self._modo = "editar"
        self.setEnabled(True)
        self._toggle_fecha(self.chk_sin_fecha.isChecked())
        debug("Formulario habilitado en modo EDITAR para CUIL", self._cuil_inicial)

    def desactivar(self) -> None:
        self.setEnabled(False)
        self._limpiar_campos()
        self._modo = None
        self.datos = {}
        self._cuil_inicial = ""
        debug("Formulario desactivado")

    def _limpiar_campos(self) -> None:
        self.razon_social.clear()
        self.cuil.clear()
        self.localidad.clear()
        self.calle.clear()
        self.calle_nro.clear()
        self.dpto.clear()
        self.piso.clear()
        self.email.clear()
        self.provincia.setCurrentIndex(0)
        self.condicion_cta.setCurrentIndex(0)
        self.condicion_afip.setCurrentIndex(0)
        self.condicion_dgr.setCurrentIndex(0)
        self.condicion_gcia.setCurrentIndex(0)
        self.condicion_empleador.setCurrentIndex(0)
        self.forma_juridica.setCurrentIndex(0)
        self.chk_sin_fecha.setChecked(True)
        self._fecha_db: Optional[QDate] = None  # fecha original de la BD

    def _toggle_fecha(self, checked: bool) -> None:
        """Habilita/deshabilita el selector de fecha. Al desmarcar restaura la fecha de la BD, no la actual."""
        if checked:
            self.fecha_ult_lib_deuda.setDate(QDate(1900, 1, 1))  # muestra vacío
            self.fecha_ult_lib_deuda.setDisabled(True)
        else:
            # Restaurar la fecha original de la BD si existe; si no, usar la actual
            restaurar = self._fecha_db if (self._fecha_db is not None and self._fecha_db.isValid()) else QDate.currentDate()
            self.fecha_ult_lib_deuda.setDate(restaurar)
            self.fecha_ult_lib_deuda.setEnabled(True)

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
            # La query no devuelve CUIL; usar el valor buscado
            self.cuil.setText(self._cuil_inicial)
            debug("cargar_datos(): CUIL tomado del buscador", self._cuil_inicial)

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
            self._fecha_db = to_qdate(fecha)
            self.chk_sin_fecha.setChecked(False)
            self.fecha_ult_lib_deuda.setDate(self._fecha_db)
            debug("Set fecha desde datetime", fecha)
        elif isinstance(fecha, str):
            qd = QDate.fromString(fecha, DATE_FMT_DB)
            if qd.isValid():
                self._fecha_db = qd
                self.chk_sin_fecha.setChecked(False)
                self.fecha_ult_lib_deuda.setDate(self._fecha_db)
                debug("Set fecha desde str", fecha)
            else:
                self._fecha_db = None
                self.chk_sin_fecha.setChecked(True)
                warn("Formato de fecha no válido recibido desde DB.")
        else:
            # fecha es None en la DB → marcar "Sin fecha"
            self._fecha_db = None
            self.chk_sin_fecha.setChecked(True)
            debug("Fecha NULL en DB, sin fecha cargada", None)

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
        if self.chk_sin_fecha.isChecked():
            if self.datos:  # EDICIÓN: preservar el valor original de la BD
                fecha_orig = self.datos.get("fecha_ult_lib_deuda") if hasattr(self.datos, "get") else None
                if isinstance(fecha_orig, datetime):
                    fecha_ult_lib_deuda = fecha_orig.strftime("%Y-%m-%d")
                elif isinstance(fecha_orig, str) and fecha_orig:
                    fecha_ult_lib_deuda = fecha_orig
                else:
                    fecha_ult_lib_deuda = None
                debug("Sin fecha marcado en edición, preservando valor original", fecha_ult_lib_deuda)
            else:  # INSERCIÓN: enviar NULL
                fecha_ult_lib_deuda = None
        else:
            fecha_ult_lib_deuda = self.fecha_ult_lib_deuda.date().toString(DATE_FMT_DB)

        print("[DEBUG] Guardar -> modo:", self._modo)
        print("[DEBUG] Payload:", cuil, razon_social, provincia, localidad, calle, calle_nro,
              dpto, piso, email, condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
              condicion_empleador, forma_juridica, fecha_ult_lib_deuda)

        try:
            if self._modo == "editar":
                exito = actualizar_registro(
                    cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email,
                    condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
                    condicion_empleador, forma_juridica, fecha_ult_lib_deuda
                )
            else:
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
            self.desactivar()
            self.guardado.emit()
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
        self.setWindowTitle("Gestión de Proveedores")
        self.setMinimumSize(480, 800)

        root_layout = QVBoxLayout(self)
        root_layout.setSpacing(8)
        root_layout.setContentsMargins(12, 12, 12, 12)

        # ── Búsqueda ──
        search_layout = QHBoxLayout()
        self.cuil_input = QLineEdit(self)
        self.cuil_input.setPlaceholderText("Ingrese el CUIL (11 dígitos)")
        self.cuil_input.setValidator(QRegExpValidator(QRegExp(r"\d{0,11}"), self))
        search_layout.addWidget(self.cuil_input)
        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.buscar_cuil)
        search_layout.addWidget(self.search_button)
        root_layout.addLayout(search_layout)

        # ── Resultado y acciones ──
        self.result_label = QLabel("", self)
        root_layout.addWidget(self.result_label)

        btn_layout = QHBoxLayout()
        self.nuevo_button = QPushButton("Nuevo", self)
        self.nuevo_button.setObjectName("btnNuevo")
        self.nuevo_button.setEnabled(False)
        self.nuevo_button.clicked.connect(self._activar_nuevo)
        btn_layout.addWidget(self.nuevo_button)
        self.editar_button = QPushButton("Editar", self)
        self.editar_button.setObjectName("btnEditar")
        self.editar_button.setEnabled(False)
        self.editar_button.clicked.connect(self._activar_editar)
        btn_layout.addWidget(self.editar_button)
        root_layout.addLayout(btn_layout)

        # ── Formulario embebido (siempre visible, inicia deshabilitado) ──
        self.form_panel = VentanaNuevo(parent=self)
        self.form_panel.guardado.connect(self._on_guardado)
        scroll = QScrollArea(self)
        scroll.setWidget(self.form_panel)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        root_layout.addWidget(scroll)

    def showEvent(self, e) -> None:
        super().showEvent(e)
        center_on_screen(self)

    def buscar_cuil(self) -> None:
        cuil = self.cuil_input.text().strip()
        debug("Buscar CUIL", cuil)
        if len(cuil) != 11:
            QMessageBox.critical(self, "Error", "El CUIL debe tener 11 dígitos.")
            return

        # Desactivar formulario si estaba activo
        if self.form_panel.isEnabled():
            self.form_panel.desactivar()

        try:
            resultado = ejecutar_procedimiento_almacenado(cuil)
            debug("Resultado SP existe?", resultado)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al consultar: {e}")
            return

        if resultado == 1:
            self.result_label.setText(f"CUIL {cuil} encontrado en la base de datos.")
            self.editar_button.setEnabled(True)
            self.nuevo_button.setEnabled(False)
            # Cargar datos en el panel (deshabilitado, solo lectura visual)
            try:
                datos = obtener_datos_por_cuil(cuil)
            except Exception as e:
                datos = None
                warn(f"No se pudieron precargar datos: {e}")
            self.form_panel.mostrar_datos(cuil, datos)
            self._datos_cache = datos  # guardar para no re-consultar al editar
        else:
            self.result_label.setText(f"CUIL {cuil} no encontrado en la base de datos.")
            self.nuevo_button.setEnabled(True)
            self.editar_button.setEnabled(False)
            self._datos_cache = None
            self.form_panel.mostrar_datos(cuil, None)

    def _activar_nuevo(self) -> None:
        cuil = self.cuil_input.text().strip()
        debug("Activar NUEVO para CUIL", cuil)
        self.form_panel.activar_nuevo(cuil)

    def _activar_editar(self) -> None:
        cuil = self.cuil_input.text().strip()
        datos = getattr(self, "_datos_cache", None)
        if datos:
            self.form_panel.activar_editar(cuil, datos)
        else:
            # Fallback: re-consultar si el cache no está
            debug("Cache vacío, re-consultando datos para CUIL", cuil)
            try:
                datos = obtener_datos_por_cuil(cuil)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al obtener datos: {e}")
                return
            if datos:
                self.form_panel.activar_editar(cuil, datos)
            else:
                QMessageBox.critical(self, "Error", "No se pudieron cargar los datos para editar.")

    def _on_guardado(self) -> None:
        self.nuevo_button.setEnabled(False)
        self.editar_button.setEnabled(False)
        self.result_label.setText("")
        self.cuil_input.clear()

# ──────────────────────────────
# Main
# ──────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    # ── Control de acceso ──────────────────────────────────────
    acceso, usuario, perfil = verificar_acceso()
    if not acceso:
        dlg = AccesoDenegadoDialog(usuario=usuario, perfil=perfil)
        center_on_screen(dlg)
        dlg.exec_()
        sys.exit(0)
    # ───────────────────────────────────────────────────────────

    win = CUILSearchApp()
    win.setWindowIcon(QIcon(ICON_MAIN))
    win.show()
    sys.exit(app.exec_())

