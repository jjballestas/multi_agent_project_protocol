---
handoff_id: HANDOFF-TASK-0281-codex-to-arquitecto
task_id: TASK-0281
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-21
implementation_commit: 7b708f8
iteration: 2
---

# TASK-0281 iteration 2 handoff

## Result

The generic born-operational peer runner implements all requested structural repairs:

- own evidence requires the pre-exec event-log prefix to retain the same SHA-256;
  any rewrite, compaction, restoration, or reordering makes evidence unavailable;
- the residue gate always reads NUL-delimited porcelain, so spaces and non-ASCII
  path bytes are never quote-parsed, and the probe is inside the lock cleanup path;
- pre-exec defers have a separate watchdog counter, consume zero agent attempts,
  never set the message as exhausted, and remain eligible after the veto clears.

The previous orphan-lock and bounded watchdog behavior remains intact. The live
Codex and Analista harnesses were not redeployed.

## Permanent controls

`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` proves:

- a real pure append with a new signed own event is accepted;
- a longer rewrite containing historical own evidence and a shorter rewrite are
  rejected; the length-only control mutant is demonstrably green for the longer
  rewrite and therefore killed by the repaired assertion;
- fresh paths containing a space and a non-ASCII byte both return `live` without
  `LOOP_ERROR`;
- three environmental defers emit the watchdog signal with `attempts=0` and
  `exhausted=false`, then the unchanged message runs and is consumed when the
  dirty precondition disappears.

## Verification by exit code

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> 0
- `python scripts/test_anthropic_checker_harness.py` -> 0
- `python scripts/test_exec_lease_harness.py` -> 0
- `python scripts/validate_collaboration_state.py` -> 0
- `python scripts/scan_encoding.py` -> 0
- `python scripts/scan_domain_neutrality.py` -> 0
- runtime drift -> false at seq 5546

Codex is maker only and did not review or ratify this delivery. Route commit
`7b708f8` to Analista for independent iteration-2 judgement.
