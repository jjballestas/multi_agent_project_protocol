---
task_id: TASK-0168
title: "Runtime: extender task_status_capability (DECISION-0060) -- architect/orchestrator cierra sus triage/extraction-tasks propias; golden + neutralidad"
type: implementation
status: done
owner: Codex
phase: P2
priority: normal
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
linked_decisions: [DECISION-0060, DECISION-0032, DECISION-0022]
file: Area_comun/tasks/TASK-0168-codex-gate-triage-extraction-close.md
---

# TASK-0168 - Gate: architect cierra triage/extraction propias (DECISION-0060)

> Cambio de runtime del protocolo-core (NO producto). maker=Codex / checker=Arquitecto. Bajo #4 enforce ON.

## Alcance

- `runtime/submit_intent.py::task_status_capability`: la regla de DECISION-0032 cambia de
  `task_type == "analysis"` a `task_type in {"analysis", "triage", "extraction"}` (misma condicion
  `actor_owns_task and to_status in {"in_review","done","blocked"}` -> `{"orchestrator","architect"}`).
  Todo lo demas intacto; la regla generica de `implementer` sigue para los otros tipos.
- Golden/behavior-test (extender `examples/analysis_close_cases/` o caso nuevo determinista):
  - GC-a: architect cierra su PROPIA `type: triage` (y `type: extraction`) -> permitido con orchestrator.
  - GC-b: `type: triage` de OTRO owner -> sigue exigiendo implementer (no se relaja para terceros).
  - GC-c: `type: product` propia -> sigue exigiendo implementer (no se relaja por tipo).
  - GC-d: rutas existentes `in_review->done` (reviewer) y `qa_pending->done` (qa) sin cambios.

## DoD

- Cambio aditivo (solo relaja para {analysis,triage,extraction}+owner). validate con/sin secretos exit 0;
  drift 0; neutralidad+encoding 0; #4 byte-identica (NO toca protocol.config.json; protocol_version PINNED,
  DECISION-0047). Golden verde; sin regresion en el resto del modelo de capacidades.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker.
- REPRO objetivo: con el cambio, `submit_intent` task_status de una `type: triage` propia del architect a
  `done` PASA (sin error de capability); una triage de tercero o un `type: product` propio FALLAN igual que hoy.

## Notas

- Esta tarea es el habilitador para cerrar `TASK-EXTRACT-1F5C13A7B5` (triage del Arquitecto, hoy bloqueada).
  Tras mergear, el Arquitecto la cierra por la via lifecycle estandar.
- Versionado por epoca (DECISION-0047): el bump MINOR se reconcilia en CHANGELOG/manifest fuera del config.
