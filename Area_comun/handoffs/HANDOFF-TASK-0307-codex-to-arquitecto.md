---
handoff_id: HANDOFF-TASK-0307-codex-to-arquitecto
task_id: TASK-0307
from: Codex
to: Arquitecto
status: ready_for_review
implementation_commit: 98b887a0218aed391f134138f966bab60983b2bd
created_at: 2026-07-30
---

# HANDOFF TASK-0307 - checkpoint-bound physical event-log compaction

## Delivered

- `EventWriter.write_snapshot()` compacts the hot log after a signed checkpoint
  when `compaction_threshold` is exceeded.
- `compact_through(up_to_seq)` moves the complete prefix to
  `runtime/state/archives/events-<lo>-<hi>.jsonl`, writes a SHA-256 sidecar, and
  leaves only events above the checkpoint boundary in `events.jsonl`.
- `events_in_log_order()` continues to return archives plus the hot tail. The
  live checkpoint path verifies only the hot tail after validating archive
  integrity; the offline gate receives and audits the complete union.
- Non-numeric checkpoint sequence and policy limits return an untrusted
  checkpoint and full replay instead of raising.

## Critical safety evidence

- The differential captures ordered events and canonical state before
  compaction, compacts, and requires both outputs to remain identical.
- A post-compaction live replay records exactly the one hot-tail event passed
  through event-auth verification and remains byte-identical to full replay.
- Mutating an archived event makes its SHA-256 sidecar mismatch. The live path
  then verifies the complete union. The offline chain gate also rejects the
  mutation.
- Recomputing the sidecar over the corrupt archive does not hide the mutation:
  offline full-chain validation still rejects it.
- Malformed `up_to_seq` and `max_incremental_events` values produce explicit
  untrusted verdicts without an exception.

## Scope exclusions

- `protocol.config.json` is byte-identical.
- No genesis, chain rule, trust model, or product repository changed.
- Events are moved, never deleted: archives plus hot log remain the complete
  ordered ledger.

## Recompute

```text
python -m py_compile runtime/eventlog.py examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py
python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py
python scripts/validate_collaboration_state.py
python scripts/scan_encoding.py
python scripts/scan_domain_neutrality.py
git diff --check
git diff --exit-code 2fd10a6 -- protocol.config.json
```

Expected: all commands exit 0 and the runtime event-log suite reports seven
passing cases. Codex requests Arquitecto recomputation and independent Analista
review focused on zero loss/duplication and archived-event fail-safe behavior.
