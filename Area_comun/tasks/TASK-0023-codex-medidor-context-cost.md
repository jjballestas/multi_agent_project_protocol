---
id: TASK-0023
owner: Codex
status: done
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
## Ejecucion Codex
- Implementado `scripts/measure_context_cost.py` y `scripts/measure_context_cost.ps1`.
- Agregado `token_cost` a `protocol.config.json` y `protocol.config.template.json`.
- Agregado golden case `examples/context_cost_cases/` con paridad `.py`/`.ps1`.
- Baseline reproducido sobre root: cold-start `34972` tok, claims released `97.73%`, tasks done `85.19%`,
  frontmatter/body `1.7464`, frontmatter `63.59%`; `--budget` avisa sin romper.

## Revision Claude
- Ratificada contra SPEC-0023: cumple escenarios deterministas, config `token_cost`, `--json`,
  `--budget` read-only y golden cases. Sin cambios requeridos.

## Ratificacion Claude (arquitecto)
RATIFICADA contra SPEC-0023. Verificacion independiente read-only (`.py`) por Claude sobre root:
cold-start `35619` tok; claims released `100%`; tasks done `85.19%`; frontmatter/body `1.8061`;
frontmatter `64.36%`; `--budget 30000` => WARNING sin romper (exit 0). Confirmados los 3 escenarios
(cold-start/peso-muerto/overhead), `chars_per_token`/`coldstart_globs` configurables con defaults,
`--json` parseable y read-only (arbol intacto tras correr). Drift vs baseline del handoff esperado
(el estado creció). Paridad `.ps1` atestiguada por Codex/CI (deny-rule PowerShell en sesion arquitecto).
**Transicion a `done` PENDIENTE** de liberar `TASK_INDEX.json`/`PROJECT_STATE.json` (bajo claim activo
de Codex por TASK-0027). Se aplica al liberar el estado; veredicto ya firme.
