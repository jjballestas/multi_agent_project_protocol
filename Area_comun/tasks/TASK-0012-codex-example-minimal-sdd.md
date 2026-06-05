---
id: TASK-0012
owner: Codex
status: proposed
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0010, TASK-0011]
relates_to: [TASK-0009]
phase: P2
---

# TASK-0012 — Crear example minimal_sdd_instance

> Tipo `implementation` → **SDD obligatorio**. `proposed` hasta que TASK-0008 entregue `spec_id`.

## objetivo
Crear `examples/minimal_sdd_instance/` que demuestre una instancia con `sdd.enabled: true`, una
spec en `specs/`, y una tarea implementable con los 6 campos SDD que valida en verde.

## SDD (pendiente de TASK-0008)
- `spec_id`: _pendiente_
- `execution_pipeline`: _pendiente_
- `acceptance_criteria`: la instancia valida en verde con SDD activado; incluye al menos 1 spec y 1 tarea implementable conforme.
- `linked_decisions`: DECISION-0004, DECISION-0002
- `test_plan`: validador (.py y .ps1) sobre `examples/minimal_sdd_instance` → OK.
- `closure_criteria`: _pendiente_

## riesgos
- No romper los ejemplos existentes; no introducir dominio en el ejemplo SDD (debe ser neutral).
