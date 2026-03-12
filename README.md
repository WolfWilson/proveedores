# 🏢 Gestión de Proveedores

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-41CD52?logo=qt&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2014-red?logo=microsoft-sql-server&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-orange)

## 📌 Descripción
**Gestión de Proveedores** es una aplicación de escritorio desarrollada en **Python** con **PyQt5**, diseñada para facilitar la administración y actualización de datos de proveedores.  
Permite consultar, agregar y editar información directamente desde una base de datos **SQL Server**, ofreciendo una interfaz intuitiva y profesional.

## ✨ Características
- 🔍 **Búsqueda por CUIL** con conexión directa a SQL Server.
- ✏️ **Alta, baja y modificación** de proveedores.
- 📋 **Validación automática** de datos antes de insertar o actualizar.
- 🖥 **Interfaz moderna y responsiva** con estilos personalizados.
- ⚡ **Optimizado** para entornos Windows 10+.

## 🛠 Tecnologías Utilizadas
- **Lenguaje**: [Python 3.10+](https://www.python.org/)
- **Interfaz gráfica**: [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)
- **Base de datos**: [Microsoft SQL Server 2014](https://www.microsoft.com/es-es/sql-server/sql-server-2014) — conexión vía `pyodbc` con autenticación Windows (`Trusted_Connection`)
- **Empaquetado**: [PyInstaller](https://pyinstaller.org/) — genera ejecutable `.exe` standalone
- **Control de versiones**: [Git](https://git-scm.com/)

## 📦 Dependencias Python

| Paquete | Uso |
|---|---|
| `PyQt5` | Interfaz gráfica (ventanas, widgets, estilos) |
| `pyodbc` | Conexión a SQL Server |

> Las dependencias de la librería estándar utilizadas son: `sys`, `re`, `datetime`, `typing`, `os`.

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/WolfWilson/proveedores.git
cd proveedores

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso
```bash
python main.py
```
1. Ingresa el **CUIL** del proveedor.
2. Consulta o edita la información existente.
3. Guarda los cambios en la base de datos.

## 📂 Estructura del Proyecto
```
proveedores/
├── anto_modulos/
│   ├── anto_conexion.py          # ✅ Conexión a SQL Server y funciones de acceso a datos
│   ├── centrar_ventana.py        # ✅ Utilidad para centrar la ventana en pantalla
│   ├── resources.py              # ✅ Rutas a recursos (iconos, imágenes) compatibles con PyInstaller
│   ├── style.py                  # ✅ Hoja de estilo global (PyQt5)
│   ├── anto_conexionCAMBIOS.py   # ⚠️ No utilizado (versión alternativa de conexión)
│   └── nuevo_regimen_modulo.py   # ⚠️ No utilizado (módulo legacy)
├── Source/                       # Recursos estáticos (iconos, imágenes)
├── old_version/                  # Versiones anteriores del proyecto
├── main.py                       # Archivo principal de la aplicación
├── pyv2.py                       # ⚠️ No utilizado (versión anterior de la UI)
├── main.spec                     # Configuración de PyInstaller
└── README.md                     # Este archivo
```

## 🗄️ Procedimientos Almacenados (SQL Server)

La aplicación interactúa con la base de datos `Gestion` en el servidor `SQL01` mediante los siguientes procedimientos y consultas:

| Función Python | Tipo | Objeto SQL |
|---|---|---|
| `insertar_nuevo_registro()` | Stored Procedure | `AntoInsert_Proveedores_By_CUIL` |
| `actualizar_registro()` | Stored Procedure | `dbo.AntoUpdate_Proveedores` |
| `obtener_datos_por_cuil()` | Query directa | `SELECT … FROM Proveedores WHERE CUIL = ?` |
| `ejecutar_procedimiento_almacenado()` | Query directa | `SELECT COUNT(1) FROM Proveedores WHERE CUIL = ?` |

**Drivers ODBC probados (en orden de prioridad):**
1. `SQL Server Native Client 11.0`
2. `SQL Server Native Client 10.0`
3. `SQL Server` (legacy)
## Pyinstaller
   ```bash
pyinstaller --onefile --noconsole --icon "Source/icon.ico" --add-data "Source;Source" --add-data "anto_modulos;anto_modulos" main.py
   ```

## 🤝 Contribuir
1. Haz un **fork** del repositorio.
2. Crea una rama para tu función o corrección:
   ```bash
   git checkout -b mi-nueva-funcion
   ```
3. Haz commit de tus cambios:
   ```bash
   git commit -m "Agrega mi nueva función"
   ```
4. Sube la rama a tu fork:
   ```bash
   git push origin mi-nueva-funcion
   ```
5. Abre un **Pull Request**.

## 📄 Licencia
Este proyecto está bajo la licencia [MIT](LICENSE).

---
💡 *Desarrollado para optimizar y modernizar la gestión de proveedores.*
