---
spec_id: SPEC-0013-doc-sdd-onboarding
task_id: TASK-0013
type: documentation
status: ready
linked_decisions: [DECISION-0004, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0013 — Documentar inicio de proyecto con SDD

> Tipo `documentation`: campos mínimos. Como toca `README_INSTANCIACION.md` (publicado), la revisión
> cruzada aplica rigor de implementable (criterio del arquitecto).

## objective
Documentar el flujo de adopción de SDD: activar `sdd`, escribir una spec, declarar los campos en una
tarea implementable y pasar la revisión cruzada.

## expected_output
Sección nueva en `README_INSTANCIACION.md` (y/o doc en `Area_comun/`) con el paso a paso, enlazando
plantillas de `specs/` y el ejemplo `examples/minimal_sdd_instance/`.

## question_to_resolve
¿Cuál es el paso a paso mínimo para que un proyecto nuevo arranque en modo SDD sin ambigüedad?

## closure_criterion
Documentación coherente con DISENO-SDD §4, enlaza specs/templates + ejemplo; revisión cruzada OK;
validadores verdes. Neutral de dominio.
