# 🏢 Gestión de Proveedores

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-41CD52?logo=qt&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2014+-red?logo=microsoft-sql-server&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-orange)

## 📌 Descripción

**Gestión de Proveedores** es una aplicación de escritorio desarrollada en **Python** con **PyQt5**, diseñada para administrar el padrón de proveedores de una organización. Permite buscar, registrar y editar proveedores por CUIL con conexión directa a una base de datos **SQL Server** usando autenticación Windows integrada.

El acceso al módulo está **controlado por permisos**: solo usuarios con asignación activa al área 720002 y habilitación de impresión pueden ingresar, verificado automáticamente mediante el SP `dbo.Perfil_usuario_new`.

---

## ✨ Características

- 🔍 **Búsqueda por CUIL** (11 dígitos) con validación en tiempo real.
- ➕ **Alta de nuevos proveedores** mediante formulario completo.
- ✏️ **Edición de registros existentes** con precarga automática de datos.
- 📋 **Validación de datos** antes de insertar o actualizar (CUIL, email, campos obligatorios).
- 🔐 **Control de acceso** por perfil de usuario (SP `Perfil_usuario_new`): ventana de denegación con GIF animado si no tiene permisos.
- 🎨 **Interfaz oscura moderna** con estilos QSS parametrizables.
- 🏗️ **Compatible con PyInstaller** para distribuir como `.exe` standalone.
- 🖥️ **Centrado automático** de ventanas en pantalla.

---

