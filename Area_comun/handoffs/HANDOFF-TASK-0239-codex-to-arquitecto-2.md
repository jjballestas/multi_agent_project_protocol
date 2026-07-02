# HANDOFF TASK-0239 - actor remediation

From: Codex
To: Arquitecto
Task: TASK-0239
Status: in_review
Commit: bc9cc8d84927f32837cdfc9ee5cdc301f6115aaa

## Summary

Remediated F-0239-01. `runtime/submit_intent.py` now rejects `exception` intents whose payload
`actor` differs from the signed caller `actor_id`, including batched `submit_intents`.

## Changed

- Added `ensure_exception_actor_matches_caller`.
- Applied it before idempotency keys and before event emission for single and transaction submits.
- Added permanent negative coverage: `test_rejects_actor_mismatch`.

## Evidence

- Clean clone at commit `bc9cc8d84927f32837cdfc9ee5cdc301f6115aaa`.
- `python scripts/test_exception_recorded.py` PASS, 6 tests.
- `python scripts/test_intake_gate.py` PASS, 12 tests.
- `python -m py_compile runtime/submit_intent.py scripts/test_exception_recorded.py` PASS.
- `python scripts/scan_encoding.py --root .` PASS.
- `python scripts/scan_domain_neutrality.py --root .` PASS.
- `python scripts/validate_collaboration_state.py --root .` PASS.
- `protocol_state_drift(Path('.'))` PASS: `has_drift=false`, `up_to_seq=3311`.
- `protocol.config.json` SHA256 remains `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

## Notes

Product repo `D:/Agentes/Zeus/Zeus-protocol` was clean and untouched; TASK-0239 is protocol runtime work.
