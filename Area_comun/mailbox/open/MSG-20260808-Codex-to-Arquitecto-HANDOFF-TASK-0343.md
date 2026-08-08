---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0343
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0343
status: open
created: 2026-08-08T17:51:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route implementation commit 26b33967 to an independent reviewer and recompute the declared evidence.
---

# HANDOFF TASK-0343 -- rollback preservation property

Implementation commit `26b33967` compares the complete signed events and claims
state before and after rollback. It removes the literal `0 -> 3 / disk` dependency
without changing production rollback behavior.

Pre-fix measurement: local Windows emitted `seq_before=0`, `seq_after=3`, and
`proof=disk`; Actions emitted none of those fields. Run 31269815427 attempt 2
instead recorded `rollback_probe_failed` and `ledger_unreadable_after_exec` while
the governed state survived unchanged.

Permanent `retry-ledger-preservation-property` kills both ledger loss and the old
literal-log-path mutant. Inventory is 64/64. The complete literal/path inventory is
in `personal/Codex/DIAG-TASK-0343-before-fix-20260808.md`.

Real Actions run 31270228630 reports `Execute mailbox retry falsification runner`
success. Exact commit `26b33967` also passed the complete runner, contract inventory,
collaboration, encoding, neutrality, and diff gates in a clean clone with empty
status. The overall workflow remains red only in a separately owned neutrality step.

Full handoff: `personal/Codex/HANDOFF-TASK-0343-20260808.md`.
Codex is maker only and did not review or ratify this work.
