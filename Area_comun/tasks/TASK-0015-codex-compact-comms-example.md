---
id: TASK-0015
owner: Codex
status: done
type: implementation
priority: low
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0014]
relates_to: [TASK-0014]
phase: P2
spec_id: Area_comun/specs/SPEC-0015-compact-comms-example.md
execution_pipeline: [Crear examples/compact_communication_case, Anadir 1-2 mensajes compactos con codigos estandar y una question, Anadir handoff compacto de ejemplo, Validar .py y .ps1, Barrido de neutralidad, Handoff y liberar claim]
acceptance_criteria: [Ejemplo valida verde en .py y .ps1, Mensajes usan formato compacto y codigos estandar, Neutral de dominio, No rompe ejemplos existentes]
linked_decisions: [DECISION-0005, DECISION-0002]
test_plan: [.py y .ps1 sobre examples/compact_communication_case, Barrido de neutralidad]
closure_criteria: [Ejemplo verde en ambos validadores, Neutral, Handoff documenta criterios y pruebas, Claim liberado]
review: Aceptada por Claude contra SPEC-0015. examples/compact_communication_case valida verde en .py/.ps1; mensajes compactos (type OK/REVIEW, one_line_summary, context_refs, una question) + handoff; neutral; ejemplos previos verdes. Ultimo entregable de v0.5.0.
---

# TASK-0015 — Ejemplo compact_communication_case

> `implementation` → SDD obligatorio. SDD-elegible (ver `spec_id`). Implementar contra
> [SPEC-0015](../specs/SPEC-0015-compact-comms-example.md). Depende de TASK-0014 (validador).

## SDD
Los 6 campos están en el frontmatter (canónico) y detallados en la spec.

## riesgos
- El ejemplo debe ser neutral y no introducir dominio.

## notas_de_ejecucion
- Creado `examples/compact_communication_case/`.
- Incluye mensaje `REVIEW`, respuesta `OK` y handoff compacto de ejemplo.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0015-codex-to-claude-1.md`.
