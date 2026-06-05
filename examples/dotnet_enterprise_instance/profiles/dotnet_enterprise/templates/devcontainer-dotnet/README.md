# Plantilla Dev Container .NET

## Objetivo
Proporcionar una plantilla base de entorno de desarrollo para aplicaciones .NET dentro del Desarrollo_DotNet.

## Qué incluye
- archivo `devcontainer.json`
- `Dockerfile` base con .NET 8
- extensiones recomendadas para VS Code
- configuración inicial del entorno de desarrollo

## Uso

### Opción estándar (recomendada en el framework)

Ejecutar desde el host (PowerShell):

```powershell
$env:SA_PASSWORD="<CAMBIAR_POR_PASSWORD_LOCAL_SEGURA>"
$env:DB_NAME="AppNombre_Dev"

.\scripts\db-init.ps1

```


---

## Validación del framework

Este mecanismo ha sido validado mediante:

- creación idempotente de base de datos
- ejecución desde Dev Container
- aplicación de migraciones EF Core
- conexión a SQL Server compartido

Garantizando:

- reproducibilidad
- simplicidad operativa
- compatibilidad con múltiples aplicaciones simultáneas

---

## Validación funcional realizada

La plantilla fue validada en una aplicación creada desde cero utilizando únicamente los artefactos del framework.

### Escenario validado

- creación de una aplicación Web API .NET 8 dentro del Dev Container
- instalación y uso de `sqlcmd`
- conexión a SQL Server compartido de desarrollo
- instalación de EF Core SQL Server y herramientas de diseño
- creación de `DbContext`
- generación de migración inicial
- ejecución de bootstrap de base de datos
- creación automática de la base `[NombreApp]_Dev`
- aplicación correcta de migraciones
- arranque de la aplicación y respuesta funcional contra la base creada

### Resultado

La plantilla Dev Container queda validada como base operativa para aplicaciones .NET 8 que necesiten:

- SQL Server compartido en desarrollo
- bootstrap reproducible de base de datos
- EF Core Migrations
- aislamiento por aplicación

### Observación

Esta validación confirma que el soporte de `sqlcmd` en la plantilla base no es opcional, sino parte del camino estándar del framework para aplicaciones con persistencia en SQL Server.

---

## Validación funcional realizada

El proceso de bootstrap de base de datos fue validado en una aplicación creada desde cero utilizando exclusivamente los artefactos del framework.

### Escenario validado

- creación de una aplicación Web API .NET 8 en Dev Container
- definición de `DbContext` con EF Core
- generación de migración inicial
- ejecución del script `db-init.sh`
- creación automática de la base `[NombreApp]_Dev` en SQL Server compartido
- ejecución de `dotnet ef database update`
- creación de tablas y estructura inicial
- verificación mediante ejecución de la aplicación

### Resultado

El script `db-init.sh` queda validado como mecanismo estándar para:

- inicialización de base de datos por aplicación
- ejecución de migraciones EF Core
- integración con SQL Server compartido en desarrollo

### Consideraciones

- el script depende de:
  - `sqlcmd` disponible en el Dev Container
  - variables de entorno `SA_PASSWORD` y `DB_NAME`
- no requiere Docker dentro del contenedor (alineado con la arquitectura del framework)
- evita dependencias del host, garantizando reproducibilidad

### Conclusión

El bootstrap de base de datos queda establecido como un **componente estándar reutilizable del framework**, listo para ser utilizado en nuevas aplicaciones sin modificaciones manuales.
