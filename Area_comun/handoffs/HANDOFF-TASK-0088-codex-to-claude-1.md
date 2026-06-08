# HANDOFF TASK-0088 - Codex to Claude

Date: 2026-06-08
Owner: Codex
Status: ready for in_review handoff-release transaction

## Summary

Implemented SA.4 step 1 lock-lift, off by default:

- Added `subprocess_multiturn_allowed(...)` in `runtime/orchestrator.py`.
- `llm/subprocess` multi-turn remains rejected with the same message unless all four gates are true:
  `--allow-real-invoker`, `--allow-supervised-autonomy`,
  `real_invoker_activation_error(config) is None`, and
  `supervised_autonomy_activation_error(config) is None`.
- When the gates are valid, subprocess multi-turn gets deterministic `None` turn slots up to `--max-iter` or
  `supervised_autonomy.caps.max_turns`.
- `--once` subprocess behavior stays intact.
- No live registry was populated; `protocol.config.json` and `protocol.config.template.json` were not changed.
- No pilot was run.

## Anomaly Detected And Fixed

While running adjacent regressions, `examples/runtime_loop_cases` failed in prune-hook fixtures because
`scripts/prune_state.py` now imports runtime modules after the submit_intent prune integration, but the fixture
copied only `scripts/`. I fixed the fixture to copy runtime `.py` files when it installs prune scripts.

I also corrected the initial supplemental scope after noticing the real adapter suite path is
`examples/runtime_real_adapter_cases/`, not `examples/real_adapter_cases/`; the corrected supplemental claim was
opened before any edit to that area. No file in `examples/runtime_real_adapter_cases/` needed changes.

## Changed Paths

- `runtime/orchestrator.py`
- `examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py`
- `examples/runtime_loop_cases/run_runtime_loop_cases.py`
- `Area_comun/handoffs/HANDOFF-TASK-0088-codex-to-claude-1.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0088-in-review.md`

## Validation Evidence

```text
python -m py_compile runtime\orchestrator.py examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py examples\runtime_loop_cases\run_runtime_loop_cases.py -> OK
python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py -> OK: 9
python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py -> OK: 4
python examples\llm_adapter_cases\run_llm_adapter_cases.py -> OK: 6
python examples\runtime_loop_cases\run_runtime_loop_cases.py -> OK: 8
python examples\runtime_budget_cases\run_runtime_budget_cases.py -> OK: 5
python examples\runtime_apply_cases\run_runtime_apply_cases.py -> OK: 4
python scripts\validate_collaboration_state.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root . -> OK
python scripts\scan_encoding.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root . -> OK
python scripts\scan_domain_neutrality.py --root . -> exit 0
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root . -> exit 0
python scripts\prune_state.py --root . --check -> OK: prune not due
runtime protocol_state_drift -> has_drift=false, up_to_seq=86 before handoff-release
```

## Review Notes

- The new golden uses a local deterministic subprocess agent; it does not call a real LLM or network.
- The live config remains off for `runtime.real_invoker` and `runtime.supervised_autonomy`; this only lifts the
  code lock when a later micro-GO supplies valid registrations and both CLI allow flags.
- The old rejection string `subprocess llm invoker requires --once` is preserved for off/incomplete registration.
- Final handoff-release will advance runtime event sequence after this file is written; use the event log as
  authoritative for final sequence numbers.
