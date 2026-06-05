# Uso de IA en el Desarrollo_DotNet

> Ver también: [gestion-secretos-desarrollo.md](./gestion-secretos-desarrollo.md)

## Rol de la IA
La IA (Claude Code) actúa como:

- asistente de desarrollo
- apoyo en arquitectura
- generador de código supervisado
- analista técnico

## Principios de uso

### 1. Supervisión humana obligatoria
Ningún código generado por IA debe pasar a producción sin revisión.

### 2. No acceso a información sensible
Nunca compartir con la IA:

- credenciales reales
- secretos
- tokens
- datos de clientes
- configuraciones productivas

### 3. Uso permitido
Se puede usar IA para:

- generar código base
- refactorizar
- explicar errores
- proponer arquitecturas
- documentar

### 4. Trazabilidad
Todo cambio generado con IA debe:

- versionarse en Git
- pasar por pull request
- validarse en pipeline

### 5. Contexto controlado
Solo se debe compartir con la IA:

- fragmentos de código necesarios
- logs controlados
- ejemplos anonimizados

## Buenas prácticas

- usar IA para acelerar, no para decidir sola
- validar siempre el output
- no copiar código sin entenderlo
- mantener control del diseño
  
## Objetivo final

La IA debe aumentar la productividad sin comprometer:

- seguridad
- calidad
- control técnico

---

## Restricciones de red del entorno IA

El entorno de desarrollo no debe asumir acceso libre a internet.

### Accesos permitidos
- Azure DevOps
- endpoints del proveedor IA
- feeds oficiales de paquetes
- repositorios internos autorizados

### Accesos no permitidos
- navegación libre sin control
- descarga arbitraria de herramientas
- conexiones a servicios externos no aprobados
- acceso a entornos de producción

### Regla operativa
La conectividad del contenedor debe considerarse controlada y limitada según políticas del proyecto o de la organización.