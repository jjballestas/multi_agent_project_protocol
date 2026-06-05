---
id: TASK-0009
owner: Codex
status: proposed
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0008]
relates_to: [TASK-0010, TASK-0011]
phase: P2
---

# TASK-0009 — Actualizar templates de tareas/handoffs/reportes para SDD

> Tipo `implementation` → **SDD obligatorio**. No puede pasar a `ready`/`claimed`/`in_progress`
> hasta que TASK-0008 entregue su `spec_id`. Los 6 campos SDD siguientes están **pendientes**.

## objetivo
Actualizar las plantillas de protocolo para incorporar `type` y los campos SDD (o los 4 mínimos),
y reflejar criterios cumplidos + pruebas ejecutadas en handoffs/reportes.

## archivos_relevantes (propuesta; confirmar en spec)
- `Area_comun/protocol/TASK_PROTOCOL.md` (gate SDD + discovery-antes-de-implementar)
- `Area_comun/protocol/TASK_TEMPLATE.md` (`type` + campos SDD/mínimos)
- `Area_comun/protocol/HANDOFF_TEMPLATE.md` (criterios cumplidos + pruebas)
- `Area_comun/reports/HUMAN_REPORT_TEMPLATE.md`

## SDD (pendiente de TASK-0008)
- `spec_id`: _pendiente (lo asigna TASK-0008)_
- `execution_pipeline`: _pendiente_
- `acceptance_criteria`: _pendiente_
- `linked_decisions`: DECISION-0004, DECISION-0001
- `test_plan`: _pendiente_
- `closure_criteria`: _pendiente_

## riesgos
- Mantener neutralidad de dominio en todas las plantillas del core.
