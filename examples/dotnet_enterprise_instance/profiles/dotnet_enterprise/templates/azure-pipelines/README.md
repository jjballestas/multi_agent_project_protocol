# Pipeline base Azure DevOps

## Objetivo
Proporcionar una plantilla base para validar automáticamente proyectos .NET dentro del flujo corporativo.

## Qué hace esta plantilla
- restaura dependencias
- compila en modo Release
- ejecuta tests
- usa .NET 8

## Archivo de plantilla
`azure-pipelines-dotnet.yml`

## Estrategia de uso
Esta plantilla no se ejecuta directamente desde este repositorio maestro.

Cada aplicación real debe:

1. copiar `azure-pipelines-dotnet.yml` a la raíz de su propio repositorio
2. renombrarlo a `azure-pipelines.yml`
3. adaptarlo si necesita pasos adicionales

## Motivo de esta estrategia
Se evita depender de rutas relativas que no existirán en repositorios de aplicaciones reales y se mantiene una plantilla simple, portable y reutilizable.