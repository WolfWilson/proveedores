# anto_conexion.py


import pyodbc
from datetime import datetime

drivers = [
        'ODBC Driver 17 for SQL Server',  # Preferido y más reciente
        'SQL Server Native Client 11.0',  # Native Client version 11
        'SQL Server Native Client 10.0',  # Native Client version 10
        'SQL Server',  # Generic ODBC driver name (legacy)
    ]

def obtener_conexion():
    # Configura la conexión a la base de datos SQL Server.
    server = 'SQL01'
    database = 'Gestion'

    for driver in drivers:
        conexion_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )
        try:
            print(f"Intentando conectar con el driver: {driver}")
            conexion = pyodbc.connect(conexion_str)
            print(f"Conexión exitosa con el driver: {driver}")
            return conexion
        except pyodbc.Error as error:
            print(f"Error al intentar conectar con el driver: {driver}")
            print(error)
    
    raise Exception("No se pudo conectar a la base de datos con ninguno de los drivers disponibles.")




def actualizar_registro(cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email,
                        condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
                        condicion_empleador, forma_juridica, fecha_ult_lib_deuda):
    try:
        # Obtiene la conexión usando tu método
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Conversión de fecha
        fecha_ult_lib_deuda_dt = datetime.strptime(fecha_ult_lib_deuda, "%Y-%m-%d")
        
        # Llama al procedimiento almacenado
        cursor.execute("""
            EXEC dbo.AntoUpdate_Proveedores
                @RAZON_SOCIAL = ?, 
                @CUIL = ?, 
                @PROVINCIA = ?, 
                @LOCALIDAD = ?, 
                @CALLE = ?, 
                @CALLE_NRO = ?, 
                @DPTO = ?, 
                @PISO = ?, 
                @EMAIL = ?, 
                @CONDICION_CTA = ?, 
                @CONDICION_EN_AFIP = ?, 
                @CONDICION_DGR = ?, 
                @CONDICION_GCIA = ?, 
                @CONDICION_EMPLEADOR = ?, 
                @FORMA_JURIDICA = ?, 
                @FECHA_ULT_LIB_DEUDA = ?, 
                @DNI_DESDE_CUIT = NULL
        """, (
            razon_social, cuil, provincia, localidad, calle, calle_nro, dpto, piso, email,
            condicion_cta, condicion_afip, condicion_dgr, condicion_gcia,
            condicion_empleador, forma_juridica, fecha_ult_lib_deuda_dt
        ))
        
        # Guarda los cambios
        conn.commit()
        
        return True  # Devuelve True si la operación fue exitosa
    except pyodbc.Error as e:
        print("Error al ejecutar el procedimiento:", e)
        return False  # Devuelve False si hubo un error
    finally:
        cursor.close()
        conn.close()





# anto_conexion.py

