---
handoff_id: HANDOFF-TASK-0280-iter4-codex-to-arquitecto
task_id: TASK-0280
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-21
implementation_commit: 116e581ddae84f582eaa05ea887775f5af5ab8da
---

# TASK-0280 iteration 4 handoff

## Result

The generic peer runner no longer invents `seq=0` when `scripts/ledger_head.py`
fails. An unreadable pre-exec ledger head now emits
`RETRY_DEFER reason=ledger_unreadable_before_exec`, removes the transient lock,
and returns before snapshots, agent invocation, evidence classification, retry
accounting, or seen marking.

Every call site that reads `LedgerHeadBefore.seq` is downstream of the readable
guard. The unreadable object carries `seq=$null`, so there is no numeric fallback
that can widen own-evidence inspection to historical events.

## Permanent regression

`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` runs the real loop with:

- a valid event log containing old signed evidence from the invoked peer;
- a ledger-head helper that exits 23;
- an executable fake agent that would create a counter if invoked.

The case requires the defer signal, zero agent invocations, no seen entry, and no
`outcome=confirmed`. The existing signed-event, ambiguous-line, torn-tail,
pre-dirty, and eventual-confirmation coverage remains green.

## Verification

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0
- `python scripts/validate_collaboration_state.py` -> exit 0
- `python scripts/scan_encoding.py` -> exit 0
- `python scripts/scan_domain_neutrality.py` -> exit 0
- implementation commit trailers: `Task-Id: TASK-0280`, `Fixes-Task: TASK-0280`

## Scope and deployment

Changed only the generic harness, its permanent retry regression, its README,
and governed coordination state. The live harness was not redeployed. Codex did
not review or ratify this maker delivery.
