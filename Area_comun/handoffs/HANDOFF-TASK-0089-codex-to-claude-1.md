# HANDOFF TASK-0089 - Codex to Claude

Date: 2026-06-08
Owner: Codex
Status: ready for in_review handoff-release transaction

## Summary

Implemented the off-pilot vendor-neutral LLM turn wrapper:

- Added `runtime/llm_turn_wrapper.py`.
- The wrapper reads the prompt from stdin and invokes a configurable backend from `--backend` or
  `LLM_TURN_WRAPPER_BACKEND`.
- Default backend timeout is 100s, below the 120s `SubprocessInvoker` timeout; explicit timeouts must be below 120s.
- Backend stdout is normalized from clean JSON, fenced/prose JSON, or `{ "report": { ... } }`.
- The extracted report is validated against `runtime/turn_schema.json`.
- Success emits only the clean report JSON to stdout and exits 0.
- Failure modes emit no stdout, return non-zero, and write diagnostics to stderr.
- `runtime.llm_cli_presets.claude.command` now points to the wrapper with backend `claude -p`.
- `runtime.real_invoker.enabled` and `runtime.supervised_autonomy.enabled` remain `false`; no pilot or real smoke was run.

## Changed Paths

- `runtime/llm_turn_wrapper.py`
- `examples/llm_turn_wrapper_cases/`
- `protocol.config.json`
- `.github/workflows/validate.yml`
- `Area_comun/handoffs/HANDOFF-TASK-0089-codex-to-claude-1.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0089-in-review.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0089-GO-llm-wrapper.md`
- Runtime-authoritative ledger files updated via `submit_intent` / `prune_state.py`.

## Golden Coverage

`examples/llm_turn_wrapper_cases/` uses a deterministic local fake backend and covers:

- clean valid JSON
- fenced JSON with prose around it
- `{ "report": { ... } }`
- backend configured through environment variable
- schema-invalid report
- backend non-zero exit
- backend timeout before the invoker timeout
- live preset points to the wrapper while SA.4 remains off-pilot

CI now runs the wrapper golden directly with Python and through the PowerShell shim.

## Validation Evidence

```text
python examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py -> OK: 8
powershell -NoProfile -ExecutionPolicy Bypass -File examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.ps1 -> OK: 8
python examples\llm_adapter_cases\run_llm_adapter_cases.py -> OK: 6
python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py -> OK: 4
python scripts\validate_collaboration_state.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root . -> OK
python scripts\scan_domain_neutrality.py --root . -> exit 0
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root . -> exit 0
python scripts\scan_encoding.py --root . -> OK
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root . -> OK
python scripts\prune_state.py --root . --check -> OK: prune not due
runtime protocol_state_drift -> has_drift=false, up_to_seq=110 before handoff-release
```

## Review Notes

- This does not hardcode a vendor in the wrapper; the live `claude` preset supplies one backend command.
- No secrets, no network, and no real LLM invocation were used in the golden.
- The wrapper emits the unwrapped report object, which `SubprocessInvoker` already accepts.
- A maintenance prune was due at turn start and was applied by `prune_state.py --apply` in submit_intent mode before
  claiming TASK-0089; drift stayed false.
- Final handoff-release will advance the runtime event sequence after this file is written.
