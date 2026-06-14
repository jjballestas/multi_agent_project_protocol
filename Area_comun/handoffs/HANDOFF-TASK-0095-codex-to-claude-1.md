# HANDOFF TASK-0095 - Codex to Claude

Date: 2026-06-15
Owner: Codex
Status: in_review

## Summary

Implemented self-consistent runtime turn commits for task status transitions. `apply_gate_and_commit` now
derives task markdown paths mutated by turn transitions and includes them in `commit_turn`, so the committed
snapshot keeps `TASK_INDEX` and the task `.md` aligned.

## Changed

- Added `task_file_commit_paths(root, report)` in `runtime/apply.py`.
- `apply_gate_and_commit` now includes those derived task file paths alongside explicit `changed_paths`,
  transition ledger paths, runtime state paths, and materialized protocol-state paths.
- Updated `examples/runtime_apply_cases/run_runtime_apply_cases.py` so the valid turn no longer lists the
  task `.md` in `changed_paths`; the golden asserts `git status --short -- Area_comun/tasks/TASK-9000.md`
  is clean and `HEAD:Area_comun/tasks/TASK-9000.md` contains `status: in_review`.

## Evidence

- `python examples\runtime_apply_cases\run_runtime_apply_cases.py` -> OK, 4 cases.
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> OK, 15 cases.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 4 cases.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 11 cases.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- Runtime drift check -> `has_drift:false`, up_to_seq 508 at the time of the check.

## Notes for review

- No gate or claim semantics changed.
- The helper is scoped to task IDs present in this turn's transitions. It does not include unrelated task
  files.
- No `.ps1` wrapper applies to this runtime apply path.
