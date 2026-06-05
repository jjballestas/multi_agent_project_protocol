---
id: TASK-0025
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0023]
relates_to: [TASK-0024]
phase: P2
spec_id: Area_comun/specs/SPEC-0025-frontmatter-minimo.md
linked_decisions: [DECISION-0008, DECISION-0005, DECISION-0001]
execution_pipeline: [Definir set obligatorio + regla de omision, Template variante minima, Validador acepta minimo sin exigir omitidos, Golden cases minimo/legacy, Medir delta con measure_context_cost]
acceptance_criteria: [Mensaje minimo valido en .py/.ps1, omitidos asumen default, legacy sigue valido, checks existentes intactos (requires_response + higiene), overhead medido baja]
test_plan: [Golden minimo/legacy .py/.ps1, measure antes/despues, root + ejemplos verdes]
closure_criteria: [Template minimo + validador back-compat, golden verdes con paridad, delta medido, claim liberado]
---

# TASK-0025 — Frontmatter de mailbox mínimo

> `implementation` → SDD; implementar contra [SPEC-0025](../specs/SPEC-0025-frontmatter-minimo.md)
> y DECISION-0008 §3 + DECISION-0005. Aditivo y **compatible hacia atrás** (legacy sigue válido).
> Depende de TASK-0023 (medir el delta).
