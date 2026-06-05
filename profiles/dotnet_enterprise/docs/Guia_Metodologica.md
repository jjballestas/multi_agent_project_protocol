# Guía Metodológica — Desarrollo_DotNet

## 1. Objetivo del entorno

Diseñar un entorno de desarrollo asistido por IA que permita trabajar varias aplicaciones al mismo tiempo, cada una con su propio ecosistema técnico, sin conflictos de dependencias, manteniendo control, seguridad y trazabilidad para proyectos orientados a sectores bancario, gubernamental y empresarial.

La IA actúa como asistente de desarrollo supervisado, no como agente autónomo con control de infraestructura crítica.

---

## 2. Decisiones base del entorno

### 2.1. Plataforma de trabajo

| Componente | Decisión |
|---|---|
| IDE principal | VS Code |
| Asistente IA | Claude Code |
| Control de versiones | Git |
| Plataforma DevOps | Azure DevOps |
| Stack principal | .NET 8 LTS |
| Base de datos | SQL Server |

### 2.2. Política de contenedores

- **Desarrollo:** usa Docker
- **QA/UAT:** opcional, según necesidad del proyecto
- **Producción:** no usa Docker — despliegue en máquinas virtuales

### 2.3. Razón de usar Docker en desarrollo

Docker no es la estrategia de despliegue final. Se usa como mecanismo para:

- aislar cada proyecto
- evitar conflictos entre dependencias
- reproducir entornos de forma consistente
- permitir desarrollar varias aplicaciones en paralelo
- facilitar que la IA trabaje sobre entornos técnicos estables

---

## 3. Principios rectores

### 3.1. Aislamiento por aplicación

Cada aplicación tiene su propio entorno de desarrollo aislado:

```
App A → su contenedor, su SDK, sus tools, sus paquetes
App B → su contenedor, su SDK, sus tools, sus paquetes
```

Esto evita choques entre versiones de .NET, conflictos de librerías, instalaciones globales innecesarias y contaminación entre proyectos.

### 3.2. Reproducibilidad

Cualquier desarrollador debe poder levantar cualquier proyecto con la misma base técnica, sin dependencias del equipo host.

### 3.3. Seguridad

La IA no debe tener acceso libre a secretos, producción, datos reales ni componentes sensibles. Ver sección 9.

### 3.4. Supervisión humana

Toda propuesta generada por IA debe ser revisada, probada y aprobada por una persona antes de integrarse al repositorio principal.

### 3.5. Separación de entornos

Debe existir separación estricta entre desarrollo, pruebas y producción, tanto en acceso como en configuración y datos.

---

## 4. Arquitectura general del entorno

```
Desarrollador
   ↓
VS Code
   ↓
Dev Container por aplicación
   ├── Claude Code
   ├── SDK .NET 8
   ├── herramientas del proyecto
   ├── librerías y utilidades aisladas
   └── red controlada
   ↓
Azure DevOps
   ├── Azure Repos (Git)
   ├── Pull Requests
   ├── Pipelines
   └── Boards / trazabilidad
   ↓
Despliegue a máquinas virtuales
   ├── DEV
   ├── QA/UAT
   └── PROD
```

---

## 5. Arquitectura de desarrollo con Docker

### 5.1. Idea central

Cada aplicación tiene un workspace aislado basado en Docker. No se trata de contenerizar toda la organización, sino de que cada proyecto de desarrollo viva dentro de su propio entorno controlado.

### 5.2. Qué puede contener cada entorno Docker de desarrollo

Según necesidad del proyecto:

- contenedor principal de desarrollo
- contenedor de API .NET
- contenedor auxiliar de pruebas
- acceso al contenedor compartido de SQL Server
- mocks de integraciones externas
- herramientas internas del proyecto

### 5.3. Qué problema resuelve

Con varias aplicaciones activas al mismo tiempo, Docker permite que cada una use su propia versión de .NET, sus paquetes del sistema y sus herramientas, sin afectar el equipo host ni los demás proyectos.

---

## 6. Estructura base de una aplicación

Cada aplicación debe seguir esta estructura:

```
/app-nombre
   /src
   /tests
   /.devcontainer
   /docker
   docker-compose.yml
   azure-pipelines.yml
   README.md
```

