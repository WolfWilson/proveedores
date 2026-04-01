# anto_modulos/acceso.py
# Control de acceso al módulo Proveedores.
#
# Usa dbo.Perfil_usuario_new (sin parámetros — toma suser_sname() internamente).
# Columna "area": 720002 → el usuario cumple ambas condiciones (grupo + área activa).
#
# Para probar la ventana de acceso denegado con tu usuario,
# descomentá la línea FORZAR_DENEGADO = True más abajo.

from __future__ import annotations
import getpass

from anto_modulos.anto_conexion import obtener_conexion

# ─── Configuración ────────────────────────────────────────────────────────────
AREA_REQUERIDA = 720002   # valor numérico esperado en columna "area"

# ─── Override de prueba ───────────────────────────────────────────────────────
# Descomentá para forzar acceso DENEGADO independientemente del usuario real:
# FORZAR_DENEGADO = True
FORZAR_DENEGADO = False
# ─────────────────────────────────────────────────────────────────────────────


def verificar_acceso() -> tuple[bool, str, dict]:
    """
    Llama a dbo.Perfil_usuario_new y verifica si la columna "area" == 720002.

    Retorna:
        (tiene_acceso: bool, usuario: str, perfil: dict)
        perfil contiene los datos devueltos por el SP (vacío si no hay registro).
    """
    usuario = getpass.getuser()

    if FORZAR_DENEGADO:
        print(f"[acceso] FORZAR_DENEGADO activo — acceso denegado para {usuario}")
        return False, usuario, {}

    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("EXEC dbo.Perfil_usuario_new")
        row = cursor.fetchone()
        cols = [col[0] for col in cursor.description] if cursor.description else []
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[acceso] Error al ejecutar Perfil_usuario_new: {e}")
        return False, usuario, {}

    if row is None:
        print(f"[acceso] Sin registro de perfil para {usuario} → DENEGADO")
        return False, usuario, {}

    perfil = dict(zip(cols, row))
    area_valor = perfil.get("area", 0)

    acceso = (area_valor == AREA_REQUERIDA)
    print(f"[acceso] Usuario : {usuario}")
    print(f"[acceso] Perfil  : {perfil}")
    print(f"[acceso] area    : {area_valor}  →  {'PERMITIDO' if acceso else 'DENEGADO'}")
    return acceso, usuario, perfil
