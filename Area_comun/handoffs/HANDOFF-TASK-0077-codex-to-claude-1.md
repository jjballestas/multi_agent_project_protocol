---
handoff_id: HANDOFF-TASK-0077-codex-to-claude-1
task_id: TASK-0077
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0077 - cutover del lazo Codex a submit_intent --intents

## Entrega

Implementado SPEC-0063 en modo sombra, sin activar `event_state.enforce` ni `authoritative` y sin re-genesis del
repo vivo:

- `runtime/ledger_ops.py` construye envelopes comunes con `schema_version: protocol_ledger_ops.v1`.
- `auto_claim_envelope()` mapea auto-claim a una transaccion `claim acquire` + `task_status ready->in_progress`.
- `handoff_release_envelope()` mapea handoff-release a `task_status in_progress->in_review` + `task_upsert`
  opcional + `claim release`, en ese orden para conservar autoridad de scope.
- `submit_envelope()` delega la escritura real a `submit_intent.submit_intents`; el helper no edita hot state por
  su cuenta.
- `runtime/ledger_ops.ps1` delega en Python y soporta `-Submit`.
- `examples/cutover_loop_cases` prueba fixture drift-0 con genesis limpia, materializacion esperada, drift 0,
  retries idempotentes y paridad CLI/PowerShell.
- CI ejecuta `Run Codex loop cutover cases`.

## Archivos tocados

- `.github/workflows/validate.yml`
- `runtime/ledger_ops.py`
- `runtime/ledger_ops.ps1`
- `examples/cutover_loop_cases/run_cutover_loop_cases.py`
- `Area_comun/tasks/TASK-0077-codex-cutover-submit-intent-loop.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0076-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0077-GO-cutover.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0077-in-review.md`
- `Area_comun/handoffs/HANDOFF-TASK-0077-codex-to-claude-1.md`

## Validacion ejecutada

- `python examples\cutover_loop_cases\run_cutover_loop_cases.py` -> OK, 4 casos.
- `python -m py_compile runtime\ledger_ops.py examples\cutover_loop_cases\run_cutover_loop_cases.py` -> OK.
- `python examples\intent_tx_cases\run_intent_tx_cases.py` -> OK, 6 casos.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 9 casos.
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK, 6 casos.
- `python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` -> OK, 6 casos.
- `python examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py` -> OK, 7 casos.
- `python examples\runtime_protocol_genesis_ref_cases\run_runtime_protocol_genesis_ref_cases.py` -> OK, 9 casos.
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning esperado de drift por modo sombra.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, con warning esperado de drift por modo sombra.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .` -> exit 0.
- `python scripts\prune_state.py --root . --apply` -> `claims_archived=3`, `tasks_archived=1`,
  `after_tokens=13237`.
- `python scripts\prune_state.py --root . --check` -> OK, cold-start ~13.2k tokens.
- `git diff --check` -> exit 0, solo warnings CRLF esperados en Windows.

## Notas de revision

- El repo vivo sigue en shadow y con drift warning esperado; no ejecute `runtime/regenesis.py` sobre el vivo.
- Claude ya integro en `1e65b91` el mandato documental del cutover; esta entrega cubre el lado Codex del helper y
  golden.
- El siguiente paso natural es ratificar TASK-0077 y ejecutar la activacion coordinada posterior solo cuando ambos
  lazos esten verificados y el rollback este ensayado.
