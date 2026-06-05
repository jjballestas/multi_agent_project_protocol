---
id: TASK-0011
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0008, TASK-0010]
relates_to: [TASK-0009, TASK-0012]
phase: P2
spec_id: Area_comun/specs/SPEC-0011-validator-sdd.md
execution_pipeline: [Add sdd config template block, Implement Python SDD validator, Mirror PowerShell SDD validator, Create SDD golden cases, Verify parity and existing examples, Create handoff and release claim]
acceptance_criteria: [SDD disabled preserves existing behavior, SDD enabled errors on missing full fields, SDD enabled errors on unresolved spec_id, Pre-SDD tasks are exempt, Lightweight tasks warn on missing minimum fields, Python and PowerShell have matching exits and output]
linked_decisions: [DECISION-0004, DECISION-0001, DECISION-0003]
test_plan: [Run SDD golden case harness, Run Python validator on root and examples, Run PowerShell validator on root and examples, Run domain neutrality scan]
closure_criteria: [Golden cases pass, Existing examples remain valid, Handoff documents criteria and tests, Claim released]
review: Aceptada por Claude contra SPEC-0011. Verificacion independiente - golden cases SDD OK en .ps1 (harness) y .py (exit 0/1/0/0 esperados; mensajes por campo + spec_id-not-found + warnings ligeros). Paridad confirmada. SDD off => validadores verdes en root + 3 ejemplos. Bloque sdd (default off) en protocol.config.template. Sin migracion retroactiva.
---

# TASK-0011 — Actualizar validadores para modo SDD

> Tipo `implementation` → **SDD obligatorio**. TASK-0008 ya entregó la spec: **SDD-elegible**.

## objetivo
Añadir, de forma **aditiva**, el modo SDD a `validate_collaboration_state.{py,ps1}` y el bloque
`sdd` a `protocol.config.template.json`, con paridad y golden cases.

## comportamiento esperado (de DECISION-0004 §9-§10)
- Sin `sdd.enabled` (o false): comportamiento idéntico al actual (no rompe históricas ni ejemplos).
- `sdd.enabled: true`, `enforcement: "new_implementable_tasks"`:
  - ERROR si tarea implementable nueva en ready/claimed/in_progress carece de algún campo SDD o el `spec_id` no existe.
  - WARNING si tarea discovery/analysis/review/documentation/triage no declara objective/expected_output/question_to_resolve/closure_criterion.
  - Exime tareas históricas/pre-SDD (sin migración retroactiva).

## SDD (resuelto — ver spec_id)
Los 6 campos están definidos en [SPEC-0011-validator-sdd.md](../specs/SPEC-0011-validator-sdd.md):
comportamiento config-gated, exención pre-SDD, reglas ERROR/WARNING, golden cases en
`examples/sdd_validation_cases/` y paridad `.py`↔`.ps1`. Implementar contra esa spec y DISENO-SDD §4.

## riesgos
- Romper compatibilidad: los chequeos solo aplican con `sdd.enabled`. Mantener paridad .py/.ps1.

## notas_de_ejecucion
- Implementado modo SDD config-gated en ambos validadores.
- Creado `examples/sdd_validation_cases/` con harness de paridad.
- Validadores existentes siguen verdes con SDD apagado.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0011-codex-to-claude-1.md`.
