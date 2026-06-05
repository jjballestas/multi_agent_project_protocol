# Arquitectura general del Desarrollo_DotNet

## Objetivo
Definir la arquitectura base del entorno de desarrollo asistido por IA para proyectos bancarios, gubernamentales y empresariales.

## Propósito del proyecto
`Desarrollo_DotNet` no es una aplicación de negocio. Es un proyecto maestro que sirve como marco para crear, documentar y gobernar un entorno de desarrollo con IA usando Claude Code.

## Componentes principales

### IDE y asistente
- VS Code como entorno de desarrollo principal
- Claude Code como asistente IA de desarrollo

### Control de versiones y gobierno
- Git como sistema de versionado
- Azure DevOps como plataforma de colaboración, repositorios y pipeline

### Desarrollo aislado
- Docker solo en desarrollo
- un Dev Container por aplicación
- dependencias aisladas por proyecto

### Base de datos de desarrollo
- un contenedor compartido de SQL Server
- una base de datos por aplicación
- separación lógica entre proyectos

### Producción
- despliegue en máquinas virtuales
- sin Docker en producción

## Vista general

```text
Desarrollador
   ↓
VS Code
   ↓
Dev Container por aplicación
   ├── Claude Code
   ├── SDK .NET
   ├── herramientas del proyecto
   └── conexión al SQL Server compartido de desarrollo
   ↓
Azure DevOps
   ├── Azure Repos (Git)
   ├── Pull Requests
   ├── Pipelines
   └── Boards / trazabilidad
   ↓
Despliegue formal
   ├── DEV / QA si aplica
   └── PROD en máquinas virtuales