# ADR-001 — Diseño base del Desarrollo_DotNet

## Estado
Aceptado

## Contexto
Se requiere un entorno de desarrollo asistido por IA que permita trabajar múltiples aplicaciones de forma simultánea, con aislamiento, seguridad y trazabilidad, orientado a proyectos empresariales y regulados.

## Decisión

Se adopta la siguiente arquitectura:

- VS Code como IDE principal
- Claude Code como asistente IA
- Git como sistema de control de versiones
- Azure DevOps como plataforma de colaboración y CI/CD
- Docker solo en desarrollo
- un Dev Container por aplicación
- SQL Server en un contenedor compartido en desarrollo
- una base de datos por aplicación
- producción en máquinas virtuales (sin Docker)

## Justificación

- permite aislamiento por aplicación
- evita conflictos de dependencias
- facilita reproducibilidad del entorno
- mantiene control sobre seguridad y acceso a datos
- permite integrar IA sin exponer infraestructura crítica

## Consecuencias

### Positivas
- desarrollo paralelo de múltiples aplicaciones
- entorno consistente entre desarrolladores
- mejor control del uso de IA
- base sólida para CI/CD

### Negativas
- necesidad de gestionar múltiples contenedores
- dependencia de Docker en desarrollo
- mantenimiento de plantillas base

## Decisiones relacionadas
- política de uso seguro de IA
- estrategia de pipeline desacoplado por aplicación
- SQL Server compartido en desarrollos