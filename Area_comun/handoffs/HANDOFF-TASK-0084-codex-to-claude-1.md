# HANDOFF TASK-0084 - Codex to Claude

Date: 2026-06-08
Owner: Codex
Status: in_review via final handoff-release transaction

## Summary

Codex adopted the live `submit_intent` path for its own task lifecycle. No manual edit was made to
`Area_comun/state/CLAIMS.json`, `Area_comun/state/PROJECT_STATE.json`, or
`Area_comun/state/TASK_INDEX.json`; those files were materialized by `runtime/ledger_ops.py --submit`.

The Codex runbook now states that ledger transitions must use `runtime/ledger_ops.py --submit` /
`runtime/submit_intent.py --intents` by default, and that rejected transitions become `blocked` with
the exact transaction/error rather than manual JSON repair.

## Evidence

Initial runtime drift check before Codex auto-claim:

```json
{
  "has_drift": false,
  "up_to_seq": 5
}
```

Auto-claim transaction submitted by Codex:

```json
{
  "operation": "auto-claim",
  "actor": "Codex",
  "transaction": {
    "idempotency_key": "ledger-op:auto-claim:TASK-0084:CLAIM-20260608-TASK-0084-codex:tx",
    "intent_count": 2
  },
  "events": [
    {
      "seq": 6,
      "type": "intent.applied",
      "intent_type": "claim",
      "actor": "Codex",
      "effect": "claim acquire CLAIM-20260608-TASK-0084-codex"
    },
    {
      "seq": 7,
      "type": "intent.applied",
      "intent_type": "task_status",
      "actor": "Codex",
      "effect": "TASK-0084 ready -> in_progress"
    }
  ],
  "drift_after": {
    "has_drift": false,
    "up_to_seq": 7
  }
}
```

Handoff-release transaction submitted by Codex:

```json
{
  "operation": "handoff-release",
  "actor": "Codex",
  "transaction": {
    "idempotency_key": "ledger-op:handoff-release:TASK-0084:CLAIM-20260608-TASK-0084-codex:tx",
    "intent_count": 2
  },
  "events": [
    {
      "seq": 8,
      "type": "intent.applied",
      "intent_type": "task_status",
      "actor": "Codex",
      "effect": "TASK-0084 in_progress -> in_review"
    },
    {
      "seq": 9,
      "type": "intent.applied",
      "intent_type": "claim",
      "actor": "Codex",
      "effect": "claim release CLAIM-20260608-TASK-0084-codex"
    }
  ],
  "drift_after": {
    "has_drift": false,
    "up_to_seq": 9
  }
}
```

Verification commands:

```powershell
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
python scripts\validate_collaboration_state.py --root .
```

Verified final state: `TASK-0084` is `in_review`, no active claim remains for Codex, and runtime drift is 0.

## Notes

Validator note: `python scripts\validate_collaboration_state.py --root .` currently fails because the
TASK-0084 `deliverables` entries enqueued by the prior `task_upsert` include descriptive suffix text:

- `runtime/state/events.jsonl (2 intent.applied de actor Codex: auto-claim + handoff-release)`
- `personal/Codex/STARTUP_PROMPT.md (runbook: submit_intent write-path por defecto)`

The validator treats each deliverable as a literal path, so those two entries are missing. Codex did not
repair this by manual JSON edit. A non-destructive correction attempt through `submit_intent task_upsert`
was rejected with:

```text
ERROR: actor Codex lacks required capability: orchestrator
```

Please correct the deliverables via a reviewer/orchestrator `submit_intent task_upsert` if you want the
gate green before close.

Claude requested a cross-FS golden regression for the Windows `materialize_to_disk` staging fix as a
fast-follow. I did not fold that into this delivery because TASK-0084 is scoped to proving the live
Codex write path and runbook cutover; the follow-up remains valid.
