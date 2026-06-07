---
handoff_id: HANDOFF-TASK-0076-codex-to-claude-1
task_id: TASK-0076
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0076 - submit_intent transaccional + re-genesis

## Entrega

Implementado SPEC-0062 en modo sombra, sin activar `event_state.enforce` ni `authoritative`:

- `runtime/submit_intent.py` conserva `--intent` mono-intent y agrega `--intents`/`--intents-json`.
- El envelope transaccional acepta `{actor_id,timestamp,commit,intents:[...]}`; CLI puede sobreescribir esos campos.
- `submit_intents()` normaliza todos los intents, valida cada uno contra el estado resultante de aplicar los previos, y rechaza idempotency keys duplicadas.
- La transaccion emite un `intent.applied` por intent con metadata `{idempotency_key,index,count}`, materializa una sola vez al final, actualiza side-effects de task markdown, y verifica drift 0.
- Rollback total: si falla cualquier paso de escritura/materializacion, restaura archivos protocol-state, task files y `runtime/state`.
- Idempotencia: repetir la misma transaccion no duplica eventos.
- `runtime/regenesis.py` (+ `.ps1`) escribe un genesis fresco por `snapshot_ref` desde el hot state actual, idempotente y no destructivo; deja `protocol_state_drift.has_drift=False`.

## Archivos tocados

- `.github/workflows/validate.yml`
- `runtime/submit_intent.py`
- `runtime/submit_intent.ps1`
- `runtime/regenesis.py`
- `runtime/regenesis.ps1`
- `examples/intent_tx_cases/run_intent_tx_cases.py`
- `Area_comun/tasks/TASK-0076-codex-submit-intent-transaccional-regenesis.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/CLAIMS_ARCHIVE.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/TASK_INDEX_ARCHIVE.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0075-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-respuesta-anomalia-task0076.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0076-GO-submit-intent.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0076-in-review.md`

## Validacion ejecutada

- `python examples\intent_tx_cases\run_intent_tx_cases.py` -> OK, 6 casos.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 9 casos.
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK, 6 casos.
- `python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` -> OK, 6 casos.
- `python examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py` -> OK, 7 casos.
- `python examples\runtime_protocol_genesis_ref_cases\run_runtime_protocol_genesis_ref_cases.py` -> OK, 9 casos.
- `python -m py_compile runtime\submit_intent.py runtime\regenesis.py examples\intent_tx_cases\run_intent_tx_cases.py` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `powershell -NoProfile -File scripts\scan_domain_neutrality.ps1 -Root .` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning esperado de drift por modo sombra.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, con warning esperado de drift por modo sombra.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK.
- `python scripts\prune_state.py --root . --apply` -> `claims_archived=3`, `tasks_archived=1`, cold-start final ~12.9k tokens.
- `python scripts\prune_state.py --root . --check` -> OK, cold-start final ~12.9k tokens.
- `git diff --check` -> exit 0, solo warnings CRLF esperados en Windows.

## Notas de revision

- No se enciende `enforce` ni `authoritative`.
- El mailbox sigue fuera de submit_intent, segun SPEC-0062.
- Re-genesis no destruye historia: agrega un nuevo genesis por referencia que pasa a ser la base efectiva del replay.
