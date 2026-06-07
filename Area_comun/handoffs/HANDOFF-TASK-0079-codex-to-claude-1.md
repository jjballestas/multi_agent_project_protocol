---
handoff_id: HANDOFF-TASK-0079-codex-to-claude-1
task_id: TASK-0079
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0079 - SA.2 kill-switch + reloj

## Entrega

Implementado SPEC-0064 SA.2 en shadow, sin tocar el invoker real y sin encender autonomia:

- `runtime/supervised_autonomy.py` valida `caps.wall_clock_ms` como cap obligatorio junto a `max_turns`.
- El payload normalizado incluye `wall_clock_ms`.
- El runreport markdown incluye `caps.wall_clock_ms`.
- `pause_sentinel_path(root)` fija el centinela `runtime/state/PAUSE`.
- `runtime/orchestrator.py` comprueba el centinela **antes de cada turno**; si existe, registra
  `outcome=paused` sin ejecutar adapter ni mutar estado.
- El loop acumula duracion determinista con `--clock-fixed`; antes de un turno que excederia
  `caps.wall_clock_ms`, para con `outcome=wallclock_exhausted`.
- `protocol.config.json` y template mantienen `runtime.supervised_autonomy.enabled=false`, ahora con
  `caps.wall_clock_ms=300000`.
- `examples/supervised_autonomy_cases` queda ampliado a 6 golden cases: max_turns, pausa, reloj, rechazo sin
  registro, off sin flag, cerrojo real intacto.

## Archivos tocados

- `protocol.config.json`
- `protocol.config.template.json`
- `runtime/orchestrator.py`
- `runtime/supervised_autonomy.py`
- `examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py`
- `Area_comun/tasks/TASK-0079-codex-autonomia-SA2-killswitch-reloj.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0078-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0079-GO-autonomia-SA2.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0079-in-review.md`
- `Area_comun/handoffs/HANDOFF-TASK-0079-codex-to-claude-1.md`

## Validacion ejecutada

- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK, 6 casos.
- `python -m py_compile runtime\orchestrator.py runtime\supervised_autonomy.py examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK.
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> OK, 8 casos.
- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> OK, 6 casos.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 4 casos.
- `python examples\runtime_budget_cases\run_runtime_budget_cases.py` -> OK, 5 casos.
- `python examples\runtime_observability_cases\run_runtime_observability_cases.py` -> OK, 5 casos.
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py` -> OK, 4 casos.
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning esperado de drift por modo sombra.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, con warning esperado de drift por modo sombra.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .` -> exit 0.
- `python scripts\prune_state.py --root . --apply` -> `claims_archived=2`, `tasks_archived=1`,
  `after_tokens=12799`.
- `python scripts\prune_state.py --root . --check` -> OK, cold-start ~12.8k tokens.
- `git diff --check` -> exit 0, solo warnings CRLF esperados en Windows.

## Notas de revision

- `runtime/state/PAUSE` no se commitea; es centinela operativo.
- La pausa se registra en runlog/runreport, pero no ejecuta adapter ni commit de turno.
- El reloj se evalua antes del turno que excederia el cap, de modo que no hay medio turno aplicado.
- El invoker real sigue rechazando subprocess multi-turno sin `--once`.
- Queda para SA.3: checkpoint humano + escalacion.
