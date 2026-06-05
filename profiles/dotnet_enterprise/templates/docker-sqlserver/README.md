# SQL Server compartido de desarrollo

Este contenedor proporciona un motor SQL Server común para los entornos de desarrollo de múltiples aplicaciones.

## Objetivo
Permitir que varias aplicaciones se conecten al mismo motor SQL Server en desarrollo, manteniendo una base de datos separada por aplicación.

## Reglas
- una aplicación = una base de datos
- no compartir esquemas entre aplicaciones salvo decisión explícita
- usar scripts separados por proyecto
- evitar dependencias cruzadas entre bases

## Contenedor
- nombre: `sqlserver-dev`
- imagen: `mcr.microsoft.com/mssql/server:2022-latest`
- puerto expuesto: `1433`

## Primeros pasos
1. Copiar `.env.example` a `.env`
2. Editar `.env` con una contraseña segura para desarrollo
3. Verificar que `.env` no se suba al repositorio
4. Ejecutar `docker compose up -d`

## Credenciales de desarrollo
Se definen en el archivo `.env`.

## Ejemplo de conexión
- servidor: `localhost,1433`
- usuario: `sa`
- contraseña: la definida en `.env`

## Ejemplo de base de datos creada
`AppEjemplo_Dev`