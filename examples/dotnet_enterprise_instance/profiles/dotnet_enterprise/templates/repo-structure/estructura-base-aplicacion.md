# Estructura base de una aplicación

## Objetivo

Definir una estructura estándar para aplicaciones desarrolladas dentro del Desarrollo_DotNet, asegurando reproducibilidad, aislamiento por aplicación, simplicidad mantenible y alineación con las plantillas oficiales del framework.

---

## Estructura recomendada

```text
/app-nombre
│
├── src/
├── tests/
├── .devcontainer/
├── docker/
├── scripts/
│   ├── create-database.sql
│   └── db-init.sh
├── docker-compose.yml
├── azure-pipelines.yml
└── README.md
```


## Descripción de cada directorio

- `src/` — código fuente de la aplicación (API, lógica de negocio, acceso a datos, configuración).
- `tests/` — proyectos de pruebas unitarias, integración y validación del sistema.
- `.devcontainer/` — definición del entorno de desarrollo aislado en VS Code (imagen .NET, extensiones, configuración).
- `docker/` — Dockerfile y elementos auxiliares del entorno local de desarrollo.
- `scripts/` — scripts operativos de la aplicación. Incluye la inicialización de base de datos y procesos reproducibles de entorno.
  - `create-database.sql` — crea la base de datos de la aplicación de forma idempotente.
  - `db-init.sh` — script de bootstrap que crea la base y aplica migraciones.
- `docker-compose.yml` — definición de servicios locales necesarios para desarrollo (sin incluir SQL Server, que es compartido).
- `azure-pipelines.yml` — pipeline propio de la aplicación, basado en la plantilla del framework.
- `README.md` — documentación de la aplicación (objetivo, setup, uso del entorno, inicialización de base de datos).

---

## Versionado de plantillas

Cada aplicación debe declarar explícitamente qué versión de plantillas utiliza.

Ejemplo:

```text
Plantillas base:
- DevContainer: v1.0.0
- Pipeline: v1.0.0
- DB Bootstrap: v1.0.0

---

## Configuración de base de datos (estándar)

Las aplicaciones NO deben incluir cadenas de conexión hardcodeadas en código fuente.

### Reglas

- la cadena de conexión debe definirse en `appsettings.json` o `appsettings.Development.json`
- los secretos (passwords) NO deben almacenarse en el repositorio
- en desarrollo se utilizará `host.docker.internal` para acceder al SQL Server compartido

### Ejemplo

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=host.docker.internal,1433;Database=NombreApp_Dev;User Id=sa;Password=${SA_PASSWORD};TrustServerCertificate=True"
  }
}