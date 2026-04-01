"""
test_perfil_usuario.py
----------------------
Verifica el acceso del usuario actual ejecutando dbo.Perfil_usuario_new.

El SP no recibe parámetros: usa suser_sname() internamente.
Columna clave: "area"
  - 720002 → PERMITIDO  (cumple grupo + área activa + imprime)
  - 0      → DENEGADO
"""

import sys
import pyodbc

# ── Conexión ─────────────────────────────────────────────────────────────────
DRIVERS_PREFERIDOS = [
    "SQL Server Native Client 11.0",
    "SQL Server Native Client 10.0",
    "SQL Server",
]

SERVIDOR  = "SQL01"
BASE      = "Gestion"
AREA_REQ  = 720002


def obtener_driver() -> str:
    disponibles = [d for d in pyodbc.drivers() if any(p in d for p in DRIVERS_PREFERIDOS)]
    if not disponibles:
        raise RuntimeError("No se encontró ningún driver ODBC de SQL Server.")
    disponibles.sort(key=lambda d: next(i for i, p in enumerate(DRIVERS_PREFERIDOS) if p in d))
    return disponibles[0]


def main():
    print("=" * 60)
    print("  TEST: dbo.Perfil_usuario_new")
    print("=" * 60)

    try:
        driver = obtener_driver()
        print(f"Driver ODBC   : {driver}")
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={SERVIDOR};"
            f"DATABASE={BASE};"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str, timeout=10)
    except Exception as e:
        print(f"\n[ERROR] No se pudo conectar: {e}")
        sys.exit(1)

    try:
        cursor = conn.cursor()

        # Mostrar el usuario de sesión que ve SQL Server
        cursor.execute("SELECT suser_sname() AS usuario_sql")
        row = cursor.fetchone()
        print(f"suser_sname() : {row[0] if row else '(sin resultado)'}")
        print()

        # Ejecutar el SP
        cursor.execute("EXEC dbo.Perfil_usuario_new")
        cols = [col[0] for col in cursor.description]
        row  = cursor.fetchone()

        if row is None:
            print("[RESULTADO] Sin registro → DENEGADO")
            print("            El usuario no tiene perfil activo en la base.")
            sys.exit(0)

        perfil = dict(zip(cols, row))

        print("Columnas devueltas por el SP:")
        print("-" * 40)
        for col, val in perfil.items():
            print(f"  {col:<20}: {val}")
        print("-" * 40)

        area_valor = perfil.get("area", 0)
        acceso     = (area_valor == AREA_REQ)

        print()
        print(f"area           : {area_valor}")
        print(f"Área requerida : {AREA_REQ}")
        print()
        if acceso:
            print("✅  ACCESO PERMITIDO")
        else:
            print("❌  ACCESO DENEGADO")
            print(f"    'area' es {area_valor!r}, se esperaba {AREA_REQ}.")

    except Exception as e:
        print(f"\n[ERROR] al ejecutar Perfil_usuario_new: {e}")
    finally:
        cursor.close()
        conn.close()

    print("=" * 60)


if __name__ == "__main__":
    main()
