---
task_id: TASK-0224
title: "Fix redactor de reportes: bug de fechas + todo reporte lleva hora (updated) + estado dataset recontado X/500"
type: build
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0040]
file: Area_comun/tasks/TASK-0224-codex-fix-redactor-fechas-reportes.md
---

# TASK-0224 — Fix redactor de reportes (fechas + hora + dataset)

- **Owner:** Codex (build) · **Review:** Arquitecto + Analista
- **Linked:** DECISION-0040 (dataset)

## Contexto
El redactor de reportes (`scripts/generate_human_guide.py` y/o el redactor de
`Area_comun/reports/`) tiene un bug de fechas. Regla del operador: **todo reporte debe llevar
SIEMPRE hora (campo updated) + estado del dataset recontado X/500** (eligibles
`seq>=2221 ∧ intent.applied ∧ ed25519`, desglose por agente).

## Alcance
1. Corregir el bug de fechas del redactor.
2. Inyectar en cada reporte: timestamp `updated` (hora real) + línea de estado dataset X/500 con desglose.

## DoD
- Reporte de muestra generado con hora + dataset correctos (evidencia).
- Sin regresiones en los reportes existentes.
- Gate.

## Handoff
Autocontenida. Ambigüedad → `blocked` + 1 pregunta concreta.
