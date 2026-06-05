# Seguridad de red en contenedores de desarrollo

## Objetivo

Definir cómo se controla la conectividad de red de los contenedores de desarrollo para evitar que la IA o el entorno accedan a recursos no autorizados.

## Principio base

El contenedor de desarrollo no tiene acceso libre a internet. La conectividad se limita a los destinos estrictamente necesarios para desarrollar.

---

## Modelo de red adoptado

### Red interna del proyecto

Cada proyecto define una red Docker propia en su `docker-compose.yml`. Los contenedores del proyecto se comunican por red interna sin exponer puertos innecesarios al host.

```yaml
networks:
  app-network:
    driver: bridge
```

### Accesos permitidos desde el contenedor

| Destino | Motivo |
|---|---|
| Azure DevOps (`dev.azure.com`) | Repositorios, pipelines, boards |
| `api.anthropic.com` | Claude Code como asistente IA |
| `api.nuget.org` | Paquetes NuGet oficiales |
| Registros internos autorizados | Paquetes y artefactos corporativos |

### Accesos no permitidos

- Navegación libre a internet
- Descarga de herramientas desde fuentes no aprobadas
- Conexión a servicios externos no listados
- Acceso a entornos productivos

---

## Implementación por niveles

### Nivel básico (recomendado para inicio)

Configurar el `docker-compose.yml` de cada aplicación para usar una red interna y limitar puertos expuestos al mínimo necesario:

```yaml
services:
  app-dev:
    build:
      context: .
      dockerfile: docker/Dockerfile
    networks:
      - app-network
    ports:
      - "5000:8080"     # solo el puerto de la aplicación

  sqlserver-dev:
    image: mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04
    networks:
      - app-network
    ports:
      - "127.0.0.1:1433:1433"    # solo localhost, no expuesto a red externa

networks:
  app-network:
    driver: bridge
```

Usar `127.0.0.1:1433` en lugar de `0.0.0.0:1433` impide que el SQL Server sea accesible desde otras máquinas en la misma red local.

### Nivel intermedio (proyectos regulados)

Añadir reglas de salida en el `daemon.json` de Docker Desktop para limitar las IPs o dominios accesibles. En Windows, esto se gestiona mediante reglas del Firewall de Windows aplicadas al proceso `com.docker.backend.exe`.

Pasos:
1. Identificar las IPs de los destinos permitidos (Azure DevOps, NuGet, proveedor IA).
2. Crear reglas de salida en el Firewall de Windows que permitan solo esos destinos.
3. Bloquear el resto del tráfico saliente del proceso Docker.
4. Documentar las reglas aplicadas en este directorio.

### Nivel avanzado (entornos corporativos)

En organizaciones con proxy corporativo, configurar el proxy en el `devcontainer.json`:

```json
{
  "remoteEnv": {
    "HTTP_PROXY": "http://proxy.corp.internal:8080",
    "HTTPS_PROXY": "http://proxy.corp.internal:8080",
    "NO_PROXY": "localhost,127.0.0.1,.corp.internal"
  }
}
```

El proxy corporativo puede entonces auditar y filtrar el tráfico del contenedor según políticas de la organización.

---

## Consideraciones de seguridad adicionales

- No exponer el puerto `1433` del SQL Server a `0.0.0.0` — solo a `127.0.0.1`.
- No mapear volúmenes con rutas sensibles del host al contenedor.
- No pasar variables de entorno de producción al contenedor de desarrollo.
- Revisar que el `.env` del contenedor no contenga credenciales de otros entornos.

---

## Limitación declarada

Docker no implementa por sí mismo el control de tráfico saliente. El aislamiento de red que Docker provee es de red interna entre contenedores, no de filtrado de salida a internet. La restricción real depende de:

- Firewall del sistema operativo host
- Proxy corporativo si existe
- Políticas de red de la organización

Este documento define la política. La implementación técnica exacta depende de la infraestructura de cada equipo.
