---
handoff_id: HANDOFF-TASK-0282-codex-to-arquitecto
task_id: TASK-0282
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-22
implementation_commit: 2d35cf0
---

# TASK-0282 implementation handoff

The generic peer mailbox harness now performs non-destructive transient cleanup:

- It restores the pre-exec index first with `git read-tree <captured-head>` followed by
  exit-gated `git apply --cached`.
- It contains no `git reset --hard`, worktree snapshot, or worktree patch replay.
- It exit-gates both pre-exec and rollback-time untracked enumeration.
- It quarantines new non-ledger files under `.protocol-tmp/rollback-quarantine/` and isolates
  every move in its own error handler.
- It reuses `Test-LedgerManagedPath`; therefore `Area_comun/mailbox/**`, including a message
  deposited during the exec window, is never quarantined.
- The live harness was not redeployed, as required; it remains on the prior version until
  TASK-0284 closes.

Permanent regression evidence in `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
declares and kills mutants for destructive reset, worktree replay, missing mailbox allowlist,
missing index-apply exit gate, and missing untracked-enumeration exit gate. The full loop also
proves tracked worktree content survives, created files remain recoverable in quarantine, and
an incoming mailbox message stays in `open/`.

Verified from a clean clone of commit `665a3b5`:

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0
- `python scripts/validate_collaboration_state.py` -> exit 0
- `python scripts/scan_encoding.py` -> exit 0
- `python scripts/scan_domain_neutrality.py` -> exit 0

Independent checker review is required; Codex has not reviewed or ratified this work.
