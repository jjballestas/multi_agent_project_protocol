# HANDOFF TASK-0096 - Codex to Claude

Date: 2026-06-15
Owner: Codex
Status: in_review

## Summary

Implemented unique run-log protection for real subprocess invoker runs. Real invoker runs now require an
explicit fresh `--run-id`; reusing an existing run log is rejected before the invoker runs, preventing JSONL
append accumulation and cross-run metrics aggregation.

## Changed

- `runtime/orchestrator.py`:
  - Added `real_invoker_run_id_error`.
  - Requires `--run-id` for `--llm-invoker subprocess`.
  - Rejects a subprocess run if `runtime/runs/<run_id>.jsonl` already exists.
  - Replay/recorded deterministic defaults remain unchanged.
- `examples/runtime_real_adapter_cases/run_runtime_real_adapter_cases.py`:
  - Existing subprocess tests pass explicit run IDs.
  - Added coverage for missing `--run-id` and existing run-log rejection.
- `examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py`:
  - Added a two-run real subprocess regression: consecutive runs use distinct run logs, each reports
    `turns_total == 1`, and each JSONL has one entry.
- `examples/llm_adapter_cases/run_llm_adapter_cases.py`:
  - Updated native subprocess golden to pass explicit `--run-id`.

## Evidence

- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> OK, 6 cases.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 5 cases.
- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK, 10 cases.
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> OK, 15 cases.
- `python examples\runtime_budget_cases\run_runtime_budget_cases.py` -> OK, 5 cases.
- `python examples\runtime_observability_cases\run_runtime_observability_cases.py` -> OK, 5 cases.
- `python examples\runtime_cost_attribution_cases\run_runtime_cost_attribution_cases.py` -> OK, 11 cases.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- Runtime drift check -> `has_drift:false`, up_to_seq 522 at the time of the check.

## Notes for review

- No Date.now/random equivalent was introduced.
- No gate or claim semantics changed.
- Deterministic replay/recorded runs still use the existing replay-input hash default when `--run-id` is
  omitted.
