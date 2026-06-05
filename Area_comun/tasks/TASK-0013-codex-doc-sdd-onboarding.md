---
id: TASK-0013
owner: Codex
status: proposed
type: documentation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0009, TASK-0010]
relates_to: [TASK-0012]
phase: P2
---

# TASK-0013 — Documentar cómo iniciar un proyecto con SDD

> Tipo `documentation`. Toca `README_INSTANCIACION.md` (publicado): se trata con rigor; declara
> los 4 campos mínimos y, si la revisión lo exige por tocar contrato, criterios de aceptación.

## objective
Documentar el flujo de adopción de SDD: cómo activar `sdd`, escribir una spec, declarar los campos
en una tarea implementable y pasar la revisión cruzada.

## expected_output
- Sección nueva en `README_INSTANCIACION.md` (y/o doc en `Area_comun/`) sobre inicio con SDD.

## question_to_resolve
¿Cuál es el paso a paso mínimo para que un proyecto nuevo arranque en modo SDD sin ambigüedad?

## closure_criterion
- Documentación enlaza specs/templates y el ejemplo `minimal_sdd_instance`; revisión OK; validador verde.

## linked_decisions
- DECISION-0004, DECISION-0001