### 6.1. Carpeta `.devcontainer`

Define el entorno de desarrollo para VS Code. Incluye imagen base, extensiones necesarias, variables de entorno no sensibles, herramientas del proyecto y configuración inicial del contenedor.

### 6.2. Carpeta `docker`

Puede contener el Dockerfile del entorno dev, archivos auxiliares, scripts de inicialización y configuración local.

### 6.3. `docker-compose.yml`

Levanta los componentes locales del proyecto: app, base de datos, mock server, cola simulada u otras herramientas auxiliares.

### 6.4. `azure-pipelines.yml`

Copiado y adaptado desde la plantilla del proyecto maestro. Cada aplicación gestiona su propio pipeline.

---

## 7. Cómo encajan VS Code, Docker y Claude Code

**VS Code** es el IDE principal desde donde se abre cada proyecto.

**Docker** proporciona el aislamiento del entorno por proyecto.

**Claude Code** trabaja dentro del contexto del proyecto abierto, sobre un entorno técnico ya controlado y reproducible. Así la IA no opera sobre la máquina host completa, sino sobre un entorno más predecible y limitado, lo que mejora consistencia, seguridad, reproducibilidad y calidad de ejecución de pruebas.

---

## 8. Azure DevOps y Git dentro del diseño

### 8.1. Plataforma adoptada

- **Git** como sistema de versionado
- **Azure DevOps** como ecosistema corporativo de colaboración y gobierno

### 8.2. Qué aporta Azure DevOps

- Azure Repos (repositorios privados)
- Pull Requests con políticas de revisión
- Pipelines de CI/CD
- Boards y trazabilidad de cambios
- Control de acceso por proyecto

---

## 9. Seguridad del entorno

### 9.1. Secretos

Los secretos nunca deben quedar en repositorios, en prompts ni en archivos de configuración accesibles al agente. Se deben usar archivos locales excluidos por `.gitignore`, variables protegidas del pipeline o un vault corporativo.

### 9.2. Datos

La IA trabaja con datos sintéticos, anonimizados o muestras controladas. Nunca con datos reales de clientes, expedientes sensibles, credenciales ni llaves privadas.

### 9.3. Control de cambios

Todo cambio sugerido por IA debe quedar en Git, pasar por pull request y validarse con pipeline antes de integrarse a la rama principal.

### 9.4. Modelo de red del entorno IA

El contenedor de desarrollo no debe asumir salida libre a internet. La política recomendada es salida controlada, con acceso únicamente a:

**Accesos permitidos:**
- Azure DevOps
- endpoints del proveedor IA
- feeds oficiales de paquetes (NuGet, etc.)
- repositorios internos autorizados

**Accesos no permitidos:**
- navegación abierta sin control
- descarga arbitraria de herramientas
- conexiones a servicios externos no aprobados
- acceso a entornos de producción

Docker aísla el entorno de ejecución, pero no define la seguridad de red. La conectividad debe controlarse con políticas de red de la máquina o de la organización.

---

## 10. Gestión de múltiples aplicaciones simultáneas

Cada aplicación tiene su propio repositorio, su contenedor de desarrollo, su configuración de VS Code, su pipeline y su base de datos en el SQL Server compartido. Esto permite cambiar de un proyecto a otro sin reinstalar dependencias, sin tocar el host y sin mezclar configuraciones entre proyectos.

---

## 11. SQL Server en desarrollo

### 11.1. Decisión adoptada

Se usa un único contenedor del motor SQL Server como servicio compartido de desarrollo. Múltiples aplicaciones se conectan a ese contenedor, cada una con su propia base de datos.

### 11.2. Reglas de gobierno del SQL Server compartido

- una aplicación = una base de datos
- naming convention fija: `[NombreApp]_Dev` en desarrollo, `[NombreApp]_QA` en QA
- scripts de base de datos separados por proyecto
- no compartir esquemas entre aplicaciones salvo decisión explícita documentada
- evitar dependencias cruzadas entre bases

**Ejemplos de naming:**
```
AppFacturacion_Dev
AppAuditoria_Dev
AppPortalClientes_Dev
```

### 11.3. En producción

SQL Server se despliega en la infraestructura real definida por la organización, no en Docker.

---

## 12. Rol de la IA dentro del entorno

