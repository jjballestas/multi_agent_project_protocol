# Gobernanza del SQL Server compartido de desarrollo

## Objetivo

Definir las reglas operativas para el contenedor SQL Server compartido que sirve a múltiples aplicaciones en desarrollo, evitando colisiones, dependencias cruzadas y pérdidas de datos.

---

## Decisión de diseño

Un único contenedor del motor SQL Server sirve a todas las aplicaciones en desarrollo. Cada aplicación tiene su propia base de datos dentro de ese motor. Las aplicaciones no comparten esquemas salvo decisión explícita documentada.

---

## Naming convention

| Entorno | Patrón | Ejemplo |
|---|---|---|
| Desarrollo | `[NombreApp]_Dev` | `AppFacturacion_Dev` |
| QA | `[NombreApp]_QA` | `AppFacturacion_QA` |

El nombre de la app en la base de datos debe coincidir con el nombre del repositorio de la aplicación, en PascalCase sin guiones ni espacios.

---

## Creación de bases de datos

Cada aplicación es responsable de crear su propia base de datos. El SQL Server compartido no crea bases automáticamente.

### Script de inicialización mínimo

Cada aplicación debe incluir un script:

---

## Mecanismo estándar de inicialización de base de datos

A partir de la versión actual del framework, se define como obligatorio el uso del mecanismo de bootstrap por aplicación:

### Componentes

- `scripts/create-database.sql` → creación idempotente de la base
- `scripts/db-init.sh` o `db-init.ps1` → ejecución controlada
- EF Core Migrations → gestión del esquema

### Flujo estándar

1. ejecutar `db-init`
2. crear base si no existe
3. aplicar migraciones
4. dejar entorno listo

### Restricciones

- no usar `Database.Migrate()` automático en runtime
- no modificar esquema manualmente fuera de migraciones
- no compartir bases entre aplicaciones

### Objetivo

Garantizar:

- reproducibilidad del entorno
- consistencia entre desarrolladores
- trazabilidad de cambios de esquema
- compatibilidad con SQL Server compartido