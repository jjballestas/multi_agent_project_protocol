---
handoff_id: HANDOFF-TASK-0306-codex-to-arquitecto
task_id: TASK-0306
from: Codex
to: Arquitecto
status: ready_for_review
implementation_commit: 18c175f591b04cb2cf2d943973f1d8ca6c5d0ef3
created_at: 2026-07-30
---

# HANDOFF TASK-0306 - signed checkpoint and incremental live replay

## Delivered

- `runtime/state/snapshot.json` now receives `integrity`, an HMAC-SHA256 made
  with the existing runtime instance key (`runtime-hmac:v1`) over
  `canonical_hash`, `up_to_seq`, and the `prev_hash` of the event at that
  sequence.
- `verify_snapshot_checkpoint` verifies signature, key id, state hash,
  checkpoint metadata, event boundary, head range, and freshness before
  returning a replay base.
- `EventWriter.state()` verifies only events newer than a trusted checkpoint.
  Every invalid/unavailable checkpoint condition returns to the pre-existing
  full replay path.
- `runtime/CHECKPOINT_POLICY.json` is a tracked registry outside the pinned
  protocol config and sets `max_incremental_events` to 128.

## Security evidence

- The executable test corrupts the integrity signature, mutates checkpoint
  state without re-signing, and makes the checkpoint stale. Each case verifies
  every event through the full path.
- The differential compares canonical state and snapshot fields from
  incremental and full replay byte-for-byte.
- The offline `validate_chain` test mutates an old event that the live
  checkpoint would trust and still obtains `valid: false`.
- No config, genesis, event-chain rule, or compacting behavior changed.

## Measurement

Read-only measurement on the live log at implementation time:

- events present: 6,125
- full event-auth verifications: 6,125; 4.1455 seconds
- current-checkpoint event-auth verifications: 0; 0.1078 seconds
- with one event after the checkpoint, the executable test observes exactly
  one event-auth verification.

## Recompute

```text
python -m py_compile runtime/eventlog.py examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py
python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py
python examples/runtime_event_auth_cases/run_runtime_event_auth_cases.py
python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py
python scripts/validate_collaboration_state.py
python scripts/scan_encoding.py
python scripts/scan_domain_neutrality.py
git diff --check
```

Expected: all exit 0. The runtime eventlog suite reports six passing cases.
Maker Codex requests Arquitecto recomputation and independent Analista review,
with emphasis on fail-safe fallback and the unchanged offline full-chain gate.
