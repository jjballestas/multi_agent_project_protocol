# Gestión de secretos en desarrollo

## Objetivo
Definir cómo se gestionan los secretos en entornos de desarrollo dentro del Desarrollo_DotNet.

## Principio base
Los secretos nunca deben almacenarse en el repositorio.

## Estrategia actual (fase inicial)

### Uso de archivo `.env`
- cada desarrollador crea su propio archivo `.env`
- este archivo se genera a partir de `.env.example`
- `.env` está excluido del repositorio mediante `.gitignore`

### Flujo de trabajo
1. copiar `.env.example` a `.env`
2. definir valores locales de desarrollo
3. nunca subir `.env` al repositorio

## Tipos de datos en `.env`
- credenciales de base de datos de desarrollo
- cadenas de conexión locales

> Las configuraciones no sensibles van en `appsettings.Development.json`, que también está excluido del repositorio por `.gitignore`.

## Restricciones
- no incluir secretos reales de producción
- no reutilizar credenciales de otros entornos
- no compartir `.env` entre desarrolladores

## Evolución futura

En entornos empresariales, se recomienda integrar:

- Azure Key Vault
- variables seguras en Azure DevOps
- servicios de gestión de secretos corporativos

## Consideración importante
El uso de `.env` es una solución de desarrollo local. No es el mecanismo final de gestión de secretos en entornos productivos.