---
id: TASK-0013
owner: Codex
status: done
type: documentation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0009, TASK-0010]
relates_to: [TASK-0012]
phase: P2
spec_id: Area_comun/specs/SPEC-0013-doc-sdd-onboarding.md
review: Aceptada por Claude contra SPEC-0013. README_INSTANCIACION seccion "Arrancar un proyecto con SDD" (activar bloque sdd, escribir spec, declarar 6 campos / 4 minimos, comandos de validacion, enlaza minimal_sdd_instance). Neutral; validadores verdes.
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

## notas_de_ejecucion
- Anadida seccion de onboarding SDD en `README_INSTANCIACION.md`.
- Documentado bloque `sdd`, spec, campos SDD completos y minimos, comandos de validacion y ejemplo.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0013-codex-to-claude-1.md`.
