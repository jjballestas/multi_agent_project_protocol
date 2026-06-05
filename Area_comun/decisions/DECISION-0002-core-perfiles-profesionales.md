---
decision_id: DECISION-0002
title: Arquitectura en capas — core neutral, profiles profesionales, examples
status: accepted
date: 2026-06-05
deciders: [Claude (architect), operador humano]
supersedes: []
superseded_by: []
relates_to: [TASK-0005, TASK-0006, TASK-0007, DECISION-0001]
phase: P1
---

# DECISION-0002 — Core neutral + perfiles profesionales + ejemplos

## Contexto

El protocolo debe seguir siendo **reutilizable y neutral de dominio**, pero existe conocimiento
profesional valioso (por ejemplo el del repo `D:\Agentes\entorno_open_cloude`: .NET 8, SQL Server,
Azure DevOps, Dev Containers, Docker en desarrollo, ADRs, branching, gestión de secretos,
pipelines) que muchos equipos querrían reutilizar. Si ese conocimiento entra en los archivos
genéricos del núcleo, el protocolo deja de ser neutral y se vuelve específico de un stack.

Necesitamos un mecanismo para **incorporar buenas prácticas por stack/tipo de proyecto sin
contaminar el núcleo**.

## Decisión

El protocolo se organiza conceptualmente en **tres capas**:

```
┌─────────────────────────────────────────────────────────────┐
│ a) CORE neutral de dominio                                    │
│    AGENTS / Area_comun / protocol docs / *.template.* /       │
│    validador / lifecycle / claims / mailbox / handoffs        │
│    → SIN trading, .NET, SQL Server, Azure DevOps, Docker,     │
│      ni negocio concreto. Es lo que se publica y versiona.    │
├─────────────────────────────────────────────────────────────┤
│ b) PROFILES / extensiones por stack o tipo de proyecto        │
│    profiles/<nombre>/  (p.ej. profiles/dotnet_enterprise/)    │
│    → ADRs, branching, seguridad, pipelines, versionado de     │
│      plantillas, onboarding, Dev Containers, SQL Server,      │
│      Azure DevOps... TODO lo específico vive AQUÍ, opcional.  │
├─────────────────────────────────────────────────────────────┤
│ c) EXAMPLES / instancias aplicadas                            │
│    examples/  e instancias reales (p.ej. bot_spot_ai_*)       │
│    → demuestran core, o core + uno/varios perfiles.           │
└─────────────────────────────────────────────────────────────┘
```

### Reglas

1. **El core NO incluye** reglas específicas de trading, .NET, SQL Server, Azure DevOps, Docker
   ni de ningún negocio concreto. La neutralidad del núcleo es innegociable (AGENTS.md §4,
   CLAUDE.md regla 1).
2. **Lo específico de `D:\Agentes\entorno_open_cloude` entra como perfil profesional**, p.ej.
   `profiles/dotnet_enterprise/`. Ese perfil puede incorporar ADRs, estrategia de branching,
   seguridad, pipelines (Azure DevOps), versionado de plantillas, onboarding, Dev Containers,
   SQL Server y Docker en desarrollo.
3. **Composición:** cada proyecto puede instanciar **solo el core**, o **core + uno o varios
   perfiles**. Los perfiles son aditivos; no modifican el contrato del core.
4. **Un perfil puede añadir fronteras y políticas más estrictas**, pero **nunca relajar** ni
   reescribir las del core ni romper la neutralidad de los archivos del núcleo.
5. **Registro de adopción:** cada adopción de perfil queda registrada en la instancia, en
   `PROJECT_STATE.json` (campo `adopted_profiles`, máquina-legible) **o** en una decisión de la
   propia instancia. Recomendado: ambos (campo + decisión la primera vez).
6. **Versionado (coherente con DECISION-0001):** introducir el mecanismo de perfiles y publicar
   perfiles nuevos es un cambio **MINOR** (capacidad aditiva, compatible). Romper el contrato del
   core para acomodar un perfil sería MAJOR y está prohibido por la regla 1/4.
7. **Contrato de perfil:** cada perfil declara un `profile.manifest` con su id, versión,
   `requires_protocol_version` (rango SemVer del core que necesita), stack, artefactos que aporta
   y fronteras que añade (definido en TASK-0005).

## Consecuencias

- **Positivas:** el core permanece neutral y reutilizable; el conocimiento profesional se
  reutiliza sin acoplar el protocolo a un stack; los proyectos eligen su nivel de opinión
  (mínimo o con perfiles); trazabilidad de qué perfiles usa cada instancia.
- **Costo / seguimiento:**
  - TASK-0005 (Claude): define la estructura `profiles/`, el `profile.manifest` y la plantilla.
  - TASK-0006 (Codex): construye `profiles/dotnet_enterprise/` desde `entorno_open_cloude`.
  - TASK-0007 (Codex): añade `adopted_profiles` al estado y soporte en el validador (aditivo).
  - Riesgo a vigilar: fuga de dominio al core. La revisión de frontera la hace el arquitecto en
    cada handoff de perfil.

## Alternativas consideradas

- **Meter las prácticas .NET directamente en el core:** descartado; rompe la neutralidad de
  dominio, que es la razón de ser del protocolo.
- **Un repo separado por stack sin relación con el core:** descartado; pierde la composición
  (core + perfil) y la trazabilidad de compatibilidad por versión.
- **Forks por stack:** descartado; multiplica el mantenimiento y produce drift frente al core.
