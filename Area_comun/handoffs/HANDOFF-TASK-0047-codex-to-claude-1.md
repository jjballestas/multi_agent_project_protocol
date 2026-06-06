---
task_id: TASK-0047
from: Codex
to: Claude
status: submitted
created_at: 2026-06-06
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0006, DECISION-0015]
---

# HANDOFF TASK-0047 - Runtime suites in CI

## Summary

Implemented TASK-0047 additively by updating only `.github/workflows/validate.yml`
for the product change. No `runtime/`, contract or fixture files were modified.

Added to CI:

- `Install Python test dependencies`
  - `python -m pip install jsonschema`
- Runtime suites:
  - `python examples/runtime_router_cases/run_runtime_router_cases.py`
  - `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py`
  - `python examples/runtime_review_qa_cases/run_runtime_review_qa_cases.py`
  - `python examples/agent_registry_cases/run_agent_registry_cases.py`
  - `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py`
  - `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py`
  - `python examples/runtime_apply_cases/run_runtime_apply_cases.py`
  - `python examples/runtime_loop_cases/run_runtime_loop_cases.py`
  - `python examples/runtime_observability_cases/run_runtime_observability_cases.py`
  - `python examples/llm_adapter_cases/run_llm_adapter_cases.py`

The LLM adapter suite remains the recorded-mode golden runner. The workflow does not pass
`--allow-real-invoker` and does not invoke any real LLM.

## Local verification

Runtime suites added to CI:

- `python examples/runtime_router_cases/run_runtime_router_cases.py` -> 10/10
- `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` -> 5/5
- `python examples/runtime_review_qa_cases/run_runtime_review_qa_cases.py` -> 9/9
- `python examples/agent_registry_cases/run_agent_registry_cases.py` -> 4/4
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 5/5
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 5/5
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> 4/4
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py` -> 8/8
- `python examples/runtime_observability_cases/run_runtime_observability_cases.py` -> 5/5
- `python examples/llm_adapter_cases/run_llm_adapter_cases.py` -> 6/6

Existing workflow gates verified locally:

- `python scripts/validate_collaboration_state.py --root .` -> OK
- `python scripts/validate_collaboration_state.py --root examples/minimal_instance` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root examples/minimal_instance` -> OK
- `python scripts/scan_encoding.py --root .` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .` -> OK
- `python examples/encoding_gate_cases/run_encoding_gate_cases.py` -> OK
- `python examples/handoff_release_cases/run_handoff_release_cases.py` -> OK
- `python examples/mailbox_status_cases/run_mailbox_status_cases.py` -> OK
- `python scripts/prune_state.py --root . --check` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/sdd_validation_cases/run_sdd_cases.ps1` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/compact_comms_validation_cases/run_compact_comms_cases.ps1` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1` -> OK
- `python scripts/scan_domain_neutrality.py --root .` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .` -> OK

Workflow syntax:

- Parsed `.github/workflows/validate.yml` with local PyYAML -> OK.
- `git diff --check` -> OK.

## Notes

- The only product file changed is `.github/workflows/validate.yml`.
- Coordination files changed only for claim/status/mailbox/handoff.
- This task does not start A.1 writer-vivo or Phase 5.
