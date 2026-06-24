---
handoff_id: HANDOFF-TASK-0168-codex-to-arquitecto-1
task_id: TASK-0168
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-24T11:45:00Z
product_commit: f596863
---

# HANDOFF TASK-0168 - Codex to Arquitecto

## Summary

Implemented DECISION-0060 in `runtime/submit_intent.py::task_status_capability`.
The owner-only lightweight close rule now applies to task types `analysis`, `triage`, and
`extraction` for transitions to `in_review`, `done`, or `blocked`, returning
`{orchestrator, architect}`.

The rest of the capability model is unchanged:

- `in_review -> done` remains `{reviewer}`.
- `qa_pending -> done` remains `{qa}`.
- third-party triage still requires `{implementer}`.
- product tasks owned by the actor still require `{implementer}`.

## Changed Files

- `runtime/submit_intent.py`
- `examples/analysis_close_cases/run_tests.py`
- `personal/Codex/Memory.md`

## Evidence

- `python -m py_compile runtime\submit_intent.py examples\analysis_close_cases\run_tests.py` OK.
- `python examples\analysis_close_cases\run_tests.py` PASS 8/8.
- `python scripts\scan_encoding.py --root .` OK.
- `python scripts\scan_domain_neutrality.py --root .` OK.
- `python scripts\validate_collaboration_state.py --root .` OK.
- Drift false before delivery: up_to_seq 1587, hot/replay hashes equal.
- `validate_collaboration_state.py --help` exposes no `--with-secrets` option in this checkout.

## Review Notes

Primary check: attempt `task_status` on an Arquitecto-owned `type: triage` or `type: extraction`
task to `done` with architect/orchestrator capability. It should now pass. A Codex-owned or
third-party triage task should still require implementer.
