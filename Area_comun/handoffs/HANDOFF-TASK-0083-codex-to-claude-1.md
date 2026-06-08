---
handoff_id: HANDOFF-TASK-0083-codex-to-claude-1
task_id: TASK-0083
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0083 - Bridge Agent Teams Capas A+B

## Entrega

Implementadas solo las Capas A+B de SPEC-0065:

- `runtime/team_bridge.py` lee JSON por stdin y acepta `--event TaskCreated|TaskCompleted|TeammateIdle`.
- Sin `runtime.team_bridge.enabled:true` y registro valido, sale 0 como no-op y no escribe audit.
- Capa A (`"gate"`): en `TaskCompleted`/`TeammateIdle` corre `validate_collaboration_state.py` y
  `scan_domain_neutrality.py`; si el payload trae `turn_report` o `turn_report_path`, corre tambien
  `runtime/turn_validate.py`. Fallo de gate => stderr + exit 2.
- Capa B (`"audit"`): anexa `{observed_at, hook, ...payload}` a
  `Area_comun/state/team_audit.jsonl` con `ensure_ascii=True`, sin mutar `state/*.json`.
- Error de audit no rompe el team: se informa por stderr y el proceso sale 0 si no hubo fallo de gate.
- `runtime.team_bridge` se agrego apagado (`enabled:false`, `layers:[]`) en instancia y template.
- `runtime/team_bridge.py` se agrego explicitamente a `domain_neutrality.scan_globs`.
- `examples/team_bridge_cases/` queda en CI.

## Fuera de alcance respetado

- No implemente Capa C.
- No llame a `submit_intent`.
- No active el bridge en la instancia viva.
- No toque `.claude/settings.json`.
- Un payload con `[TASK-XXXX]` solo se audita en A+B.

## Archivos tocados

- `runtime/team_bridge.py`
- `examples/team_bridge_cases/run_team_bridge_cases.py`
- `protocol.config.json`
- `protocol.config.template.json`
- `.github/workflows/validate.yml`
- `Area_comun/tasks/TASK-0083-codex-team-bridge-capas-AB.md`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/TASK_INDEX_ARCHIVE.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/CLAIMS_ARCHIVE.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0082-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0083-GO-team-bridge-AB.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0083-in-review.md`

## Validacion

- `python -m py_compile runtime\team_bridge.py examples\team_bridge_cases\run_team_bridge_cases.py` -> OK.
- `python examples\team_bridge_cases\run_team_bridge_cases.py` -> OK, 7 cases.
- `python scripts\validate_collaboration_state.py --root .` -> OK, warning esperado de runtime drift.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `python examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py` -> OK, 5 cases.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 4 cases.
- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK, 8 cases.
- `python examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py` -> OK, 7 cases.
- `python scripts\prune_state.py --root . --check` -> OK.
- `git diff --check` -> OK, solo warnings CRLF.

## Riesgos residuales

- La activacion real de A+B en la instancia viva sigue siendo un paso separado con registro de operador.
- Capa C queda diferida a precondiciones DECISION-0022.

## Requested action

Ratificar TASK-0083 contra SPEC-0065 y cerrar como done si procede.
