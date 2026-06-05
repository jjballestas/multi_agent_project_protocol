# Estrategia de branching — Desarrollo_DotNet

## Decisión adoptada

Se adopta **GitFlow** como estrategia de branching para todos los proyectos del entorno.

---

## Estructura de ramas

| Rama | Tipo | Propósito |
|---|---|---|
| `main` | Permanente | Código en producción. Solo recibe merges desde `release/*` o `hotfix/*`. |
| `develop` | Permanente | Integración continua del trabajo en curso. Base para features y releases. |
| `feature/*` | Temporal | Desarrollo de una funcionalidad nueva. Sale de `develop`, vuelve a `develop`. |
| `release/*` | Temporal | Preparación de una versión para producción. Sale de `develop`, cierra en `main` y `develop`. |
| `hotfix/*` | Temporal | Corrección urgente en producción. Sale de `main`, cierra en `main` y `develop`. |

---

## Convenciones de naming

```
feature/nombre-descriptivo-en-kebab-case
release/1.2.0
hotfix/correccion-critica-login
```

El nombre debe describir el trabajo, no el ticket. Si el equipo usa Azure Boards, puede incluir el ID del work item como prefijo:

```
feature/1234-autenticacion-oauth
hotfix/5678-fix-timeout-conexion
```

---

## Flujo de trabajo

### Feature nueva

```
develop
  └─ feature/nueva-funcionalidad
       └─ (desarrollo y commits)
       └─ PR → develop (revisión humana + pipeline verde)
```

### Preparación de release

```
develop
  └─ release/1.2.0
       └─ (ajustes finales, bump de versión)
       └─ PR → main   (con tag v1.2.0)
       └─ PR → develop (para sincronizar)
```

### Hotfix urgente

```
main
  └─ hotfix/fix-critico
       └─ (corrección mínima)
       └─ PR → main   (con tag v1.1.1)
       └─ PR → develop (para no perder el fix)
```

---

## Reglas de protección de ramas

Aplicar en Azure DevOps (Repos → Branch policies) para `main` y `develop`:

- **Require a pull request** — nadie hace push directo.
- **Minimum reviewers: 1** — al menos una persona revisa.
- **Check for linked work items** — cada PR referencia un work item en Boards.
- **Build validation** — el pipeline debe estar en verde antes de aprobar el PR.
- **Delete source branch after merge** — mantiene el repositorio limpio.

---

## Política de commits

- Usar mensajes descriptivos en español o inglés de forma consistente por proyecto.
- Formato recomendado: `tipo: descripción breve`
- Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Ejemplos:
```
feat: agregar endpoint de consulta de saldo
fix: corregir timeout en conexión SQL Server
docs: actualizar README con instrucciones de Dev Container
```

---

## Relación con el pipeline

| Rama | Pipeline se activa | Qué hace |
|---|---|---|
| `feature/*` | En PR hacia `develop` | Restaurar, compilar, tests |
| `develop` | En merge | Restaurar, compilar, tests, análisis estático |
| `release/*` | En PR hacia `main` | Pipeline completo + escaneo de secretos + artefacto |
| `main` | En merge | Publicación de artefacto versionado |
| `hotfix/*` | En PR hacia `main` | Pipeline completo |

---

## ADR relacionado

Esta estrategia complementa ADR-001. No reemplaza las decisiones del diseño base sino que define el gobierno de ramas que ADR-001 dejaba sin especificar.
