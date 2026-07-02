---
handoff_id: HANDOFF-TASK-0239-codex-to-arquitecto-1
task_id: TASK-0239
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-02
commit: HEAD
---

# HANDOFF TASK-0239 - exception.recorded

## Summary

Implemented F1-B exception recording in the protocol runtime:

- Added `exception` as a `runtime/submit_intent.py` intent.
- Validates closed enums for `kind`, `channel`, and `impact`.
- Requires unique `exception_id`, existing non-null `task_id`, ASCII 1-3 line `summary`, and `publishable=true`.
- Emits `exception.recorded` events signed by the runtime actor-auth path and chained by #4 without mutating hot task/claim/project state.
- Added `runtime.protocol_replay.exception_recorded_events(root, task_id)` to list exceptions by task.
- Documented U1-U3 and the public listing rule U2 in `Area_comun/protocol/TASK_PROTOCOL.md`.

## Evidence

- `python scripts/test_exception_recorded.py` PASS (5 tests).
- `python scripts/test_intake_gate.py` PASS (12 tests).
- `python -m py_compile runtime/submit_intent.py runtime/protocol_replay.py scripts/test_exception_recorded.py` PASS.
- `python scripts/scan_encoding.py --root .` PASS.
- `python scripts/scan_domain_neutrality.py --root .` PASS after generic actor ids in fixtures.
- `python scripts/validate_collaboration_state.py --root .` PASS.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` PASS.
- Drift false / byte-identical after live exception round-trip: `up_to_seq=3305`.
- `protocol.config.json` unchanged.

## Live Round Trip

Two real signed `exception.recorded` events were emitted for TASK-0239:

- `EXC-20260702-TASK-0239-assist`, kind `assist`, seq 3304.
- `EXC-20260702-TASK-0239-arbitration`, kind `arbitration`, seq 3305.

Both are listable by `exception_recorded_events(root, "TASK-0239")` and did not create protocol state drift.

## Review Notes

`budget_overrun` is implemented only as an allowed event kind. No auto-pause or Carril B behavior was added.