## 🛠️ Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Lenguaje principal |
| [PyQt5](https://riverbankcomputing.com/software/pyqt/) | 5.15+ | Interfaz gráfica |
| [pyodbc](https://github.com/mkleehammer/pyodbc) | - | Conexión a SQL Server |
| [Microsoft SQL Server](https://www.microsoft.com/sql-server) | 2014+ | Base de datos |
| [PyInstaller](https://pyinstaller.org/) | - | Empaquetado a `.exe` |

**Módulos estándar usados:** `sys`, `re`, `datetime`, `typing`, `os`, `getpass`

---

## 📂 Estructura del Proyecto

```
proveedores/
├── main.py                          # ✅ Punto de entrada — UI principal (VentanaNuevo + CUILSearchApp)
├── pyv2.py                          # ⚠️ Versión anterior de la UI (no activo)
├── main.spec                        # Configuración de PyInstaller
├── build.bat                        # Script de compilación con PyInstaller (--onedir)
├── test_perfil_usuario.py           # Script de diagnóstico de permisos (Perfil_usuario_new)
│
├── anto_modulos/
│   ├── __init__.py
│   ├── anto_conexion.py             # ✅ Conexión SQL Server + CRUD (funciones activas)
│   ├── anto_conexionCAMBIOS.py      # ⚠️ Conexión alternativa (servidor PC-2193 / DB Aportes)
│   ├── acceso.py                    # ✅ Verificación de permisos vía Perfil_usuario_new
│   ├── acceso_denegado_dialog.py    # ✅ Diálogo de acceso denegado (GIF animado + datos de perfil)
│   ├── centrar_ventana.py           # ✅ Centra cualquier QWidget en la pantalla principal
│   ├── nuevo_regimen_modulo.py      # ⚠️ Módulo legacy (conexión a DB Aportes)
│   ├── resources.py                 # ✅ Resuelve rutas de assets (compatible con PyInstaller)
│   └── style.py                     # ✅ Hoja de estilo QSS parametrizable (tema oscuro)
│
├── Source/                          # Assets estáticos (incluidos completos en el build)
│   ├── icon.ico                     # Ícono del ejecutable
│   ├── userprofile4.png             # Ícono de la ventana principal y título del diálogo
│   ├── giphy.gif                    # GIF animado — diálogo de acceso denegado
│   ├── down-arrow_15775882.png      # Flecha del QDateEdit
│   └── up-down-arrow_15776044.png   # Flecha alternativa
│
├── old_version/
│   └── gestion_proveedoresui_V1.py  # Versión 1 archivada
│
└── README.md
```

---

## 🔐 Control de Acceso

Al iniciar la aplicación se ejecuta automáticamente `EXEC dbo.Perfil_usuario_new` (sin parámetros — usa `suser_sname()` internamente). El SP devuelve el perfil del usuario de sesión de Windows.

**Condición de acceso:** columna `area == 720002`
- ✅ **Permitido** → se abre la aplicación normalmente.
- ❌ **Denegado** → se muestra `AccesoDenegadoDialog` con GIF animado, datos del perfil del usuario, y la app se cierra al presionar Cerrar.

### Columnas relevantes del SP

| Columna | Descripción |
|---|---|
| `area` | `720002` si tiene asignación activa al área + impresión habilitada, `0` si no |
| `descripcion` | Nombre completo del usuario |
| `username` | Login `dominio\usuario` |
| `imprime` | `1` si tiene permiso de impresión |
| `estado` | `1` si el perfil está activo |

### Testing de permisos

```bash
python test_perfil_usuario.py
```

Muestra todas las columnas devueltas por el SP y el resultado (`PERMITIDO` / `DENEGADO`) para el usuario de sesión actual.

### Forzar denegación para pruebas de UI

En `anto_modulos/acceso.py`, descomentar:
```python
# FORZAR_DENEGADO = True
```

---

## ⚙️ Configuración de Base de Datos

La conexión está definida en `anto_modulos/anto_conexion.py`:

```python
server   = 'SQL01'      # ← Nombre del servidor SQL Server
database = 'Gestion'    # ← Nombre de la base de datos
# Autenticación: Windows integrada (Trusted_Connection=yes)
```

**Drivers ODBC intentados en orden de prioridad:**
1. `SQL Server Native Client 11.0`
2. `SQL Server Native Client 10.0`
3. `SQL Server` (legacy)

> Para cambiar el servidor o la base de datos, editar únicamente `anto_conexion.py`.

---

## 🗄️ Objetos SQL Server Utilizados

| Función Python | Tipo SQL | Objeto |
|---|---|---|
| `verificar_acceso()` | Stored Procedure | `dbo.Perfil_usuario_new` |
| `ejecutar_procedimiento_almacenado(cuil)` | Query | `SELECT COUNT(1) FROM Proveedores WHERE CUIL = ?` |
| `obtener_datos_por_cuil(cuil)` | Query | `SELECT … FROM Proveedores WHERE CUIL = ?` |
| `insertar_nuevo_registro(…)` | Stored Procedure | `AntoInsert_Proveedores_By_CUIL` |
| `actualizar_registro(…)` | Stored Procedure | `dbo.AntoUpdate_Proveedores` |

### Columnas de la tabla `Proveedores`

| Columna SQL | Campo en formulario | Tipo |
|---|---|---|
| `CUIL` | CUIL (solo lectura en edición) | `VARCHAR(11)` |
| `RAZON_SOCIAL` | Razón Social | `VARCHAR` |
| `PROVINCIA` | Provincia | `VARCHAR` (ComboBox) |
| `LOCALIDAD` | Localidad | `VARCHAR` |
| `CALLE` | Calle | `VARCHAR` |
| `CALLE_NRO` | Número | `VARCHAR` (solo dígitos) |
| `DPTO` | Departamento | `VARCHAR` |
| `PISO` | Piso | `VARCHAR` (solo dígitos) |
| `EMAIL` | Email | `VARCHAR` |
| `CONDICION_CTA` | Condición CTA | `VARCHAR` (ComboBox) |
| `CONDICION_EN_AFIP` | Condición AFIP | `VARCHAR` (ComboBox) |
| `CONDICION_DGR` | Condición DGR | `VARCHAR` (ComboBox) |
| `CONDICION_GCIA` | Condición GCIA | `VARCHAR` (ComboBox) |
| `CONDICION_EMPLEADOR` | Condición Empleador | `VARCHAR` (ComboBox) |
| `FORMA_JURIDICA` | Forma Jurídica | `VARCHAR` (ComboBox) |
| `FECHA_ULT_LIB_DEUDA` | Fecha Libre Deuda *(opcional)* | `DATE` / `NULL` |

---

## 📋 Opciones de ComboBoxes

| Campo | Opciones |
|---|---|
| **Condición CTA** | Activo, Baja |
| **Condición AFIP** | Monotributista, No Informado, Condición B, Exento, Responsable Inscripto, Responsable No Inscripto, Código Invalido, Null |
| **Condición DGR** | Inscripto, No Inscripto, No Informado, Exento, No Sujeto a Retención, Convenio Multilateral, Condición C, Null |
| **Condición GCIA** | Inscripto, No Inscripto, No Informado, Exento, Monotributista, No Sujeto a Retención, Convenio Multilateral, Condición D, Código Inválido, Null |
| **Condición Empleador** | Empleador, No Empleador, No Informado |
| **Forma Jurídica** | Persona Jurídica, Colectiva, Responsabilidad Limitada, Sociedad Anónima, Mutual, Asociación, No Informado, Asociación Civil, Cooperativa, En Formación, Empresa del Estado, Sociedad de Derecho, No Empleador, Organismo Público, Agrupación de Colaboración Empresaria, Fundación, Unipersonal, Otros |

---

## 📦 Instalación

### 1. Prerrequisitos

- Python 3.10 o superior instalado.
- Driver ODBC para SQL Server instalado en el equipo ([descargar](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)).
- Acceso de red al servidor `SQL01` con permisos de Windows sobre la base `Gestion`.

### 2. Clonar y configurar entorno

```bash
git clone https://github.com/WolfWilson/proveedores.git
cd proveedores

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Ejecutar

```bash
python main.py
```

---

## 🚀 Flujo de Uso

```
Inicio
  │
  ▼
verificar_acceso()  →  EXEC dbo.Perfil_usuario_new
  │
  ├── area == 720002 → ✅ Continúa
  └── area != 720002 → ❌ AccesoDenegadoDialog → cierra app
                            (GIF animado + datos de perfil)
  │
  ▼
┌─────────────────────────────────────┐
│          CUILSearchApp              │
│  [Input CUIL 11 dígitos]            │
│  [Buscar]                           │
│                                     │
│  Si EXISTE → habilita [Editar]      │
│  Si NO existe → habilita [Nuevo]    │
└───────────────┬─────────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   [Nuevo]           [Editar]
   Formulario vacío  Formulario precargado
   insertar_nuevo_   actualizar_
   registro()        registro()
```

---

## 🏗️ Guía de Modificaciones

### Cambiar servidor o base de datos

Editar `anto_modulos/anto_conexion.py`:
```python
server   = 'MI_SERVIDOR'
database = 'MI_BASE'
```

### Cambiar el área requerida para acceso

Editar `anto_modulos/acceso.py`:
```python
AREA_REQUERIDA = 720002   # cambiar por el código de área deseado
```

### Agregar un nuevo campo al formulario

1. **`anto_modulos/anto_conexion.py`** — agregar la columna al `SELECT` en `obtener_datos_por_cuil()` y al payload en `insertar_nuevo_registro()` / `actualizar_registro()`.
2. **`main.py – VentanaNuevo.__init__()`** — añadir el widget y su fila en el `QFormLayout`.
3. **`main.py – VentanaNuevo.cargar_datos()`** — mapear la nueva clave del diccionario al widget.
4. **`main.py – VentanaNuevo._validar_formulario()`** — agregar validación si es obligatorio.
5. **`main.py – VentanaNuevo.guardar_nuevo_registro()`** — leer el valor del widget y pasarlo a las funciones de capa de datos.
6. **SP SQL Server** — actualizar `AntoInsert_Proveedores_By_CUIL` y `AntoUpdate_Proveedores`.

### Cambiar el tema visual

En `anto_modulos/style.py`, la función `build_style()` acepta parámetros para colores, radios y tipografía. El objeto `STYLE` exportado se aplica en `main.py` con `app.setStyleSheet(STYLE)`.

### Reemplazar el GIF del diálogo de acceso denegado

Reemplazar `Source/giphy.gif` con el deseado (mantener el mismo nombre) o actualizar la constante en `anto_modulos/resources.py`:
```python
GIF_DENEGADO = resource_path("Source", "mi_animacion.gif")
```

---

## 📦 Empaquetar con PyInstaller

Ejecutar el script incluido:

```bat
build.bat
```

Genera el ejecutable en `dist\main\main.exe`.

La carpeta `Source/` completa (íconos, GIF, imágenes) se incluye automáticamente via `--add-data "Source;Source"`.

**Opciones usadas:**

```
--onedir --noconsole --optimize 2
--icon "Source/icon.ico"
--add-data "Source;Source"
--add-data "anto_modulos;anto_modulos"
```

---

## ⚠️ Archivos No Activos

| Archivo | Estado | Notas |
|---|---|---|
| `pyv2.py` | Versión anterior de la UI | Precursor de `main.py`, sin uso activo |
| `anto_modulos/anto_conexionCAMBIOS.py` | No importado | Conecta a servidor `PC-2193` / DB `Aportes` |
| `anto_modulos/nuevo_regimen_modulo.py` | No importado | Módulo legacy para DB `Aportes` |
| `old_version/gestion_proveedoresui_V1.py` | Archivado | Primera versión del proyecto |

---

## 🤝 Contribuir

1. Haz un **fork** del repositorio.
2. Crea una rama para tu cambio:
   ```bash
   git checkout -b feature/mi-cambio
   ```
3. Realiza los cambios y haz commit:
   ```bash
   git commit -m "feat: descripción del cambio"
   ```
4. Sube la rama y abre un **Pull Request**.

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

*Desarrollado para optimizar y modernizar la gestión de proveedores.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-41CD52?logo=qt&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2014+-red?logo=microsoft-sql-server&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-orange)

## 📌 Descripción

**Gestión de Proveedores** es una aplicación de escritorio desarrollada en **Python** con **PyQt5**, diseñada para administrar el padrón de proveedores de una organización. Permite buscar, registrar y editar proveedores por CUIL con conexión directa a una base de datos **SQL Server** usando autenticación Windows integrada.

---

## ✨ Características

- 🔍 **Búsqueda por CUIL** (11 dígitos) con validación en tiempo real.
- ➕ **Alta de nuevos proveedores** mediante formulario completo.
- ✏️ **Edición de registros existentes** con precarga automática de datos.
- 📋 **Validación de datos** antes de insertar o actualizar (CUIL, email, campos obligatorios).
- 🎨 **Interfaz oscura moderna** con estilos QSS parametrizables.
- 🏗️ **Compatible con PyInstaller** para distribuir como `.exe` standalone.
- 🖥️ **Centrado automático** de ventanas en pantalla.

---

## 🛠️ Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Lenguaje principal |
| [PyQt5](https://riverbankcomputing.com/software/pyqt/) | 5.15+ | Interfaz gráfica |
| [pyodbc](https://github.com/mkleehammer/pyodbc) | - | Conexión a SQL Server |
| [Microsoft SQL Server](https://www.microsoft.com/sql-server) | 2014+ | Base de datos |
| [PyInstaller](https://pyinstaller.org/) | - | Empaquetado a `.exe` |

**Módulos estándar usados:** `sys`, `re`, `datetime`, `typing`, `os`

---

## 📂 Estructura del Proyecto

```
proveedores/
├── main.py                        # ✅ Punto de entrada — UI principal (VentanaNuevo + CUILSearchApp)
├── pyv2.py                        # ⚠️ Versión anterior de la UI (no activo)
├── main.spec                      # Configuración de PyInstaller
│
├── anto_modulos/
│   ├── __init__.py
│   ├── anto_conexion.py           # ✅ Conexión SQL Server + CRUD (funciones activas)
│   ├── anto_conexionCAMBIOS.py    # ⚠️ Conexión alternativa (servidor PC-2193 / DB Aportes)
│   ├── centrar_ventana.py         # ✅ Centra cualquier QWidget en la pantalla principal
│   ├── nuevo_regimen_modulo.py    # ⚠️ Módulo legacy (conexión a DB Aportes)
│   ├── resources.py               # ✅ Resuelve rutas de assets (compatible con PyInstaller)
│   └── style.py                   # ✅ Hoja de estilo QSS parametrizable (tema oscuro)
│
├── Source/                        # Assets estáticos
│   ├── icon.ico                   # Ícono del ejecutable
│   ├── userprofile4.png           # Ícono de la ventana principal
│   ├── down-arrow_15775882.png    # Flecha del QDateEdit
│   └── up-down-arrow_15776044.png # Flecha alternativa
│
├── old_version/
│   └── gestion_proveedoresui_V1.py  # Versión 1 archivada
│
└── README.md
```

---

## ⚙️ Configuración de Base de Datos

La conexión está definida en `anto_modulos/anto_conexion.py`:

```python
server   = 'SQL01'      # ← Nombre del servidor SQL Server
database = 'Gestion'    # ← Nombre de la base de datos
# Autenticación: Windows integrada (Trusted_Connection=yes)
```

**Drivers ODBC intentados en orden de prioridad:**
1. `SQL Server Native Client 11.0`
2. `SQL Server Native Client 10.0`
3. `SQL Server` (legacy)

> Para cambiar el servidor o la base de datos, editar únicamente `anto_conexion.py`.  
> Si se migra a autenticación por usuario/contraseña, reemplazar `Trusted_Connection=yes` por `UID=...;PWD=...`.

---

## 🗄️ Objetos SQL Server Utilizados

| Función Python | Tipo SQL | Objeto |
|---|---|---|
| `ejecutar_procedimiento_almacenado(cuil)` | Query | `SELECT COUNT(1) FROM Proveedores WHERE CUIL = ?` |
| `obtener_datos_por_cuil(cuil)` | Query | `SELECT … FROM Proveedores WHERE CUIL = ?` |
| `insertar_nuevo_registro(…)` | Stored Procedure | `AntoInsert_Proveedores_By_CUIL` |
| `actualizar_registro(…)` | Stored Procedure | `dbo.AntoUpdate_Proveedores` |

### Columnas de la tabla `Proveedores`

| Columna SQL | Campo en formulario | Tipo |
|---|---|---|
| `CUIL` | CUIL (solo lectura en edición) | `VARCHAR(11)` |
| `RAZON_SOCIAL` | Razón Social | `VARCHAR` |
| `PROVINCIA` | Provincia | `VARCHAR` (ComboBox) |
| `LOCALIDAD` | Localidad | `VARCHAR` |
| `CALLE` | Calle | `VARCHAR` |
| `CALLE_NRO` | Número | `VARCHAR` (solo dígitos) |
| `DPTO` | Departamento | `VARCHAR` |
| `PISO` | Piso | `VARCHAR` (solo dígitos) |
| `EMAIL` | Email | `VARCHAR` |
| `CONDICION_CTA` | Condición CTA | `VARCHAR` (ComboBox) |
| `CONDICION_EN_AFIP` | Condición AFIP | `VARCHAR` (ComboBox) |
| `CONDICION_DGR` | Condición DGR | `VARCHAR` (ComboBox) |
| `CONDICION_GCIA` | Condición GCIA | `VARCHAR` (ComboBox) |
| `CONDICION_EMPLEADOR` | Condición Empleador | `VARCHAR` (ComboBox) |
| `FORMA_JURIDICA` | Forma Jurídica | `VARCHAR` (ComboBox) |
| `FECHA_ULT_LIB_DEUDA` | Fecha Libre Deuda | `DATE` |

---

## 📋 Opciones de ComboBoxes

| Campo | Opciones |
|---|---|
| **Condición CTA** | Activo, Baja |
| **Condición AFIP** | Monotributista, No Informado, Condición B, Exento, Responsable Inscripto, Responsable No Inscripto, Código Invalido, Null |
| **Condición DGR** | Inscripto, No Inscripto, No Informado, Exento, No Sujeto a Retención, Convenio Multilateral, Condición C, Null |
| **Condición GCIA** | Inscripto, No Inscripto, No Informado, Exento, Monotributista, No Sujeto a Retención, Convenio Multilateral, Condición D, Código Inválido, Null |
| **Condición Empleador** | Empleador, No Empleador, No Informado |
| **Forma Jurídica** | Persona Jurídica, Colectiva, Responsabilidad Limitada, Sociedad Anónima, Mutual, Asociación, No Informado, Asociación Civil, Cooperativa, En Formación, Empresa del Estado, Sociedad de Derecho, No Empleador, Organismo Público, Agrupación de Colaboración Empresaria, Fundación, Unipersonal, Otros |

---

## 📦 Instalación

### 1. Prerrequisitos

- Python 3.10 o superior instalado.
- Driver ODBC para SQL Server instalado en el equipo ([descargar](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)).
- Acceso de red al servidor `SQL01` con permisos de Windows sobre la base `Gestion`.

### 2. Clonar y configurar entorno

```bash
git clone https://github.com/WolfWilson/proveedores.git
cd proveedores

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Ejecutar

```bash
python main.py
```

---

## 🚀 Flujo de Uso

```
┌─────────────────────────────────────┐
│          CUILSearchApp              │
│  [Input CUIL 11 dígitos]            │
│  [Buscar]                           │
│                                     │
│  Si EXISTE → habilita [Editar]      │
│  Si NO existe → habilita [Nuevo]    │
└───────────────┬─────────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   [Nuevo]           [Editar]
   VentanaNuevo()    VentanaNuevo(datos=…)
   insertar_nuevo_   actualizar_
   registro()        registro()
```

1. Ingresar el CUIL (11 dígitos) y presionar **Buscar**.
2. Si el CUIL **existe**: se habilita **Editar** — abre formulario precargado.
3. Si el CUIL **no existe**: se habilita **Nuevo** — abre formulario vacío con el CUIL fijado.
4. Completar/modificar los campos y presionar **OK** para guardar.

---

## 🏗️ Guía de Modificaciones

### Cambiar servidor o base de datos

Editar `anto_modulos/anto_conexion.py`:
```python
server   = 'MI_SERVIDOR'   # nombre o IP
database = 'MI_BASE'
```

### Agregar un nuevo campo al formulario

1. **`anto_modulos/anto_conexion.py`** — agregar la columna al `SELECT` en `obtener_datos_por_cuil()` y al payload en `insertar_nuevo_registro()` / `actualizar_registro()`.
2. **`main.py – VentanaNuevo.__init__()`** — añadir el widget (`QLineEdit`, `QComboBox`, etc.) y su fila en el `QFormLayout`.
3. **`main.py – VentanaNuevo.cargar_datos()`** — mapear la nueva clave del diccionario al widget.
4. **`main.py – VentanaNuevo._validar_formulario()`** — agregar validación si es obligatorio.
5. **`main.py – VentanaNuevo.guardar_nuevo_registro()`** — leer el valor del widget y pasarlo a las funciones de capa de datos.
6. **SP SQL Server** — actualizar `AntoInsert_Proveedores_By_CUIL` y `AntoUpdate_Proveedores` para aceptar el nuevo parámetro.

### Agregar una opción a un ComboBox

En `main.py`, buscar el `QComboBox` correspondiente y añadir el ítem en `addItems([…])`.  
Si el valor viene de la BD, asegurarse de que exista también en el SP.

### Cambiar el tema visual

En `anto_modulos/style.py`, la función `build_style()` acepta parámetros para colores, radios y tipografía. El objeto `STYLE` exportado se aplica en `main.py` con `app.setStyleSheet(STYLE)`.

### Agregar validaciones de campo

Agregar lógica en `VentanaNuevo._validar_formulario()` en `main.py`. El método retorna un `str` con el mensaje de error o `None` si todo es válido.

### Cambiar íconos o imágenes

Reemplazar archivos en la carpeta `Source/` y actualizar las constantes en `anto_modulos/resources.py`:
```python
ICON_MAIN       = resource_path("Source", "mi_icono.png")
DATE_ARROW_DOWN = resource_path("Source", "mi_flecha.png")
```

---

## 📦 Empaquetar con PyInstaller

```bash
pyinstaller --onefile --noconsole \
  --icon "Source/icon.ico" \
  --add-data "Source;Source" \
  --add-data "anto_modulos;anto_modulos" \
  main.py
```

El ejecutable generado queda en `dist/main.exe`. La función `resource_path()` en `resources.py` resuelve rutas correctamente tanto en desarrollo como dentro del `.exe`.

---

## ⚠️ Archivos No Activos

| Archivo | Estado | Notas |
|---|---|---|
| `pyv2.py` | Versión anterior de la UI | Precursor de `main.py`, sin uso activo |
| `anto_modulos/anto_conexionCAMBIOS.py` | No importado | Conecta a servidor `PC-2193` / DB `Aportes` |
| `anto_modulos/nuevo_regimen_modulo.py` | No importado | Módulo legacy para DB `Aportes` |
| `old_version/gestion_proveedoresui_V1.py` | Archivado | Primera versión del proyecto |

---

## 🤝 Contribuir

1. Haz un **fork** del repositorio.
2. Crea una rama para tu cambio:
   ```bash
   git checkout -b feature/mi-cambio
   ```
3. Realiza los cambios y haz commit:
   ```bash
   git commit -m "feat: descripción del cambio"
   ```
4. Sube la rama y abre un **Pull Request**.

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

*Desarrollado para optimizar y modernizar la gestión de proveedores.*
