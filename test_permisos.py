#!/usr/bin/env python
# coding: utf-8
# test_permisos.py — Prueba de control de acceso al módulo Proveedores
#
# Condición 1: usuario pertenece al grupo NT "Gestion"  → dbo.Tiene_permiso
# Condición 2: usuario tiene asignación activa al área 720002 → dbo.TieneNomen
#
# Ambos SPs usan suser_sname() / IS_MEMBER() internamente;
# la sesión Trusted_Connection determina el usuario automáticamente.
#
# Uso: python test_permisos.py

import getpass
from anto_modulos.anto_conexion import obtener_conexion

GRUPO_REQUERIDO = "Gestion"   # Ajustar si requiere prefijo: "DOMINIO\\Gestion"
AREA_REQUERIDA  = "720002"    # Código de área Mesa de Entradas/Salidas


# ── Condición 1: grupo NT ──────────────────────────────────────────────────

def verificar_grupo(grupo: str) -> bool | None:
    """
    EXEC dbo.Tiene_permiso @GrupoNT = ?
    Retorna True / False / None (grupo inexistente o error).
    """
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("EXEC dbo.Tiene_permiso @GrupoNT = ?", (grupo,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row is None:
            return None
        valor = row[0]  # columna "puede"
        return None if valor is None else bool(valor)
    except Exception as e:
        print(f"  [ERROR] verificar_grupo: {e}")
        return None


# ── Condición 2: área asignada vía TieneNomen ─────────────────────────────

def verificar_area(cod_area: str) -> tuple[bool | None, list[dict]]:
    """
    EXEC dbo.TieneNomen  (sin parámetros — usa suser_sname() internamente)
    Retorna (tiene_area, todas_las_areas) donde:
        tiene_area → True si cod_area está entre las asignaciones activas
        todas_las_areas → lista de todas las áreas activas del usuario
    """
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("EXEC dbo.TieneNomen")
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        cursor.close()
        conn.close()

        areas = [dict(zip(cols, row)) for row in rows]
        tiene = any(str(a.get("cod_nomen", "")).strip() == cod_area for a in areas)
        return tiene, areas
    except Exception as e:
        print(f"  [ERROR] verificar_area: {e}")
        return None, []


# ── Resultado final ────────────────────────────────────────────────────────

def tiene_acceso() -> bool:
    """Devuelve True solo si el usuario cumple TODAS las condiciones."""
    cond1 = verificar_grupo(GRUPO_REQUERIDO)
    cond2, _ = verificar_area(AREA_REQUERIDA)
    return bool(cond1) and bool(cond2)


# ── Main (diagnóstico detallado) ───────────────────────────────────────────

def main():
    usuario_windows = getpass.getuser()
    print("=" * 60)
    print(f"  Usuario Windows en sesión : {usuario_windows}")
    print("=" * 60)

    # Condición 1
    c1 = verificar_grupo(GRUPO_REQUERIDO)
    if c1 is True:
        estado1 = "✅  ES miembro"
    elif c1 is False:
        estado1 = "❌  NO es miembro"
    else:
        estado1 = "⚠️  Grupo no encontrado o error"
    print(f"  [C1] Grupo '{GRUPO_REQUERIDO}'  →  {estado1}")

    # Condición 2
    c2, areas = verificar_area(AREA_REQUERIDA)
    if c2 is True:
        estado2 = f"✅  Área {AREA_REQUERIDA} asignada y activa"
    elif c2 is False:
        estado2 = f"❌  Área {AREA_REQUERIDA} NO encontrada"
    else:
        estado2 = "⚠️  Error al consultar áreas"
    print(f"  [C2] Área requerida        →  {estado2}")

    if areas:
        print(f"\n  Áreas activas del usuario ({len(areas)}):")
        for a in areas:
            print(f"    {str(a.get('cod_nomen','')):>10}  {a.get('DescNom','')}")

    print("=" * 60)
    acceso = bool(c1) and bool(c2)
    print(f"  ACCESO AL MÓDULO           →  {'✅  PERMITIDO' if acceso else '🚫  DENEGADO'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
