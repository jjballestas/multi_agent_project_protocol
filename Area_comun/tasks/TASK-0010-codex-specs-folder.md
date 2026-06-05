---
id: TASK-0010
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0008]
relates_to: [TASK-0009, TASK-0011, TASK-0012]
phase: P2
spec_id: Area_comun/specs/SPEC-0010-specs-folder.md
review: Aceptada por Claude contra SPEC-0010. Las 4 plantillas requeridas + 2 aditivas (REQUIREMENTS, ACCEPTANCE_CRITERIA) declaradas como desviacion aditiva y neutral; SPEC_TEMPLATE cubre los 6 campos. Neutralidad OK; validadores verdes.
---

# TASK-0010 — Crear carpeta specs/ y plantillas SDD

> Tipo `implementation` → **SDD obligatorio**. TASK-0008 ya entregó la spec: **SDD-elegible**.
> Nota: `Area_comun/specs/` ya existe (la creó TASK-0008 con las specs concretas); esta tarea añade
> las **plantillas reutilizables** (SPEC_TEMPLATE, PROJECT_BRIEF_TEMPLATE, TEST_PLAN_TEMPLATE,
> TRACEABILITY_MATRIX_TEMPLATE).

## objetivo
Crear `Area_comun/specs/` y las plantillas SDD reutilizables (neutrales de dominio).

## archivos_relevantes (propuesta; confirmar en spec)
- `Area_comun/specs/SPEC_TEMPLATE.md`
- `Area_comun/specs/PROJECT_BRIEF_TEMPLATE.md`
- `Area_comun/specs/TEST_PLAN_TEMPLATE.md`
- `Area_comun/specs/TRACEABILITY_MATRIX_TEMPLATE.md`

## SDD (resuelto — ver spec_id)
Los 6 campos están definidos en [SPEC-0010-specs-folder.md](../specs/SPEC-0010-specs-folder.md).
Implementar contra esa spec (las 4 plantillas neutrales; sin tocar las specs concretas SPEC-0009..0013).

## riesgos
- Las plantillas son masters del core: deben quedar neutrales (sin trading/.NET/SQL/Azure).

## notas_de_ejecucion
- 2026-06-05 Codex: creadas seis plantillas reutilizables en `Area_comun/specs/`.
- 2026-06-05 Codex: `REQUIREMENTS_TEMPLATE.md` y `ACCEPTANCE_CRITERIA_TEMPLATE.md` se agregaron por peticion explicita del humano, de forma aditiva.
- 2026-06-05 Codex: handoff creado en `Area_comun/handoffs/HANDOFF-TASK-0010-codex-to-claude-1.md`.
