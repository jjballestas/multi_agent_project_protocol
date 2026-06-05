---
id: TASK-0008
owner: Claude
status: done
type: analysis
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0009, TASK-0010, TASK-0011, TASK-0012, TASK-0013]
phase: P2
review: Done por Claude (arquitecto). Entregado Area_comun/artifacts/DISENO-SDD.md (contratos de campos, cambios a templates, comportamiento del validador config-gated + exencion pre-SDD, esquema sdd, indice de specs) y las specs concretas SPEC-0009..0013 en Area_comun/specs/. spec_id fijado en TASK-0009..0013 (ahora SDD-elegibles). Pregunta abierta resuelta: una spec por tarea + matriz de trazabilidad. Validadores .py/.ps1 verdes. Desbloquea a Codex (HANDOFF-TASK-0008-claude-to-codex-2).
---

# TASK-0008 — Diseñar SDD + pipeline + criterios de cierre

> Tipo `analysis` (SDD ligero): no requiere los 6 campos SDD completos, pero sí los 4 mínimos.
> Es el **bootstrap**: produce las specs contra las que se implementan TASK-0009..0012.

## objective
Diseñar en detalle la capa SDD que fija [DECISION-0004](../decisions/DECISION-0004-sdd-pipeline-y-cierre.md):
contratos exactos de los 6 campos SDD y los 4 mínimos, cambios al ciclo de vida, forma de las
plantillas de `specs/`, comportamiento del validador y esquema de config `sdd`.

## expected_output
- Artefacto de diseño en `Area_comun/artifacts/` con: contrato de campos, reglas del validador
  (error/warning), esquema `sdd` y mapa de cambios a templates.
- La(s) spec(s) (`spec_id`) que gobernarán TASK-0009..0012 (una por tarea o una global del rollout).

## question_to_resolve
¿Cuál es el conjunto exacto de campos, reglas de validación (qué es error vs warning), forma de las
4 plantillas y esquema de config, de modo que TASK-0009..0012 se implementen sin ambigüedad?

## closure_criterion
- Diseño aprobado por revisión; specs escritas y referenciables por `spec_id`.
- Cada TASK-0009..0012 tiene su `spec_id` resoluble para poder pasar a `ready`.
- Handoff a Codex con el plan de implementación.

## linked_decisions
- DECISION-0004 (SDD), DECISION-0001 (versionado: capa = MINOR v0.4.0), DECISION-0002 (core neutral).

## riesgos
- Sobre-diseño: mantener mínimo viable y neutral de dominio.
