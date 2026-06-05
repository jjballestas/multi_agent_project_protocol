#!/bin/bash

set -euo pipefail

echo "===> Inicializando base de datos..."

if [ -z "${SA_PASSWORD:-}" ]; then
  echo "ERROR: SA_PASSWORD no está definido"
  exit 1
fi

if [ -z "${DB_NAME:-}" ]; then
  echo "ERROR: DB_NAME no está definido"
  exit 1
fi

if ! command -v sqlcmd >/dev/null 2>&1; then
  echo "ERROR: sqlcmd no está disponible en el entorno"
  exit 1
fi

if ! command -v dotnet >/dev/null 2>&1; then
  echo "ERROR: dotnet no está disponible en el entorno"
  exit 1
fi

if ! command -v dotnet-ef >/dev/null 2>&1 && ! dotnet ef --version >/dev/null 2>&1; then
  echo "ERROR: dotnet-ef no está disponible en el entorno"
  exit 1
fi

if [ ! -f "scripts/create-database.sql" ]; then
  echo "ERROR: no existe scripts/create-database.sql"
  exit 1
fi

echo "===> Verificando conectividad con SQL Server..."

sqlcmd -S host.docker.internal,1433 \
  -U sa \
  -P "$SA_PASSWORD" \
  -C \
  -Q "SELECT 1" >/dev/null

echo "===> Creando base de datos si no existe..."

sqlcmd -S host.docker.internal,1433 \
  -U sa \
  -P "$SA_PASSWORD" \
  -C \
  -i scripts/create-database.sql

echo "===> Aplicando migraciones..."

dotnet ef database update

echo "===> Base de datos lista"