def obtener_datos_por_cuil(cuil):
    conexion = obtener_conexion()
    if conexion is None:
        print("Error: No se pudo conectar a la base de datos.")
        return None

    try:
        cursor = conexion.cursor()
        query = """
        SELECT RAZON_SOCIAL, PROVINCIA, LOCALIDAD, CALLE, CALLE_NRO, DPTO, PISO, EMAIL,
               CONDICION_CTA, CONDICION_EN_AFIP, CONDICION_DGR, CONDICION_GCIA,
               CONDICION_EMPLEADOR, FORMA_JURIDICA, FECHA_ULT_LIB_DEUDA
        FROM Proveedores
        WHERE CUIL = ?
        """
        cursor.execute(query, (cuil,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if resultado:
            # Convertimos el resultado a un diccionario
            return {
                "razon_social": resultado[0],
                "provincia": resultado[1],
                "localidad": resultado[2],
                "calle": resultado[3],
                "calle_nro": resultado[4],
                "dpto": resultado[5],
                "piso": resultado[6],
                "email": resultado[7],
                "condicion_cta": resultado[8],
                "condicion_afip": resultado[9],
                "condicion_dgr": resultado[10],
                "condicion_gcia": resultado[11],
                "condicion_empleador": resultado[12],
                "forma_juridica": resultado[13],
                "fecha_ult_lib_deuda": resultado[14]
            }
        else:
            return None

    except pyodbc.Error as error:
        print(f"Error al obtener datos por CUIL: {error}")
        return None


def ejecutar_procedimiento_almacenado(cuil):
    conexion = obtener_conexion()
    if conexion is None:
        print("Error: No se pudo conectar a la base de datos.")
        return None

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(1) FROM Proveedores WHERE CUIL = ?", (cuil,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if resultado and resultado[0] > 0:
            return 1  # CUIL encontrado
        else:
            return 0  # CUIL no encontrado

    except pyodbc.Error as error:
        print(f"Error al insertar el registro: {error}")
        print(error.args)
        return False



def insertar_nuevo_registro(
    cuil, razon_social, provincia, localidad, calle, calle_nro, dpto, piso, email, 
    condicion_cta, condicion_afip, condicion_dgr, condicion_gcia, 
    condicion_empleador, forma_juridica, fecha_ult_lib_deuda, dni_desde_cuit):
    """
    Inserta un nuevo registro en la base de datos con los datos del proveedor.
    """

    # Validaciones previas
    if not cuil or len(cuil) != 11 or not cuil.isdigit():
        print(f"Error: El CUIL '{cuil}' no es válido. Debe tener 11 dígitos numéricos.")
        return False
    if not razon_social:
        print("Error: La Razón Social no puede estar vacía.")
        return False
    if not provincia:
        print("Error: La Provincia no puede estar vacía.")
        return False
    if not localidad:
        print("Error: La Localidad no puede estar vacía.")
        return False
    # Más validaciones según tus reglas de negocio...

    # Imprimir los valores a insertar para depuración
    print("Valores a insertar en la base de datos:")
    print(f"CUIL: {cuil}, Razón Social: {razon_social}, Provincia: {provincia}, Localidad: {localidad}")
    print(f"Calle: {calle}, Calle Nro: {calle_nro}, Dpto: {dpto}, Piso: {piso}, Email: {email}")
    print(f"Condición CTA: {condicion_cta}, Condición AFIP: {condicion_afip}, Condición DGR: {condicion_dgr}")
    print(f"Condición GCIA: {condicion_gcia}, Condición Empleador: {condicion_empleador}, Forma Jurídica: {forma_juridica}")
    print(f"Fecha Últ. Libre Deuda: {fecha_ult_lib_deuda}, DNI desde CUIT: {dni_desde_cuit}")

    query = """
    EXEC AntoInsert_Proveedores_By_CUIL
        @RAZON_SOCIAL = ?, 
        @CUIL = ?, 
        @PROVINCIA = ?, 
        @LOCALIDAD = ?, 
        @CALLE = ?, 
        @CALLE_NRO = ?, 
        @DPTO = ?, 
        @PISO = ?, 
        @EMAIL = ?, 
        @CONDICION_CTA = ?, 
        @CONDICION_EN_AFIP = ?, 
        @CONDICION_DGR = ?, 
        @CONDICION_GCIA = ?, 
        @CONDICION_EMPLEADOR = ?, 
        @FORMA_JURIDICA = ?, 
        @FECHA_ULT_LIB_DEUDA = ?, 
        @DNI_DESDE_CUIT = ?
    """

    conexion = obtener_conexion()
    if conexion is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False

    try:
        cursor = conexion.cursor()

        # Ejecutar la consulta de inserción
        print("Ejecutando el procedimiento almacenado...")
        cursor.execute(query, (razon_social, cuil, provincia, localidad, calle, calle_nro, dpto, piso, email,
                               condicion_cta, condicion_afip, condicion_dgr, condicion_gcia, 
                               condicion_empleador, forma_juridica, fecha_ult_lib_deuda, dni_desde_cuit))
        
        # Confirmar los cambios en la base de datos
        conexion.commit()

        # Confirmar si realmente se insertó la fila
        if cursor.rowcount > 0:
            print("Registro insertado correctamente.")
        else:
            print("No se insertaron registros. Verifica los datos proporcionados.")

        return True

    except pyodbc.Error as error:
        print("Error al insertar el registro:")
        print(f"Mensaje de error: {error}")
        print(f"Detalles del error: {error.args}")
        return False

    except Exception as general_error:
        print("Error inesperado al intentar insertar el registro:")
        print(f"Mensaje: {general_error}")
        return False

    finally:
        # Asegurarse de cerrar la conexión en caso de que haya quedado abierta
        if conexion:
            conexion.close()
            print("Conexión cerrada.")

