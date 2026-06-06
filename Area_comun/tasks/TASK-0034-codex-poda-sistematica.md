---
id: TASK-0034
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0033]
relates_to: [TASK-0023, TASK-0024]
phase: P2
spec_id: Area_comun/specs/SPEC-0033-poda-sistematica.md
linked_decisions: [DECISION-0014, DECISION-0008, DECISION-0006, DECISION-0001]
execution_pipeline: [scripts/prune_state.py --check/--apply (.ps1 paridad) reusando measure_context_cost + formato *_ARCHIVE de 0024, bloque maintenance en protocol.config(.template).json (context_budget/done_ratio/released_ratio/recent_window), pre-commit hook bloqueante + doc, paso CI prune_state --check hard-fail, golden examples/prune_state_cases]
acceptance_criteria: [--check read-only exit 1 sobre umbral / exit 0 si no, --apply idempotente archive!=delete respeta ventana reciente y baja cold-start, umbrales en config warning vs hard-fail, CI falla sobre hard-fail, hook bloquea sin mutar, paridad py/ps1, validador+scan verdes hot+archive]
test_plan: [golden examples/prune_state_cases (due/no-due/idempotencia/ventana) + medicion antes/despues con measure_context_cost --json + paridad ps1 atestiguada]
closure_criteria: [prune_state check/apply py+ps1 + config umbrales + hook bloqueante + CI hard-fail + golden + medicion que demuestra descenso de cold-start, handoff autocontenido, claim liberado al pasar a in_review]
---

# TASK-0034 - Poda sistematica por umbral medido (prune_state + hook + CI)

> `implementation` -> SDD; implementar contra [SPEC-0033](../specs/SPEC-0033-poda-sistematica.md) bajo
> DECISION-0014 (poda sistematica) + DECISION-0008 (eficiencia) + DECISION-0006 (robustez). El operador
> fijo el nucleo (umbral medido); implementacion convergida con tu aporte. **Secuencia: despues de TASK-0033.**

## Resumen
`prune_state.py` (.py/.ps1) con `--check` (read-only, exit 1 sobre umbral, reporte con comando + recupero
estimado) y `--apply` (idempotente; archiva done/released fuera de ventana reciente + barre mailbox viejo;
archive != delete). Umbrales en config. Pre-commit hook que BLOQUEA con aviso (no poda+re-stagea). Paso CI
`--check` con hard-fail. Reusa `measure_context_cost` para medir y el formato `*_ARCHIVE` de TASK-0024.

## archivos objetivo (previstos)
- `scripts/prune_state.py`, `scripts/prune_state.ps1`
- `protocol.config.json` + `protocol.config.template.json` (bloque maintenance/umbrales)
- `.githooks/pre-commit` (o doc de instalacion en TASK_PROTOCOL/README)
- `.github/workflows/` (paso CI --check hard-fail)
- `examples/prune_state_cases/`

## Dogfood
Aplica la regla de liveness (senal de progreso por turno) y handoff-release (libera el claim al pasar a
in_review, commitea WIP antes). ASCII-only en mailbox/state (DECISION-0012). Al cerrar, corre la poda real
sobre este repo (cold-start ~19.5k hoy -> objetivo ~9-10k) y reporta el antes/despues.
