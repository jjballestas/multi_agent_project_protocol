---
id: TASK-0009
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0008]
relates_to: [TASK-0010, TASK-0011]
phase: P2
spec_id: Area_comun/specs/SPEC-0009-sdd-templates.md
review: Aceptada por Claude contra SPEC-0009. TASK_PROTOCOL (gate SDD + clarity-before-execution + tipos + review contra spec), TASK_TEMPLATE (type + 6 campos SDD + 4 ligeros + DoD), HANDOFF_TEMPLATE (spec_id + criterios + pruebas + desviaciones) y HUMAN_REPORT actualizados. Neutralidad core/templates OK; validadores .py/.ps1 verdes.
---

# TASK-0009 — Actualizar templates de tareas/handoffs/reportes para SDD

> Tipo `implementation` → **SDD obligatorio**. TASK-0008 ya entregó la spec: **SDD-elegible**.
> Codex puede pasarla a `ready`/`claimed` al reclamarla.

## objetivo
Actualizar las plantillas de protocolo para incorporar `type` y los campos SDD (o los 4 mínimos),
y reflejar criterios cumplidos + pruebas ejecutadas en handoffs/reportes.

## archivos_relevantes (propuesta; confirmar en spec)
- `Area_comun/protocol/TASK_PROTOCOL.md` (gate SDD + discovery-antes-de-implementar)
- `Area_comun/protocol/TASK_TEMPLATE.md` (`type` + campos SDD/mínimos)
- `Area_comun/protocol/HANDOFF_TEMPLATE.md` (criterios cumplidos + pruebas)
- `Area_comun/reports/HUMAN_REPORT_TEMPLATE.md`

## SDD (resuelto — ver spec_id)
Los 6 campos están definidos en [SPEC-0009-sdd-templates.md](../specs/SPEC-0009-sdd-templates.md):
`execution_pipeline`, `acceptance_criteria`, `linked_decisions` (DECISION-0004/0002/0001),
`test_plan` (neutralidad + validadores verdes) y `closure_criteria`. Implementar contra esa spec.

## riesgos
- Mantener neutralidad de dominio en todas las plantillas del core.

## notas_de_ejecucion
- 2026-06-05 Codex: actualizadas plantillas `TASK_PROTOCOL`, `TASK_TEMPLATE`, `HANDOFF_TEMPLATE` y `HUMAN_REPORT_TEMPLATE`.
- 2026-06-05 Codex: barrido de neutralidad sin coincidencias sobre plantillas SDD/core.
- 2026-06-05 Codex: handoff creado en `Area_comun/handoffs/HANDOFF-TASK-0009-codex-to-claude-1.md`.
