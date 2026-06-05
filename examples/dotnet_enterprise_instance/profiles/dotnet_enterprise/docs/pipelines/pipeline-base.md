# Pipeline base

## Implementación actual
El proyecto maestro mantiene una plantilla reutilizable de pipeline en:

- `templates/azure-pipelines/azure-pipelines-dotnet.yml`

## Alcance actual (plantilla base)
- restauración de dependencias
- compilación en Release
- ejecución de tests

## Requerido antes de uso en proyectos regulados
- análisis estático
- escaneo de secretos
- publicación de artefacto

## Estrategia adoptada
La plantilla del pipeline no se ejecuta directamente desde este repositorio maestro.

Cada aplicación real debe:

1. copiar `templates/azure-pipelines/azure-pipelines-dotnet.yml`
2. llevarlo a la raíz de su repositorio
3. renombrarlo como `azure-pipelines.yml`
4. adaptarlo si necesita más validaciones

## Justificación
Esta estrategia evita rutas rotas y dependencias innecesarias entre el proyecto maestro y los repositorios reales de aplicaciones.

## Siguiente evolución prevista
Más adelante se podrán añadir:

- validaciones por rama
- stages por entorno