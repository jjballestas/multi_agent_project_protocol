# HANDOFF TASK-0086 - Codex to Claude

Date: 2026-06-08
Owner: Codex
Status: ready for in_review handoff-release transaction

## Summary

Implemented the config guard requested by SPEC-0067:

- Added `event_state_config_error(config)` in `runtime/protocol_replay.py`.
- The guard applies to `adoption_tier=runtime` and enforces the monotonic chain:
  `authoritative => enforce => materialize => enabled`.
- `coordination` tier remains no-op for this guard, matching SPEC-0067 "no aplica".
- Wired Python validator hard-fail through `scripts/validate_collaboration_state.py`.
- Wired PowerShell validator parity through `scripts/validate_collaboration_state.ps1`.
- Wired `runtime/submit_intent.py` to reject incoherent configs before applying single-intent or transaction writes.
- Wired `runtime/apply.py` to reject incoherent configs before applying turns.
- Added golden coverage for validator, submit_intent, and apply rejection of
  `authoritative=true` with `enforce=false`, plus coherent-chain allow cases.
- Kept `protocol.config.template.json` untouched; the live config with all flags true still validates.

## Anomaly Detected And Fixed

While making old B.3 enforce tests coherent with the new chain, I found that `apply_gate_and_commit`
materialized from the event log before checking drift. With `materialize=true`, that could hide a
pre-existing manual divergence before the enforce gate saw it.

Fix included in this task:

- `apply_gate_and_commit` now runs `enforce_protocol_state_drift(root)` before applying the turn.
- It still runs the drift gate after materialization as before.
- The B.3 golden now passes with coherent `enabled=true/materialize=true/enforce=true`.

## Changed Paths

- `runtime/protocol_replay.py`
- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `runtime/submit_intent.py`
- `runtime/apply.py`
- `examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py`
- `examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py`
- `Area_comun/handoffs/HANDOFF-TASK-0086-codex-to-claude-1.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0086-in-review.md`

## Validation Evidence

```text
python -m py_compile runtime\protocol_replay.py runtime\submit_intent.py runtime\apply.py scripts\validate_collaboration_state.py examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py -> OK
python examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py -> OK: 9
python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py -> OK: 6
python examples\intent_flow_cases\run_intent_flow_cases.py -> OK: 11
python examples\intent_tx_cases\run_intent_tx_cases.py -> OK: 6
python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py -> OK: 6
python examples\runtime_protocol_genesis_ref_cases\run_runtime_protocol_genesis_ref_cases.py -> OK: 9
python examples\runtime_apply_cases\run_runtime_apply_cases.py -> OK: 4
python examples\runtime_prune_cases\run_runtime_prune_cases.py -> OK
python examples\materialize_cross_fs_cases\run_materialize_cross_fs_cases.py -> OK: 2
python examples\cutover_loop_cases\run_cutover_loop_cases.py -> OK: 4
python scripts\validate_collaboration_state.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root . -> OK
python scripts\scan_encoding.py --root . -> OK
python scripts\scan_domain_neutrality.py --root . -> exit 0
python scripts\prune_state.py --root . --check -> OK: prune not due
runtime protocol_state_drift -> has_drift=false
```

## Review Notes

- The guard intentionally returns no error for `coordination` tier, even if runtime-only flags are present,
  because SPEC-0067 asks for coordination-tier to be "no aplica".
- The removed B.2 assertion was the incoherent off case `enabled=false/materialize=true`; coherent off remains
  covered by `enabled=false/materialize=false`.
- Final handoff-release will advance runtime event sequence after this file is written; use the event log as
  authoritative for final sequence numbers.
