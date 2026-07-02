---
handoff_id: HANDOFF-TASK-0238-codex-to-arquitecto-1
task_id: TASK-0238
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-02
requires_response: false
---

# TASK-0238 handoff - F1-A deterministic intake gate

## Summary
Implemented the post-boundary intake gate for tasks after `TASK-0238`.

## Changed Paths
- `Area_comun/protocol/INTAKE_GATE.json`
- `Area_comun/protocol/TASK_TEMPLATE.md`
- `examples/minimal_instance/protocol.config.json`
- `examples/minimal_instance/Area_comun/protocol/TASK_TEMPLATE.md`
- `protocol.config.template.json`
- `runtime/submit_intent.py`
- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `scripts/test_intake_gate.py`

## Behavior
- R0 is recorded outside pinned `protocol.config.json` in `Area_comun/protocol/INTAKE_GATE.json`.
- R1-R5 are enforced by both validators only for numeric `TASK-XXXX` ids greater than `TASK-0238`.
- `runtime/submit_intent.py` rejects `proposed -> ready` for post-boundary tasks with missing or invalid intake before applying the transaction.
- Templates now show the required `intake` block.
- `examples/minimal_instance` validates with the gate active.

## Evidence
- `python -m unittest scripts.test_intake_gate` PASS, 11 tests.
- `python -m py_compile scripts\validate_collaboration_state.py runtime\submit_intent.py scripts\test_intake_gate.py` PASS.
- PowerShell parser check for `scripts\validate_collaboration_state.ps1` PASS.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS with pre-existing mailbox hygiene warning only.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` PASS with same warning.
- Drift check PASS: `has_drift=false`, `up_to_seq=3263` before delivery close.
- Clean clone gates PASS for encoding, neutrality, validator, and `python -m unittest scripts.test_intake_gate`.

## Commits
- `0efe196 feat(intake): enforce deterministic ready gate`

## Notes
- Product repo `D:/Agentes/Zeus/Zeus-protocol` was clean and untouched; TASK-0238 is protocol infrastructure.
- `protocol.config.json` was not changed, preserving the pinned genesis-bound config.
