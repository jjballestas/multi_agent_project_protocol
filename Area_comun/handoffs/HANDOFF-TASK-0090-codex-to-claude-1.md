# HANDOFF TASK-0090 - Codex to Claude

Date: 2026-06-09
Owner: Codex
Status: ready for in_review handoff-release transaction

## Summary

Implemented the cross-platform backend resolution fix for the LLM turn wrapper:

- Added `resolve_backend_command(...)` in `runtime/llm_turn_wrapper.py`.
- `run_backend(...)` now resolves `command[0]` with `shutil.which` before `subprocess.run`.
- If `shutil.which` finds a backend shim/path, the resolved executable is used with the original args.
- If the backend is not found, behavior stays clean: `OSError` is caught and the wrapper exits non-zero with stderr.
- Timeout, extraction, schema validation, and clean stdout behavior are unchanged.
- SA.4 remains off-pilot: `runtime.real_invoker.enabled=false` and `runtime.supervised_autonomy.enabled=false`.
- No real smoke, no pilot, no network, and no secrets.

## Changed Paths

- `runtime/llm_turn_wrapper.py`
- `examples/llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.py`
- `Area_comun/handoffs/HANDOFF-TASK-0090-codex-to-claude-1.md`
- `Area_comun/mailbox/open/MSG-20260609-Codex-to-Claude-task0090-in-review.md`
- `Area_comun/mailbox/archived/MSG-20260609-Claude-to-Codex-task0090-GO-wrapper-resolution.md`
- Runtime-authoritative ledger files updated via `submit_intent` / `prune_state.py`.

## Golden Coverage

`examples/llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.py` now has 10 cases:

- original wrapper cases remain green
- `case_backend_resolved_by_shutil_which` verifies a command name resolved by `shutil.which` runs successfully
- `case_backend_missing_fails_cleanly` verifies an absent backend exits non-zero with no stdout and a clean stderr

The PowerShell shim runs the same Python golden, so CI parity is preserved without adding a separate workflow step.

## Validation Evidence

```text
python -m py_compile runtime\llm_turn_wrapper.py examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py -> OK
python examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py -> OK: 10
powershell -NoProfile -ExecutionPolicy Bypass -File examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.ps1 -> OK: 10
python examples\llm_adapter_cases\run_llm_adapter_cases.py -> OK: 6
python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py -> OK: 4
python scripts\validate_collaboration_state.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root . -> OK
python scripts\scan_encoding.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root . -> OK
python scripts\scan_domain_neutrality.py --root . -> exit 0
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root . -> exit 0
python scripts\prune_state.py --root . --check -> OK: prune not due
runtime protocol_state_drift -> has_drift=false, up_to_seq=131 before handoff-release
```

## Review Notes

- The golden does not hardcode `claude`; it patches `shutil.which` to resolve a fake command name to the current
  Python executable and then runs the existing deterministic fake backend.
- This targets the characterized Windows shim issue while preserving the previous clean-failure path.
- A maintenance prune was due at turn start and was applied by `prune_state.py --apply` before claiming TASK-0090;
  drift stayed false.
- Final handoff-release will advance the runtime event sequence after this file is written.
