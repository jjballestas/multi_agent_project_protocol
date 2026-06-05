---
id: TASK-0001
owner: Claude
status: done
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0002]
phase: P0
review: Done. ROADMAP-v0.2.0.md entregado; backlog priorizado (TASK-0003/0004).
---

# TASK-0001 — Roadmap y backlog de enriquecimiento del protocolo v0.2.0

## objetivo
Definir y priorizar el backlog de enriquecimiento del protocolo hacia **v0.2.0**, manteniendo
neutralidad de dominio. Produce el roadmap y puebla `TASK_INDEX.json`.

## entradas
- `AGENTS.md`, `Area_comun/protocol/*`, `examples/minimal_instance/`.
- Candidatos: validador Python multiplataforma (TASK-0002), CI, SemVer+CHANGELOG, script de
  scaffolding/instanciacion, mas ejemplos (p.ej. proyecto web/CLI), README principal del repo.

## archivos_relevantes
- crea: `Area_comun/artifacts/ROADMAP-v0.2.0.md`.
- edita: `Area_comun/state/TASK_INDEX.json` (poblar tareas priorizadas).

## entregables
- `Area_comun/artifacts/ROADMAP-v0.2.0.md` con objetivos de v0.2.0 y criterios de aceptacion.
- `TASK_INDEX.json` con backlog priorizado (cada tarea con su archivo creado y owner).

## definition_of_done
- [ ] Roadmap con objetivos v0.2.0, orden recomendado y criterios de aceptacion.
- [ ] Backlog priorizado en `TASK_INDEX.json` (cada entrada con `file` existente).
- [ ] Mantiene neutralidad de dominio (sin terminos de negocio en el nucleo).
- [ ] Handoff si genera trabajo para Codex.

## riesgos
- Sobre-ingenieria: priorizar primero lo de mayor valor (validador multiplataforma + CI).

## preguntas_abiertas
- Ninguna bloqueante.
