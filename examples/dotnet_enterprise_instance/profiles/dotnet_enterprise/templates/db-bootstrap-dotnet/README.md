# Plantilla Bootstrap de Base de Datos (.NET)

## Objetivo

Proporcionar un mecanismo estándar, reproducible y controlado para:

- crear la base de datos de la aplicación
- aplicar migraciones
- preparar el entorno de desarrollo

---

## Enfoque adoptado

Esta plantilla implementa la estrategia oficial del framework:

1. Script SQL idempotente → creación de base de datos
2. EF Core Migrations → gestión del esquema
3. Script `db-init` → ejecución controlada

---

## Archivos incluidos

- `db-init.sh` → script principal de inicialización

---

## Variables requeridas

El script depende de:

| Variable | Descripción |
|--------|------------|
| `SA_PASSWORD` | contraseña del usuario `sa` del SQL Server |
| `DB_NAME` | nombre de la base de datos (`AppNombre_Dev`) |

---

## Uso

Dentro del Dev Container:

```bash
export SA_PASSWORD=<CAMBIAR_POR_PASSWORD_LOCAL_SEGURA>
export DB_NAME=AppNombre_Dev

./scripts/db-init.sh

---

## Requisitos del entorno

Para que `db-init.sh` funcione correctamente, el Dev Container debe incluir:

- `sqlcmd` (mssql-tools18)
- acceso a `host.docker.internal`
- .NET SDK 8
- herramienta `dotnet-ef`

Estos requisitos están cubiertos por la plantilla oficial:
