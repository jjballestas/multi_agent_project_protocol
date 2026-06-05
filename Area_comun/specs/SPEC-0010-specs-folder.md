---
spec_id: SPEC-0010-specs-folder
task_id: TASK-0010
type: implementation
status: ready
linked_decisions: [DECISION-0004, DECISION-0002]
created_at: 2026-06-05
author: Claude
---

# SPEC-0010 — Crear specs/ y plantillas SDD reutilizables

## Contexto
`Area_comun/specs/` ya existe (creada por TASK-0008 con las specs concretas del rollout). Falta el
juego de **plantillas reutilizables**. Ver [DISENO-SDD.md](../artifacts/DISENO-SDD.md) §3.

## Alcance
Crear en `Area_comun/specs/`: `SPEC_TEMPLATE.md`, `PROJECT_BRIEF_TEMPLATE.md`,
`TEST_PLAN_TEMPLATE.md`, `TRACEABILITY_MATRIX_TEMPLATE.md`.

## No-alcance
No modificar las specs concretas SPEC-0009..0013 (son de TASK-0008). No tocar el validador.

## execution_pipeline
1. `SPEC_TEMPLATE.md`: los 6 campos SDD + Contexto + Alcance + No-alcance + Riesgos (placeholders `{{...}}`).
2. `PROJECT_BRIEF_TEMPLATE.md`: brief inicial de proyecto/iniciativa (objetivo, alcance, decisiones, riesgos).
3. `TEST_PLAN_TEMPLATE.md`: plan de pruebas reutilizable (qué, cómo, comandos, criterios).
4. `TRACEABILITY_MATRIX_TEMPLATE.md`: columnas requisito | spec_id | task_id | prueba | closure_criterion | estado.
5. Validar y handoff.

## acceptance_criteria
- Las 4 plantillas existen, son **neutrales de dominio** y solo contienen placeholders/estructura.
- `SPEC_TEMPLATE.md` cubre los 6 campos SDD exactamente como DISENO §1.1.
- Coherentes con `TASK_TEMPLATE.md` (TASK-0009).

## test_plan
- Barrido de neutralidad sobre `Area_comun/specs/*TEMPLATE*` (sin términos de stack).
- Validadores `.py`/`.ps1` verdes en raíz + ejemplos (specs/ no rompe el validador actual).

## closure_criteria
- acceptance_criteria cumplidos; handoff con criterios + pruebas; validadores verdes.
