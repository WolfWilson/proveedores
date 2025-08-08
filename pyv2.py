import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QComboBox, QHBoxLayout, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from datetime import datetime
from anto_modulos.anto_conexion import (
    ejecutar_procedimiento_almacenado,
    insertar_nuevo_registro,
    obtener_datos_por_cuil,
    actualizar_registro
)
from anto_modulos.style import STYLE
from anto_modulos.centrar_ventana import center_on_screen  # Importar la función para centrar la ventana


class VentanaNuevo(QDialog):
    def __init__(self, cuil_previamente_buscado, parent=None, datos=None):
        super().__init__(parent)

        self.setWindowTitle('Editar Registro' if datos else 'Nuevo Registro')
        self.setGeometry(200, 200, 400, 700)

        self.datos = datos

        # Layout
        layout = QFormLayout()

        # Campo para "Razón Social"
        self.razon_social = QLineEdit(self)
        self.razon_social.setPlaceholderText("Ingrese la razón social")
        layout.addRow('Razón Social:', self.razon_social)

        # Campo para "CUIL" (no editable y con el valor previamente buscado)
        self.cuil = QLineEdit(self)
        self.cuil.setText(cuil_previamente_buscado)  # Usar el CUIL previamente buscado
        self.cuil.setReadOnly(True)  # Campo de solo lectura
        layout.addRow('CUIL:', self.cuil)

        # ComboBox para "Provincia"
        self.provincia = QComboBox(self)
        provincias = [
            "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos", 
            "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", 
            "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
            "Santiago del Estero", "Tierra del Fuego", "Tucumán", "Ciudad Autónoma de Buenos Aires"
        ]
        self.provincia.addItems(provincias)
        layout.addRow('Provincia:', self.provincia)

        # Campo para "Localidad"
        self.localidad = QLineEdit(self)
        self.localidad.setPlaceholderText("Ingrese la localidad")
        layout.addRow('Localidad:', self.localidad)

        # Campo para "Calle" y "Nro" en la misma línea
        calle_nro_layout = QHBoxLayout()
        self.calle = QLineEdit(self)
        self.calle.setPlaceholderText("Ingrese la calle")
        calle_nro_layout.addWidget(self.calle)

        self.calle_nro = QLineEdit(self)
        self.calle_nro.setPlaceholderText("Nro")
        calle_nro_layout.addWidget(self.calle_nro)

        layout.addRow('Calle y Nro:', calle_nro_layout)

        # Campo para "Dpto" y "Piso" en la misma línea
        dpto_piso_layout = QHBoxLayout()
        self.dpto = QLineEdit(self)
        self.dpto.setPlaceholderText("Dpto")
        dpto_piso_layout.addWidget(self.dpto)

        self.piso = QLineEdit(self)
        self.piso.setPlaceholderText("Piso")
        dpto_piso_layout.addWidget(self.piso)

        layout.addRow('Dpto y Piso:', dpto_piso_layout)

        # Campo para "Email"
        self.email = QLineEdit(self)
        self.email.setPlaceholderText("Ingrese el email")
        layout.addRow('Email:', self.email)

        # Campo para "Condicion CTA"
        self.condicion_cta = QComboBox(self)
        self.condicion_cta.addItems(["Activo", "Baja"])  # Agrega las opciones al combobox
        layout.addRow('Condición CTA:', self.condicion_cta)




       # Campo para "Condición en AFIP"
        self.condicion_afip = QComboBox(self)
        self.condicion_afip.addItems([
        "Monotributista", "No Informado", "Condición B", "Exento", 
         "Responsable Inscripto", "Responsable No Inscripto", 
            "Código Invalido", "Null"
        ])
        layout.addRow('Condición en AFIP:', self.condicion_afip)


        # Campo para "Condición DGR"
        self.condicion_dgr = QComboBox(self)
        self.condicion_dgr.addItems([
        "Inscripto", "No Inscripto", "No Informado", "Exento", 
        "No Sujeto a Retención", "Convenio Multilateral", 
        "Condición C", "Null"
            ])
        layout.addRow('Condición DGR:', self.condicion_dgr)


        # Campo para "Condición GCIA"
        self.condicion_gcia = QComboBox(self)
        self.condicion_gcia.addItems([
        "Inscripto", "No Inscripto", "No Informado", "Exento", 
        "Monotributista", "No Sujeto a Retención", 
        "Convenio Multilateral", "Condición D", "Código Inválido", "Null"
        ])
        layout.addRow('Condición GCIA:', self.condicion_gcia)


        # Campo para "Condición Empleador"
        self.condicion_empleador = QComboBox(self)
        self.condicion_empleador.addItems(["Empleador", "No Empleador", "No Informado"])  # Opciones en el ComboBox
        layout.addRow('Condición Empleador:', self.condicion_empleador)


        # Campo para "Forma Jurídica"
        self.forma_juridica = QComboBox(self)
        self.forma_juridica.addItems([
         "Persona Jurídica", "Colectiva", "Responsabilidad Limitada", "Sociedad Anónima", "Mutual",
            "Asociación", "No Informado", "Asociación Civil", "Cooperativa", "En Formación", 
            "Empresa del Estado", "Sociedad de Derecho", "No Empleador", "Organismo Público", 
            "Agrupación de Colaboración Empresaria", "Fundación", "Unipersonal", "Otros"
        ])
        layout.addRow('Forma Jurídica:', self.forma_juridica)


       # Campo para "Fecha Libre Deuda"
        self.fecha_ult_lib_deuda = QDateEdit(self)
        self.fecha_ult_lib_deuda.setDisplayFormat("dd-MM-yyyy")  # Formato de fecha día-mes-año
        self.fecha_ult_lib_deuda.setCalendarPopup(True)  # Habilita el calendario desplegable
        self.fecha_ult_lib_deuda.setDate(QDate.currentDate())  # Establece la fecha actual como predeterminada
        layout.addRow('Fecha Libre Deuda:', self.fecha_ult_lib_deuda)



        # Botones de aceptar y cancelar
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.guardar_nuevo_registro)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)

        self.setLayout(layout)
        
        if datos:
            self.cargar_datos(datos)
        
    def cargar_datos(self, datos):
        # Configurar el CUIL con el valor de la búsqueda y establecerlo como no editable
        cuil_value = datos.get("cuil", "")
        if cuil_value:
            self.cuil.setText(cuil_value)
            self.cuil.setReadOnly(True)  # Asegura que el campo CUIL sea de solo lectura
        else:
            print("Advertencia: El CUIL no está presente en los datos o es inválido.")

        # Configurar campos de texto
        self.razon_social.setText(datos.get("razon_social", ""))
        self.localidad.setText(datos.get("localidad", ""))
        self.calle.setText(datos.get("calle", ""))
        self.calle_nro.setText(datos.get("calle_nro", ""))
        self.dpto.setText(datos.get("dpto", ""))
        self.piso.setText(datos.get("piso", ""))
        self.email.setText(datos.get("email", ""))

        # Configurar ComboBox usando la función auxiliar
        self.set_combobox_value(self.provincia, datos.get("provincia", ""))
        self.set_combobox_value(self.condicion_cta, datos.get("condicion_cta", ""))
        self.set_combobox_value(self.condicion_afip, datos.get("condicion_afip", ""))
        self.set_combobox_value(self.condicion_dgr, datos.get("condicion_dgr", ""))
        self.set_combobox_value(self.condicion_gcia, datos.get("condicion_gcia", ""))
        self.set_combobox_value(self.condicion_empleador, datos.get("condicion_empleador", ""))
        self.set_combobox_value(self.forma_juridica, datos.get("forma_juridica", ""))

        # Cargar fecha en QDateEdit si existe y está en el formato correcto
        fecha = datos.get("fecha_ult_lib_deuda")
        if fecha:
            if isinstance(fecha, datetime):  # Verificar si es un objeto datetime
                self.fecha_ult_lib_deuda.setDate(fecha.date())
            elif isinstance(fecha, str):  # Si es cadena, intentar convertirla a QDate
                fecha_obj = QDate.fromString(fecha, "yyyy-MM-dd")
                if fecha_obj.isValid():
                    self.fecha_ult_lib_deuda.setDate(fecha_obj)
                else:
                    print("Error: Formato de fecha no válido en los datos de la base de datos.")

    def set_combobox_value(self, combobox, value):
        """
        Configura el valor de un QComboBox si coincide con uno de los elementos.
        Si no coincide, muestra una advertencia en la consola.
        """
        # Normalizar valor para evitar errores de comparación
        value_normalized = value.strip().lower()
        items = [combobox.itemText(i).strip().lower() for i in range(combobox.count())]

        if value_normalized in items:
            index = items.index(value_normalized)
            combobox.setCurrentIndex(index)
        else:
            print(f"Advertencia: El valor '{value}' no coincide con ninguna opción en el ComboBox '{combobox.objectName()}'.")


            
        # Debugging: imprimir los valores asignados para verificar si son correctos
        print("Datos cargados en la ventana de edición:")
        print("Razón Social:", self.razon_social.text())
        print("Provincia:", self.provincia.currentText())
        print("Condición CTA:", self.condicion_cta.currentText())
        print("Condición en AFIP:", self.condicion_afip.currentText())
        print("Condición DGR:", self.condicion_dgr.currentText())
        print("Condición GCIA:", self.condicion_gcia.currentText())
        print("Condición Empleador:", self.condicion_empleador.currentText())
        print("Forma Jurídica:", self.forma_juridica.currentText())
        print("Fecha Libre Deuda:", self.fecha_ult_lib_deuda.date().toString("yyyy-MM-dd"))

    def guardar_nuevo_registro(self):
        # Obtén los valores de los campos
        razon_social = self.razon_social.text().strip()
        cuil = self.cuil.text()
        provincia = self.provincia.currentText()
        localidad = self.localidad.text().strip()
        calle = self.calle.text().strip()
        calle_nro = self.calle_nro.text().strip()
        dpto = self.dpto.text().strip()
        piso = self.piso.text().strip()
        email = self.email.text().strip()
        condicion_cta = self.condicion_cta.currentText()
        condicion_afip = self.condicion_afip.currentText()
        condicion_dgr = self.condicion_dgr.currentText()
        condicion_gcia = self.condicion_gcia.currentText()
        condicion_empleador = self.condicion_empleador.currentText()
        forma_juridica = self.forma_juridica.currentText()
        fecha_ult_lib_deuda = self.fecha_ult_lib_deuda.date().toString("yyyy-MM-dd")

        # Validaciones básicas
        if not razon_social:
            self.mostrar_mensaje_error("La Razón Social no puede estar vacía.")
            return
        if len(cuil) != 11 or not cuil.isdigit():
            self.mostrar_mensaje_error("El CUIT debe tener exactamente 11 dígitos numéricos.")
            return
        if not localidad:
            self.mostrar_mensaje_error("La Localidad no puede estar vacía.")
            return
        if not calle:
            self.mostrar_mensaje_error("La Calle no puede estar vacía.")
            return
        
        if self.datos:  # Si `self.datos` existe, estamos en modo edición
            exito = actualizar_registro(
                cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email,
                condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
                condicion_empleador, forma_juridica, fecha_ult_lib_deuda
             )
        else:  # Si no hay datos, estamos en modo inserción
            exito = insertar_nuevo_registro(
                cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email,
                condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
                condicion_empleador, forma_juridica, fecha_ult_lib_deuda, None
        )

        if exito:
            QMessageBox.information(self, 'Éxito', 'Registro guardado con éxito.')
            self.accept()  # Cierra la ventana
        else:
            QMessageBox.critical(self, 'Error', 'Error al guardar el registro.')

        self.accept()  # Cierra el diálogo

    def mostrar_mensaje_error(self, mensaje):
        # Mostrar un mensaje de error en una ventana emergente
        QMessageBox.critical(self, 'Error', mensaje)



