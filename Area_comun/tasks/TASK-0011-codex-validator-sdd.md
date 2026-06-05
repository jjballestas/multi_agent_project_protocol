---
id: TASK-0011
owner: Codex
status: proposed
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0008, TASK-0010]
relates_to: [TASK-0009, TASK-0012]
phase: P2
---

# TASK-0011 — Actualizar validadores para modo SDD

> Tipo `implementation` → **SDD obligatorio**. `proposed` hasta que TASK-0008 entregue `spec_id`.

## objetivo
Añadir, de forma **aditiva**, el modo SDD a `validate_collaboration_state.{py,ps1}` y el bloque
`sdd` a `protocol.config.template.json`, con paridad y golden cases.

## comportamiento esperado (de DECISION-0004 §9-§10)
- Sin `sdd.enabled` (o false): comportamiento idéntico al actual (no rompe históricas ni ejemplos).
- `sdd.enabled: true`, `enforcement: "new_implementable_tasks"`:
  - ERROR si tarea implementable nueva en ready/claimed/in_progress carece de algún campo SDD o el `spec_id` no existe.
  - WARNING si tarea discovery/analysis/review/documentation/triage no declara objective/expected_output/question_to_resolve/closure_criterion.
  - Exime tareas históricas/pre-SDD (sin migración retroactiva).

## SDD (pendiente de TASK-0008)
- `spec_id`: _pendiente_
- `execution_pipeline`: _pendiente_
- `acceptance_criteria`: paridad .py/.ps1; golden cases positivos y negativos; ejemplos actuales siguen verdes.
- `linked_decisions`: DECISION-0004, DECISION-0001, DECISION-0003 (patrón aditivo + paridad)
- `test_plan`: golden cases en `examples/profile_validation_cases/` o nuevos `examples/sdd_validation_cases/`; validar root + ejemplos.
- `closure_criteria`: _pendiente_

## riesgos
- Romper compatibilidad: los chequeos solo aplican con `sdd.enabled`. Mantener paridad .py/.ps1.
