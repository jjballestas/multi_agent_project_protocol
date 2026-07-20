---
handoff_id: HANDOFF-TASK-0280-iter3-codex-to-arquitecto
task_id: TASK-0280
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-21
implementation_commit: 4310073b2eb5aa5bfe3ac555b949a5dc46fb5b29
---

# TASK-0280 iteration 3 - conservative rollback by proof

## Result

Rollback no longer infers safety from route, change type, or event name. A signed ledger
advance preserves the complete post-exec tree and returns without reset. An unreadable event
log at any position defers mutation and leaves the retry loop alive. With no event advance,
the existing rollback executes only after stable readable-head checks prove the residue belongs
to the failed exec.

`ROLLBACK_LEDGER_PRESERVED` now requires three disk-backed checks: a stable second ledger-head
read, replay drift false, and identical SHA-256/existence/length fingerprints for every dirty
path across the verification window. Failure emits DRIFT or DEFER, never PRESERVED.

## Permanent regressions

The full mailbox loop now proves in one conservative vector that a transient exec retains:

- a signed `protocol_prune` archive row;
- a signed `decision` document;
- a signed mailbox move;
- unrelated residue created beside those signed effects.

It then inserts an unreadable line in the middle of the event log, proves the ambiguous residue
survives, proves no `LOOP_ERROR`, and proves the following cycle executes and confirms. The
existing unchanged-ledger vector still proves that demonstrably local residue is rolled back.

## Evidence

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> PASS.
- `python examples/prune_state_cases/run_prune_state_cases.py` -> PASS (7).
- `python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py` -> PASS (8).
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.

The live harness was not redeployed. Maker did not review or ratify this delivery.
