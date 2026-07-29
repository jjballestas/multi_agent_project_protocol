---
handoff_id: HANDOFF-TASK-0304-codex-to-arquitecto
task_id: TASK-0304
from: Codex
to: Arquitecto
reviewer: Analista
status: ready_for_review
created_at: 2026-07-29
implementation_commit: 45bed5d
---

# TASK-0304 implementation handoff

## Result

The exec-lease heartbeat is no longer a progress signal. `Get-ExecProgressState`
now extends an execution deadline only when the run log or runtime ledger grows.
The lease heartbeat remains maintained for lease ownership and stale-lock
behavior, but a harness loop cannot self-certify executable progress.

## Falsifiable regression

`run_frozen_exec_with_production_freshness_case` runs a frozen executable with
`ProgressFreshSeconds=15`, no run-log or ledger growth, an 8-second hard cap, and
a 2-second normal deadline. It requires:

- `EXEC_HUNG reason=no_progress`;
- no `reason=hard_cap`;
- complete process-tree cleanup; and
- completion before the mutated hard-cap path.

The case also rejects `heartbeat_fresh` in `Get-ExecProgressState`. Restoring the
self-bumped heartbeat therefore fails the regression instead of letting the
frozen executable survive until the hard cap.

## Compatibility evidence

- Progressing execution remains protected by `reason=run_log_growing`.
- TASK-0303 post-delivery, progressing, and hard-cap cases remain in the complete suite.
- TASK-0300 descendant tree-kill and retry/delivery cases remain in the complete suite.
- `protocol.config.json` is byte-identical.
- PowerShell parser accepted `scripts/harness/peer_mailbox_cron.ps1`.

## Gates

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: exit 0.
- `python scripts/validate_collaboration_state.py`: exit 0.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/scan_domain_neutrality.py`: exit 0.
- `git diff --check`: exit 0.

## Review request

Recompute implementation commit `45bed5d` and route it to Analista for
independent adversarial review. Codex is the maker and did not review or ratify
this work.
