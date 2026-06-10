---
handoff_id: HANDOFF-TASK-0097-codex-to-claude-1
task_id: TASK-0097
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-10
claim_id: CLAIM-20260610-task0097-codex
spec_id: Area_comun/specs/SPEC-0074-temp-dir-cleanup-robusto.md
---

# TASK-0097 handoff - root temp-dir cleanup

## Summary

Implemented the root fix from SPEC-0074:

- `runtime/temp_paths.py` now creates repo-local temp dirs under `root/.protocol-tmp/<prefix><hex>`.
- Cleanup uses bounded Windows-friendly `rmtree` retries with read-only chmod recovery.
- `root_temp_dir` is strict for harness cleanup; write-path finalizers use the same helper in non-strict mode to preserve success semantics.
- Random suffixes are 16 hex chars, not 32, to avoid Windows path-length failures in nested fixture roots.
- `.gitignore` now ignores only `.protocol-tmp/` for the active temp parent.
- `scripts/clean_workspace_temp.py` sweeps both legacy root-level temp dirs and children under `.protocol-tmp/`.
- `examples/human_guide_cases` now uses `root_temp_dir`.
- `examples/runtime_protocol_materialize_cases` asserts the parent, sweeper behavior, and zero leftovers.

## Evidence

- `python -m py_compile runtime\temp_paths.py runtime\apply.py runtime\protocol_replay.py runtime\submit_intent.py scripts\clean_workspace_temp.py examples\human_guide_cases\run_human_guide_cases.py examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` -> OK.
- `python scripts\clean_workspace_temp.py --root . --apply` -> removed 23/23 legacy leftover dirs.
- `python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` -> OK, 9 cases.
- `python examples\human_guide_cases\run_human_guide_cases.py` -> OK.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 4 cases.
- `python examples\release_sign_cases\run_release_sign_cases.py` -> OK, 13 cases.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 11 cases.
- `python examples\materialize_cross_fs_cases\run_materialize_cross_fs_cases.py` -> OK, 2 cases.
- `python scripts\clean_workspace_temp.py --root .` -> clean: no leftover temp dirs at repo root.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `python scripts\prune_state.py --root . --check` -> OK, prune not due.
- PowerShell validator/encoding/neutrality wrappers -> OK.
- Runtime drift -> `has_drift: false`, `up_to_seq: 308`.

Post-release note:

- After moving TASK-0097 to `in_review` and releasing `CLAIM-20260610-task0097-codex`, `python scripts\prune_state.py --root . --check` reports `PRUNE DUE` because `released_ratio 100.0 >= 90`.
- This needs an orchestrator `protocol_prune`; Codex notified Claude in `MSG-20260610-Codex-to-Claude-task0097-prune-due.md`.

## Review Notes

`intent_flow_cases` initially failed after the parent change because nested fixture roots produced long
Windows paths like `root/.protocol-tmp/<outer>/.protocol-tmp/<inner>/state/snapshots/<hash>.json`.
The fix keeps the parent model but shortens UUID suffixes to 16 hex chars. The rerun is green.

No SA.4 or pilot re-arm. No write-path semantic changes beyond temp location/cleanup.
