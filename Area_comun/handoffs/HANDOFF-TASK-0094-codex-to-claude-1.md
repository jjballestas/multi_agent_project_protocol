---
handoff_id: HANDOFF-TASK-0094-codex-to-claude-1
task_id: TASK-0094
from: Codex
to: Claude
status: open
created_at: 2026-06-09
claim_id: CLAIM-20260609-task0094-codex
---

# HANDOFF TASK-0094 - tempfile/ACL write-path hardening

## Summary

Formalized the Windows sandbox tempfile/ACL hardening under TASK-0094/SPEC-0071. The authoritative
write-path no longer creates materialization staging or runtime rollback backups with OS temp helpers
that can produce `0o700` ACLs under `%TEMP%`.

Posture B is applied: `AGENTS.md` was reverted to remove the temp-ACL rule from the contract, and the
rule now lives in `Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md`.

## Changed Paths

- `runtime/temp_paths.py`
- `runtime/protocol_replay.py`
- `runtime/submit_intent.py`
- `runtime/apply.py`
- `examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py`
- `examples/materialize_cross_fs_cases/run_materialize_cross_fs_cases.py`
- `examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py`
- `examples/intent_flow_cases/run_intent_flow_cases.py`
- `examples/runtime_real_adapter_cases/run_runtime_real_adapter_cases.py`
- `Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md`

## Evidence

- `python -m py_compile runtime\temp_paths.py runtime\protocol_replay.py runtime\submit_intent.py runtime\apply.py`
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK, 6 cases.
- `python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` -> OK, 7 cases.
- `python examples\materialize_cross_fs_cases\run_materialize_cross_fs_cases.py` -> OK, 2 cases.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 11 cases.
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> OK, 15 cases.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 4 cases.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- Drift check -> `has_drift=false`, `up_to_seq=207` before release.

## Notes For Review

- `materialize_to_disk()` still stages under the repo root to preserve same-filesystem atomic rename.
- `root_temp_dir()` / `make_root_temp_dir()` create repo-local paths with inherited ACLs and cleanup via
  `shutil.rmtree`.
- The materialization golden asserts the returned `canonical_hash` matches the expected materialized
  document hash.
- Regression harnesses requested by the GO now avoid direct `%TEMP%` fixtures where they must pass in
  Codex sandbox.
- No SA.4 re-arm and no pilot run.

## Not Included

The TASK-0093 v2 worktree changes are intentionally not part of this handoff or commit:

- `runtime/orchestrator.py`
- `examples/runtime_loop_cases/run_runtime_loop_cases.py`
- `Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-2.md`
