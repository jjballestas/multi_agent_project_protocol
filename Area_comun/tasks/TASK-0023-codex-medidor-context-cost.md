---
id: TASK-0023
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0024, TASK-0025]
phase: P2
spec_id: Area_comun/specs/SPEC-0023-medidor-context-cost.md
linked_decisions: [DECISION-0008, DECISION-0001]
execution_pipeline: [measure_context_cost.py con 3 escenarios + divisor configurable + --json/--budget, Espejo .ps1, Bloque token_cost en protocol.config(.template), Golden case context_cost_cases, (opcional) paso CI con --budget WARNING]
acceptance_criteria: [Reporta cold-start/peso-muerto/overhead determinista, chars_per_token y coldstart_globs configurables, --json parseable y --budget avisa sin romper, paridad .py/.ps1, read-only]
test_plan: [Correr sobre root (cold-start ~baseline), golden case con fixture de tamano conocido, paridad .py/.ps1]
closure_criteria: [Medidor funcional con --json/--budget, paridad, golden case, handoff reproduce baseline, claim liberado]
---

# TASK-0023 — Medidor de costo de contexto

> `implementation` → SDD; implementar contra [SPEC-0023](../specs/SPEC-0023-medidor-context-cost.md)
> y DECISION-0008 §1/§4. **Primero del lote** (sin medidor no hay before/after). Aditivo, neutral, read-only.

## Resumen
Herramienta del gate antes/después (DECISION-0008). Ver baseline en
`Area_comun/artifacts/DISENO-eficiencia-de-tokens.md` §1.
