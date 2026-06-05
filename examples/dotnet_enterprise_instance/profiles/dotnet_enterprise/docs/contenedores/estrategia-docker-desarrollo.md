# Estrategia Docker en desarrollo

## Objetivo
Utilizar Docker como mecanismo de aislamiento y reproducibilidad en entornos de desarrollo, sin utilizarlo en producción.

## Principio base
Docker se usa exclusivamente en desarrollo.

## Modelo adoptado

### Aislamiento por aplicación
Cada aplicación se ejecuta en su propio Dev Container, lo que permite:

- evitar conflictos de dependencias
- trabajar múltiples proyectos simultáneamente
- mantener entornos consistentes

### SQL Server compartido
Se utiliza un contenedor único de SQL Server para desarrollo:

- múltiples aplicaciones se conectan a este contenedor
- cada aplicación tiene su propia base de datos
- no se comparten esquemas entre aplicaciones

### Flujo de trabajo
1. levantar SQL Server con docker compose
2. abrir aplicación en Dev Container
3. desarrollar y probar localmente
4. conectar a la base de datos correspondiente

## Beneficios
- reproducibilidad del entorno
- aislamiento técnico
- facilidad de onboarding
- menor dependencia del host

## Limitaciones
- requiere Docker Desktop
- consumo de recursos adicional
- gestión de contenedores múltiples

## Consideraciones de seguridad
- no incluir secretos en imágenes o repositorios
- usar archivos `.env` excluidos de Git
- limitar conectividad de red según política del proyecto