# Definición de la clase CUILSearchApp
class CUILSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Configuración de la ventana principal
        self.setWindowTitle('Buscar CUIL')
        self.setGeometry(100, 100, 300, 150)

        # Establecer el ícono de la ventana principal
        self.setWindowIcon(QIcon("userprofile4.png"))  # Ruta relativa del archivo del ícono

        # Layout
        layout = QVBoxLayout()

        # Campo de entrada para el CUIL
        self.cuil_input = QLineEdit(self)
        self.cuil_input.setPlaceholderText('Ingrese el CUIL')
        layout.addWidget(self.cuil_input)

        # Botón de búsqueda
        self.search_button = QPushButton('Buscar', self)
        self.search_button.clicked.connect(self.buscar_cuil)
        layout.addWidget(self.search_button)

        # Botones "Nuevo" y "Editar"
        self.nuevo_button = QPushButton('Nuevo', self)
        self.nuevo_button.setEnabled(False)
        self.nuevo_button.clicked.connect(self.mostrar_ventana_nuevo)
        layout.addWidget(self.nuevo_button)

        self.editar_button = QPushButton('Editar', self)
        self.editar_button.setEnabled(False)
        self.editar_button.clicked.connect(self.mostrar_ventana_editar)
        layout.addWidget(self.editar_button)

        # Etiqueta para mensajes
        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        # Establecer el layout principal
        self.setLayout(layout)

    def buscar_cuil(self):
        cuil = self.cuil_input.text()
        if len(cuil) != 11 or not cuil.isdigit():
            self.mostrar_mensaje_error("El CUIL debe ser un número de 11 dígitos.")
            return

        resultado = ejecutar_procedimiento_almacenado(cuil)
        if resultado == 1:
            self.result_label.setText(f"El CUIL {cuil} existe en la base de datos.")
            self.editar_button.setEnabled(True)
            self.nuevo_button.setEnabled(False)
        else:
            self.result_label.setText(f"El CUIL {cuil} no existe en la base de datos.")
            self.nuevo_button.setEnabled(True)
            self.editar_button.setEnabled(False)

    def mostrar_ventana_nuevo(self):
        cuil = self.cuil_input.text()
        ventana_nuevo = VentanaNuevo(cuil, self)
        ventana_nuevo.exec_()

    def mostrar_ventana_editar(self):
        cuil = self.cuil_input.text()
        datos = obtener_datos_por_cuil(cuil)
        if datos:
            ventana_editar = VentanaNuevo(cuil, self, datos=datos)
            ventana_editar.exec_()
        else:
            QMessageBox.critical(self, 'Error', 'No se pudieron cargar los datos para editar.')

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.critical(self, 'Error', mensaje)

# Código principal para ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    ventana = CUILSearchApp()
    ventana.setWindowIcon(QIcon("userprofile4.png"))
    center_on_screen(ventana)       # ← luego centrar
    ventana.show()                  # ← primero mostrar
    

    sys.exit(app.exec_())