### La IA debe ayudar en

- análisis de codebase
- migraciones y refactorizaciones
- documentación técnica
- generación de pruebas automatizadas
- scaffolding de nuevos proyectos
- troubleshooting y resolución de errores
- apoyo en decisiones de arquitectura

### La IA no debe

- desplegar a producción sin control humano
- manejar secretos ni credenciales reales
- operar infraestructura crítica de forma autónoma
- tomar decisiones sensibles sin revisión
- acceder libremente a sistemas no autorizados

---

## 13. Diseño técnico para aplicaciones .NET

### 13.1. Stack base

- .NET 8 LTS como versión estándar del entorno
- APIs REST
- arquitectura modular o Clean Architecture pragmática
- pruebas unitarias e integración
- logging estructurado
- configuración por entorno

### 13.2. Relación con Docker

Docker en desarrollo sirve para encapsular el entorno técnico de la aplicación, no para definir el modelo de operación en producción.

### 13.3. Beneficio para la IA

Con el entorno en contenedor, la IA puede ejecutar comandos de forma consistente, analizar el proyecto correctamente y repetir pruebas con resultados fiables, sin depender de la configuración del host.

---

## 14. Entornos del ciclo de vida

### 14.1. Desarrollo

Uso intensivo de Docker. Objetivo: programar, probar, depurar, usar IA y validar localmente.

### 14.2. QA/UAT

Puede ejecutarse en contenedores si conviene para pruebas, o desplegarse en máquinas virtuales según la necesidad del proyecto.

### 14.3. Producción

Sin Docker. Despliegue en máquinas virtuales controladas, con configuración estable, procesos formales de promoción y monitoreo corporativo.

---

## 15. CI/CD dentro del modelo

### 15.1. Flujo de trabajo

```
Desarrollo local en Dev Container
→ validación local
→ commit en rama
→ push a Azure Repos
→ Pull Request
→ pipeline automático
→ revisión humana
→ aprobación
→ despliegue a entorno correspondiente
```

### 15.2. Estrategia de pipeline

El pipeline no vive en el proyecto maestro. Cada aplicación real copia la plantilla base desde `templates/azure-pipelines/azure-pipelines-dotnet.yml`, la lleva a la raíz de su repositorio como `azure-pipelines.yml` y la adapta si necesita pasos adicionales.

### 15.3. Qué valida el pipeline

**Validaciones mínimas (plantilla base):**
- restaurar dependencias
- compilar en modo Release
- ejecutar tests

**Validaciones requeridas antes de uso en proyectos regulados:**
- análisis estático (`dotnet format --verify-no-changes`)
- escaneo de secretos (gitleaks u herramienta equivalente)
- publicación de artefacto para despliegue

---

## 16. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| Creer que Docker resuelve toda la seguridad | Complementar con control de red, credenciales, políticas de repo y revisiones humanas |
| Meter demasiados servicios en local | Contenerizar solo lo necesario para desarrollar y probar |
| La IA obtiene más acceso del debido | Contexto mínimo, red controlada, sin secretos, sin acceso a producción |
| Duplicación desordenada entre proyectos | Usar siempre las plantillas base del proyecto maestro |

---

## 17. Arquitectura por capas

| Capa | Componentes |
|---|---|
| Desarrollo | VS Code · Claude Code · Docker/Dev Containers · un entorno aislado por aplicación |
| Colaboración | Git · Azure DevOps · PRs · políticas de revisión |
| Aplicación | .NET 8 · arquitectura modular · pruebas automatizadas |
| Datos | SQL Server compartido en desarrollo · instancia corporativa en producción |
| Despliegue | Máquinas virtuales · sin Docker en producción |

---

## 18. Resumen ejecutivo

`Desarrollo_DotNet` es un ecosistema de desarrollo IA asistido basado en **VS Code + Claude Code + Docker en desarrollo + Git/Azure DevOps + .NET + SQL Server**, donde cada aplicación vive en su propio entorno aislado, reproducible y controlado, mientras la producción se mantiene en máquinas virtuales tradicionales.

Su finalidad es permitir desarrollar múltiples aplicaciones .NET en paralelo, con aislamiento de dependencias, reproducibilidad del entorno, control técnico y seguridad adecuada para sectores regulados.