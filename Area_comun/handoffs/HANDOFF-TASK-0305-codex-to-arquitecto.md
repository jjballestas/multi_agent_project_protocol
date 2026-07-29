---
handoff_id: HANDOFF-TASK-0305-codex-to-arquitecto
task_id: TASK-0305
from: Codex
to: Arquitecto
reviewer: Analista
status: delivered
commit: 625ab32
created_at: 2026-07-29
---

# HANDOFF TASK-0305

## Result

`submit_intent` now computes the fully verified event state once and threads it through idempotency lookup,
event append, intra-transaction state advancement, and final snapshot construction.

## Critical identity evidence

- Differential test: identical event objects and byte-identical `events.jsonl`.
- Differential test: identical snapshot object and byte-identical `snapshot.json`.
- HMAC and Ed25519 fields are therefore identical.
- `validate_chain` is green on the optimized output.
- A manipulated newly appended event is rejected.
- The second event for one aggregate observes the first event's aggregate version.

## Performance

- Before: 96.760 seconds (three full state verifications).
- After: 39.785 seconds (one full state verification).
- Speedup: 2.432x on the current 6,770-event log.

## Gates

- `python -m unittest tests.test_submit_intent_state_once -v`: PASS (2).
- `python examples/intent_tx_cases/run_intent_tx_cases.py`: PASS (12).
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: PASS.
- `python scripts/scan_encoding.py`: PASS.
- `python scripts/scan_domain_neutrality.py`: PASS.
- `python scripts/validate_collaboration_state.py`: PASS.

## Boundaries

No snapshot seeding between submits, compaction, genesis/re-genesis, chain format, verification policy, product
route, or `protocol.config.json` change. Maker Codex requests independent review; Codex does not ratify this work.
