---
id: TASK-0010
owner: Codex
status: proposed
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0008]
relates_to: [TASK-0009, TASK-0011, TASK-0012]
phase: P2
---

# TASK-0010 — Crear carpeta specs/ y plantillas SDD

> Tipo `implementation` → **SDD obligatorio**. `proposed` hasta que TASK-0008 entregue `spec_id`.

## objetivo
Crear `Area_comun/specs/` y las plantillas SDD reutilizables (neutrales de dominio).

## archivos_relevantes (propuesta; confirmar en spec)
- `Area_comun/specs/SPEC_TEMPLATE.md`
- `Area_comun/specs/PROJECT_BRIEF_TEMPLATE.md`
- `Area_comun/specs/TEST_PLAN_TEMPLATE.md`
- `Area_comun/specs/TRACEABILITY_MATRIX_TEMPLATE.md`

## SDD (pendiente de TASK-0008)
- `spec_id`: _pendiente_
- `execution_pipeline`: _pendiente_
- `acceptance_criteria`: las 4 plantillas existen, son neutrales y cubren los 6 campos SDD + los 4 mínimos.
- `linked_decisions`: DECISION-0004, DECISION-0002 (neutralidad)
- `test_plan`: _pendiente_ (validador verde; sin términos de stack)
- `closure_criteria`: _pendiente_

## riesgos
- Las plantillas son masters del core: deben quedar neutrales (sin trading/.NET/SQL/Azure).
