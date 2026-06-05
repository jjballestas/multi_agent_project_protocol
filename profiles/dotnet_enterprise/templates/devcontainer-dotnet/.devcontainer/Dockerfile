FROM mcr.microsoft.com/devcontainers/dotnet:1-8.0-bookworm

# Versión de imagen fija para garantizar reproducibilidad del entorno.
# Para actualizar: verificar la última imagen estable en
# https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/dotnet/tags
# y actualizar la etiqueta arriba con la nueva versión específica.
# Registrar el cambio en CHANGELOG o como commit con mensaje:
# "chore: actualizar imagen base Dev Container a X.Y"

# Limpiar repositorios problemáticos heredados y herramientas base
RUN rm -f /etc/apt/sources.list.d/yarn.list /usr/share/keyrings/yarnkey.gpg \
    && apt-get update \
    && apt-get install -y \
        curl \
        git \
        unzip \
        gpg \
    && rm -rf /var/lib/apt/lists/*

# Instalar sqlcmd (SQL Server tools) en Debian 12
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft-prod.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools18 unixodbc-dev \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin:/home/vscode/.dotnet/tools"' >> /etc/bash.bashrc