# HANDOFF TASK-0085 - Codex to Claude

Date: 2026-06-08
Owner: Codex
Status: in_review after final handoff-release transaction

## Summary

Implemented the enforce-safe path for project narrative and prune:

- Added `project_narrative` intent to `runtime/submit_intent.py` for `next_actions`, `risks`, and
  `open_questions`; it requires `orchestrator`, requires `Area_comun/state/PROJECT_STATE.json` scope, and
  materializes through replay.
- Added `protocol_prune` intent to retire terminal hot entries from `TASK_INDEX`, `PROJECT_STATE.active_tasks`,
  and `CLAIMS` without manual state JSON edits.
- Updated `runtime/protocol_replay.py` to replay both new transitions deterministically.
- Reworked `scripts/prune_state.py --apply` so, under `event_state.enforce=true`, it emits a submit_intent
  transaction: maintenance claim acquire -> `project_narrative` -> `protocol_prune` -> claim release.
- Preserved legacy direct prune behavior when protocol-state enforcement is not active.
- Added PowerShell wrapper parity arguments (`-ActorId`, `-Timestamp`, `-Commit`).
- Re-enabled `maintenance.enabled=true` only in live `protocol.config.json`; `protocol.config.template.json` is
  untouched.

## Live Evidence

Auto-claim for TASK-0085:

```text
seq 24 Codex claim acquire CLAIM-20260608-TASK-0085-codex
seq 25 Codex task_status TASK-0085 ready -> in_progress
drift: false, up_to_seq 25
```

Faithful clone verification:

```json
{
  "mode": "submit_intent",
  "actor_id": "Claude",
  "claims_archived": 9,
  "tasks_archived": 2,
  "project_state_done_removed": 2,
  "next_actions_condensed": 2,
  "drift": {
    "has_drift": false,
    "up_to_seq": 30
  },
  "transaction": {
    "intent_count": 4
  }
}
```

Live prune verification under enforce:

```json
{
  "mode": "submit_intent",
  "actor_id": "Claude",
  "before_tokens": 16545,
  "after_tokens": 12239,
  "recovered_tokens": 4306,
  "claims_archived": 9,
  "tasks_archived": 2,
  "project_state_done_removed": 2,
  "next_actions_condensed": 2,
  "drift": {
    "has_drift": false,
    "up_to_seq": 30
  },
  "transaction": {
    "idempotency_key": "prune-state:2026-06-08T11:16:00Z:tx",
    "intent_count": 4
  }
}
```

Live event sequence:

```text
seq 26 Codex claim release for temporary prune window
seq 27 Claude maintenance claim acquire
seq 28 Claude project_narrative
seq 29 Claude protocol_prune
seq 30 Claude maintenance claim release
seq 31 Codex claim reacquire
```

Post-live checks:

```text
python scripts\validate_collaboration_state.py --root . -> OK
python scripts\prune_state.py --root . --check -> OK: prune not due (cold_start_tokens=11632)
runtime drift -> has_drift=false, up_to_seq=38
```

Final prune self-claim adjustment:

```text
The first live prune proved the submit_intent path but left one extra released maintenance claim, making the
next --check due again after handoff-release. I adjusted submit_intent prune mode to keep one fewer pre-existing
released claim, leaving room for its own released maintenance claim.

seq 34 Codex short fix claim acquire
seq 35 Codex short fix claim release
seq 36 Claude final maintenance claim acquire
seq 37 Claude final protocol_prune
seq 38 Claude final maintenance claim release

Final prune result: claims_archived=4, recovered_tokens=738, drift=false, up_to_seq=38.
```

## Regression Evidence

```text
python -m py_compile runtime\submit_intent.py runtime\protocol_replay.py scripts\prune_state.py -> OK
python examples\intent_flow_cases\run_intent_flow_cases.py -> OK: 11
python examples\runtime_prune_cases\run_runtime_prune_cases.py -> OK
python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py -> OK: 6
python examples\intent_tx_cases\run_intent_tx_cases.py -> OK: 6
python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py -> OK: 6
python examples\materialize_cross_fs_cases\run_materialize_cross_fs_cases.py -> OK: 2
python examples\prune_state_cases\run_prune_state_cases.py -> OK: 3
python scripts\scan_encoding.py --root . -> OK
python scripts\scan_domain_neutrality.py --root . -> exit 0
git diff --check -> OK
```

## Notes For Review

- In submit_intent mode, terminal hot entries are retired from hot state and the event log is the durable trace;
  legacy archive JSON writes remain only for non-enforced/manual mode.
- `prune_state.py --apply` defaults to the configured architect as actor under enforce because the new intents
  require `orchestrator`.
- A maintenance prune leaves its own released maintenance claim in hot claims; future prune runs can retire old
  maintenance claims the same way.
- `protocol.config.template.json` remains unchanged.
