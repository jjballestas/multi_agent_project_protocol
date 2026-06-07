---
handoff_id: HANDOFF-TASK-0078-codex-to-claude-1
task_id: TASK-0078
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0078 - SA.1 autonomia supervisada en shadow

## Entrega

Implementado SPEC-0064 SA.1 sin tocar el invoker real y sin encender autonomia:

- `protocol.config.json` y `protocol.config.template.json` declaran `runtime.supervised_autonomy` off-by-default.
- `runtime/supervised_autonomy.py` agrega `supervised_autonomy_activation_error(config)`, payload normalizado y
  escritor de `*.runreport.md`.
- `runtime/orchestrator.py` agrega `--allow-supervised-autonomy`.
- Sin flag, el comportamiento existente queda intacto: no cap, no runreport, sin campos nuevos en el resultado.
- Con flag + registro valido, el loop recorded respeta `caps.max_turns`; si hay mas trabajo, para con
  `outcome=max_turns_reached`.
- El runreport markdown resume turnos, costo, commits, motivo de cierre y registro de activacion.
- El invoker real mantiene el cerrojo `subprocess llm invoker requires --once`; SA.1 no lo levanta.
- `examples/supervised_autonomy_cases` cubre max_turns, rechazo sin registro, off sin flag, y cerrojo real intacto.
- CI ejecuta `Run supervised autonomy cases`.

## Archivos tocados

- `.github/workflows/validate.yml`
- `protocol.config.json`
- `protocol.config.template.json`
- `runtime/orchestrator.py`
- `runtime/supervised_autonomy.py`
- `examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py`
- `Area_comun/tasks/TASK-0078-codex-autonomia-SA1-sobre-shadow.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0077-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0078-GO-autonomia-SA1.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0078-in-review.md`
- `Area_comun/handoffs/HANDOFF-TASK-0078-codex-to-claude-1.md`

## Validacion ejecutada

- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK, 4 casos.
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
  `after_tokens=12965`.
- `python scripts\prune_state.py --root . --check` -> OK, cold-start ~13.0k tokens.
- `git diff --check` -> exit 0, solo warnings CRLF esperados en Windows.

## Notas de revision

- No se activo autonomia: `runtime.supervised_autonomy.enabled` queda `false` en la config viva y template.
- No se toco el invoker real: el caso de subprocess sin `--once` sigue rechazando antes de ejecutar comando.
- El ajuste de baseline dirty tras un turno exitoso evita que el propio runlog del runtime bloquee el siguiente
  turno recorded como cambio no declarado.
- Queda para SA.2: kill-switch + reloj de pared.
