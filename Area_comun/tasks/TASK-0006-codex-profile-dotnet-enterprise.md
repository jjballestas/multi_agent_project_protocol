---
id: TASK-0006
owner: Codex
status: done
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0005]
relates_to: [TASK-0007]
phase: P1
review: Aceptada por Claude (arquitecto). Revision de frontera OK - barrido de neutralidad sobre el core (AGENTS.template, protocol.config.template, Area_comun/protocol, scripts, README*) sin terminos de stack; lo .NET/SQL/Azure/Docker vive solo en profiles/dotnet_enterprise. Manifest conforme al contrato de TASK-0005. Higiene de secretos OK (solo placeholders y refs a $SA_PASSWORD; .env.example saneado). examples/dotnet_enterprise_instance valida en verde con adopted_profiles + decision de adopcion. Ver HANDOFF-TASK-0006-claude-to-codex-1. La forma de adopted_profiles se formaliza en el borrador DECISION-0003 (input de TASK-0007).
---

# TASK-0006 — Perfil profesional `dotnet_enterprise` (basado en entorno_open_cloude)

## objetivo
Crear el primer perfil profesional, `profiles/dotnet_enterprise/`, empaquetando las buenas
prácticas del repo `D:\Agentes\entorno_open_cloude` como **extensión opcional** del protocolo,
SIN introducir nada de esto en el core neutral.

## entradas
- TASK-0005 (estructura `profiles/`, `profile.manifest`, plantilla de perfil) — **bloqueante**.
- Repo de referencia `D:\Agentes\entorno_open_cloude`:
  - `Guia_Metodologica.md`, `ONBOARDING.md`, `docs/arquitectura/`, `docs/gobierno/`
    (branching, modelo de artefactos, versionado de plantillas, gobernanza SQL Server),
    `docs/seguridad/`, `docs/pipelines/`, `docs/decisiones/adr-001-*`.
  - `templates/` (devcontainer-dotnet, docker-sqlserver, azure-pipelines, db-bootstrap-dotnet).
  - `prompts/prompt-maestro-Desarrollo_DotNet.md`, `examples/`.

## archivos_relevantes
- crea: `profiles/dotnet_enterprise/` con:
  - `profile.manifest.json` (conforme al contrato de TASK-0005).
  - `README.md` (qué aporta, cuándo aplicarlo, cómo se instancia sobre el core).
  - artefactos del perfil: ADRs, estrategia de branching, seguridad, pipelines (Azure DevOps),
    versionado de plantillas, onboarding, Dev Containers, SQL Server. Reutilizar/adaptar desde
    `entorno_open_cloude` (no copiar secretos; `.env.example` solo como ejemplo).

## entregables
- Perfil `dotnet_enterprise` instalable sobre una instancia del core.
- Handoff a Claude para revisión de frontera (que nada del perfil se haya filtrado al core).

## definition_of_done
- [x] `profile.manifest.json` válido (declara `requires_protocol_version`, stack, artefactos,
      fronteras añadidas).
- [x] El core permanece neutral: el barrido de neutralidad sobre núcleo + `*.template.*` del core
      sigue limpio; lo específico (.NET, SQL Server, Azure DevOps, Docker) vive SOLO en el perfil.
- [x] Sin secretos; los `.env`/credenciales solo como `.example`.
- [x] Una instancia de prueba que adopte core + `dotnet_enterprise` valida en verde.
- [x] Handoff autocontenido a Claude.

## riesgos
- Tentación de "subir" reglas del perfil al core: prohibido (DECISION-0002).
- Arrastrar configuración sensible del repo origen: revisar y sanear.

## preguntas_abiertas
- Ninguna bloqueante una vez cerrada TASK-0005.

## notas_de_ejecucion
- 2026-06-05 Codex: creado `profiles/dotnet_enterprise/` desde `D:\Agentes\entorno_open_cloude`.
- 2026-06-05 Codex: saneados ejemplos de password y verificado que no hay placeholders sin resolver.
- 2026-06-05 Codex: creada instancia controlada `examples/dotnet_enterprise_instance/`.
- 2026-06-05 Codex: handoff creado en `Area_comun/handoffs/HANDOFF-TASK-0006-codex-to-claude-1.md`.
