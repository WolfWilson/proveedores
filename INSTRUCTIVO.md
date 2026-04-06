# 📋 Instructivo de Uso — Gestión de Proveedores

---

## ¿Qué problema resuelve este programa?

Cuando un sector necesita dar de alta o actualizar un proveedor en el sistema, el proceso tradicional implicaba intermediarios, formularios en papel, o acceso directo a la base de datos sin controles.

**Gestión de Proveedores** centraliza y agiliza esa tarea:

- El operador autorizado busca el CUIL del proveedor directamente desde su puesto.
- Si el proveedor **ya existe**, puede consultar y corregir sus datos al instante.
- Si el proveedor **no existe**, puede darlo de alta completando el formulario sin depender de otro sector.
- Todos los cambios quedan registrados en la base de datos institucional **en tiempo real**.

El acceso está restringido al personal habilitado del área correspondiente, garantizando que solo operadores autorizados puedan realizar modificaciones.

---

## ¿Quién puede usar el programa?

Solo el personal con **asignación activa al área 720002 – Mesa de Entradas/Salidas** y con permiso de impresión habilitado en el sistema.

Si al abrir el programa aparece una pantalla de **Acceso denegado**, significa que su usuario de Windows no tiene los permisos necesarios. En ese caso, contactar al área de sistemas para gestionar el acceso.

---

## Pantalla principal

Al iniciar el programa verá esta estructura:

```
┌──────────────────────────────────────┐
│  🔍  Ingrese el CUIL del proveedor   │
│  [_______________]  [Buscar]         │
│                                      │
│  [Nuevo]   [Editar]                  │
│ ─────────────────────────────────────│
│  Formulario de datos del proveedor   │
│  (se activa luego de buscar)         │
└──────────────────────────────────────┘
```

---

## Paso a paso

### 1. Buscar un CUIL

1. Escriba el **CUIL** del proveedor en el campo de búsqueda (11 dígitos, sin guiones ni espacios).
2. Presione el botón **Buscar** o la tecla **Enter**.

El sistema consultará la base de datos y mostrará uno de dos resultados:

| Resultado | Qué significa | Botón habilitado |
|---|---|---|
| ✅ CUIL encontrado | El proveedor ya está registrado | **Editar** |
| ❌ CUIL no encontrado | El proveedor no existe en el sistema | **Nuevo** |

---

### 2. Dar de alta un proveedor nuevo

> Disponible solo si la búsqueda devuelve **CUIL no encontrado**.

1. Presione el botón **Nuevo**.
2. El formulario se habilitará con el CUIL ya completado (no se puede modificar).
3. Complete **todos los campos obligatorios**:
   - Razón Social
   - Provincia
   - Localidad
   - Condición CTA
   - Condición en AFIP
   - Condición DGR
   - Condición GCIA
   - Condición Empleador
   - Forma Jurídica
4. Complete los campos opcionales según corresponda:
   - Calle, Número, Piso, Departamento
   - Email (debe tener formato válido: `nombre@dominio.com`)
   - Fecha Última Libre de Deuda *(ver nota abajo)*
5. Presione **OK** para guardar.

Si falta algún campo obligatorio, el sistema mostrará un mensaje indicando cuál completar antes de continuar.

---

### 3. Editar un proveedor existente

> Disponible solo si la búsqueda devuelve **CUIL encontrado**.

1. Presione el botón **Editar**.
2. El formulario se habilitará con todos los datos actuales del proveedor ya cargados.
3. Modifique únicamente los campos que necesite actualizar.
   - El campo **CUIL no se puede modificar**.
4. Presione **OK** para guardar los cambios.

---

### 4. Cancelar una operación

En cualquier momento, antes de presionar **OK**, puede presionar **Cancelar** para descartar los cambios y volver al estado de búsqueda.

---

## El campo "Fecha Última Libre de Deuda"

Este campo es **opcional**. Tiene dos comportamientos:

| Situación | Qué hacer |
|---|---|
| El proveedor tiene certificado de libre deuda | Ingresar la fecha usando el selector de fechas |
| El proveedor **no** tiene certificado | Marcar el tilde **"Sin fecha"** |

> ⚠️ Al marcar "Sin fecha" en modo edición, el campo queda **en blanco** pero no borra el valor anterior de la base de datos hasta que presione **OK** y confirme el guardado.

---

## Campos del formulario

| Campo | Obligatorio | Formato |
|---|---|---|
| CUIL | ✅ Sí | 11 dígitos (autocompletado desde la búsqueda) |
| Razón Social | ✅ Sí | Texto libre |
| Provincia | ✅ Sí | Seleccionar de la lista |
| Localidad | ✅ Sí | Texto libre |
| Calle | No | Texto libre |
| Número | No | Solo dígitos |
| Piso | No | Solo dígitos |
| Departamento | No | Texto libre |
| Email | No | Formato `usuario@dominio.com` |
| Condición CTA | ✅ Sí | Seleccionar: Activo / Baja |
| Condición en AFIP | ✅ Sí | Seleccionar de la lista |
| Condición DGR | ✅ Sí | Seleccionar de la lista |
| Condición GCIA | ✅ Sí | Seleccionar de la lista |
| Condición Empleador | ✅ Sí | Seleccionar de la lista |
| Forma Jurídica | ✅ Sí | Seleccionar de la lista |
| Fecha Libre Deuda | No | Fecha o marcar "Sin fecha" |

---

## Mensajes frecuentes

| Mensaje | Causa | Solución |
|---|---|---|
| *"El CUIL debe tener exactamente 11 dígitos"* | El CUIL ingresado tiene más o menos caracteres | Verifique el número e intente nuevamente |
| *"Complete el campo: Razón Social"* (u otro) | Falta un campo obligatorio | Completar el campo indicado |
| *"El email no tiene un formato válido"* | El email ingresado no es correcto | Corregir el formato (ej: `proveedor@empresa.com`) |
| *"Acceso denegado"* al iniciar | Su usuario no tiene permisos suficientes | Contactar a sistemas |
| *"No se pudo conectar al servidor"* | Problema de red o servidor no disponible | Verificar conexión de red y contactar a sistemas |

---

## Preguntas frecuentes

**¿Puedo editar el CUIL de un proveedor?**
No. El CUIL es el identificador único del proveedor y no puede modificarse una vez registrado.

**¿Qué pasa si cargo mal un dato y ya presioné OK?**
Puede volver a buscar el CUIL y presionar **Editar** para corregir el dato.

**¿El sistema guarda un historial de cambios?**
Los cambios se aplican directamente sobre el registro. El historial de modificaciones depende de la configuración de auditoría de la base de datos institucional.

**¿Puedo usar el programa desde cualquier equipo de la red?**
Sí, siempre que el equipo tenga acceso de red al servidor `SQL01` y el driver ODBC de SQL Server instalado.

---

## Soporte

Para problemas técnicos, errores inesperados o solicitudes de acceso, contactar al área de **Sistemas / Informática**.

---

*Programa desarrollado para agilizar la gestión del padrón de proveedores desde el sector habilitado.*
