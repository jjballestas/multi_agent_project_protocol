# Onboarding — Desarrollo_DotNet

## Objetivo

Guiar a un desarrollador nuevo para que levante el entorno completo y empiece a trabajar en una aplicación desde cero.

---

## Prerrequisitos

Instalar en el equipo host (Windows) antes de comenzar:

| Herramienta | Versión mínima | Dónde obtenerla |
|---|---|---|
| Docker Desktop | 4.x | https://www.docker.com/products/docker-desktop |
| VS Code | Última estable | https://code.visualstudio.com |
| Extensión Dev Containers | Última | VS Code → Extensions → `ms-vscode-remote.remote-containers` |
| Git | 2.x | https://git-scm.com |

**Verificar que Docker Desktop esté corriendo** antes de continuar. Si el ícono de Docker en la barra de tareas muestra un punto verde, está listo.

---

## Paso 1 — Clonar el proyecto maestro

```bash
git clone https://dev.azure.com/[organización]/[proyecto]/_git/Desarrollo_DotNet
cd Desarrollo_DotNet
```

---

## Paso 2 — Levantar el SQL Server compartido

El SQL Server es un servicio compartido para todas las aplicaciones. Se levanta una sola vez y queda activo.

```bash
cd templates/docker-sqlserver

# Crear el archivo de credenciales
cp .env.example .env

# Editar .env y cambiar la contraseña por una segura (mínimo 12 caracteres)
# ACCEPT_EULA=Y
# SA_PASSWORD=<CAMBIAR_POR_PASSWORD_LOCAL_SEGURA>
# MSSQL_PID=Developer

# Levantar el contenedor
docker compose up -d

# Verificar que esté corriendo
docker ps | grep sqlserver-dev
```

Para confirmar la conexión: conectarse con Azure Data Studio o SQL Server Management Studio a `localhost,1433` con usuario `sa` y la contraseña del `.env`.

---

## Paso 3 — Crear una nueva aplicación

Cada aplicación vive en su propio repositorio. Desde cero:

```bash
# Ir al directorio donde vivirán las aplicaciones
cd C:\ING\Ingenas

# Crear el repositorio de la nueva app en Azure DevOps
# (desde el portal o con Azure DevOps CLI)

# Clonar el repositorio vacío
git clone https://dev.azure.com/[organización]/[proyecto]/_git/AppNombre
cd AppNombre
```

Copiar las plantillas del proyecto maestro:

```bash
# Copiar la plantilla de Dev Container
xcopy /E /I C:\ING\Ingenas\Desarrollo_DotNet\templates\devcontainer-dotnet\.devcontainer .devcontainer

# Copiar la plantilla de pipeline
copy C:\ING\Ingenas\Desarrollo_DotNet\templates\azure-pipelines\azure-pipelines-dotnet.yml azure-pipelines.yml
```

Crear la estructura base:

```bash
mkdir src tests docker
dotnet new webapi -o src/AppNombre.Api
dotnet new xunit -o tests/AppNombre.Tests
dotnet new sln -n AppNombre
dotnet sln add src/AppNombre.Api tests/AppNombre.Tests
```

---

## Paso 4 — Abrir la aplicación en Dev Container

1. Abrir VS Code en la carpeta de la nueva aplicación: `File → Open Folder`
2. VS Code detectará la carpeta `.devcontainer` y mostrará el aviso: **"Reopen in Container"** — hacer clic en ese botón.
3. Esperar a que el contenedor se construya (primera vez puede tardar 2-3 minutos).
4. Verificar el entorno dentro del contenedor:

```bash
dotnet --info      # debe mostrar .NET 8
git --version      # debe mostrar git instalado
```

---

## Paso 5 — Crear la base de datos de la aplicación

Desde el terminal dentro del Dev Container o desde el host:

```bash
sqlcmd -S localhost,1433 -U sa -P <contraseña> -Q "CREATE DATABASE AppNombre_Dev"
```

Verificar que el nombre siga la convención: `[NombreApp]_Dev`.

---

## Paso 6 — Primer commit

```bash
git checkout -b develop
git add .
git commit -m "feat: estructura inicial del proyecto AppNombre"
git push origin develop
```

---

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| VS Code no muestra "Reopen in Container" | Extensión Dev Containers no instalada | Instalar `ms-vscode-remote.remote-containers` |
| Docker no arranca el contenedor | Docker Desktop no está corriendo | Iniciar Docker Desktop desde el menú Inicio |
| No conecta al SQL Server | Contenedor SQL Server no levantado | Ejecutar `docker compose up -d` en `templates/docker-sqlserver` |
| Error de contraseña en SQL Server | `.env` no editado con contraseña válida | Editar `.env`, luego `docker compose down` y `docker compose up -d` |
| `dotnet --info` no responde | Imagen del Dev Container no construida | Ejecutar `Dev Containers: Rebuild Container` desde la paleta de VS Code |

---

## Referencias

- [Guía Metodológica](./Guia_Metodologica.md) — arquitectura y decisiones del entorno
- [Estrategia de branching](./docs/gobierno/estrategia-branching.md) — cómo trabajar con Git
- [Gobernanza SQL Server](./docs/gobierno/sql-server-gobernanza.md) — reglas de bases de datos
- [Seguridad de red](./docs/seguridad/seguridad-red-contenedores.md) — política de conectividad
