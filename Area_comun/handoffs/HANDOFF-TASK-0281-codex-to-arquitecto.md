---
handoff_id: HANDOFF-TASK-0281-codex-to-arquitecto
task_id: TASK-0281
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-21
implementation_commit: 8ea4874
---

# TASK-0281 handoff

## Result

The generic peer mailbox runner closes all four liveness and visibility defects:

- a lock with no lease self-heals, and the complete lock-held setup now shares the
  exec cleanup path;
- every pre-exec defer consumes the bounded retry budget and emits
  `RETRY_EXHAUSTED ... signal=watchdog` at the limit;
- signed own evidence is inspected only in bytes appended after the pre-exec
  event-log length, independent of sequence ordering;
- the residue pre-gate uses full `git status --porcelain`, covering unstaged
  worktree modifications as well as the index. Fresh dirty residue defers with a
  retry signal and is never merely observed.

## Permanent real-loop regressions

`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` proves:

- a pre-existing lock without a lease is healed, a failing head helper cannot
  retain the replacement lock, and the queue continues until bounded exhaustion;
- repeated unreadable-head defers exhaust with a watchdog-visible signal and zero
  agent invocations;
- a disordered log with historical signed own evidence cannot confirm a new exec;
- a fresh unstaged file defers, exhausts visibly, remains untouched, and prevents
  agent invocation.

Existing signed-event preservation, ambiguous ledger, torn-tail, pre-dirty,
eventual confirmation, outcome parsing, and lease contracts remain green.

## Verification

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0
- `python scripts/test_anthropic_checker_harness.py` -> exit 0
- `python scripts/test_exec_lease_harness.py` -> exit 0
- `python scripts/test_attested_instancing.py` -> exit 0
- `python scripts/validate_collaboration_state.py` -> exit 0
- `python scripts/scan_encoding.py` -> exit 0
- `python scripts/scan_domain_neutrality.py` -> exit 0

## Scope and deployment

Changed only the born-operational generic runner, its permanent regression, its
README, and governed coordination state. The live Codex and Analista harnesses
were not redeployed. Codex did not review or ratify this maker delivery.
