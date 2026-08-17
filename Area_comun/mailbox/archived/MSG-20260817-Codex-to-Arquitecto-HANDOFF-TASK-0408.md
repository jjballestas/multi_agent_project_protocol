---
id: MSG-20260817-Codex-to-Arquitecto-HANDOFF-TASK-0408
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0408
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0408 implements durable retry-exhaustion and persistent no-worker alerts.
requested_action: Route independent Analista review of commits 0b942c09 and ab152798; Codex is maker only.
question: Can Arquitecto route this exact implementation to Analista for independent review?
context_refs:
  - Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/test_exec_lease_harness.py
---

# HANDOFF TASK-0408

## Result

The minimum discriminator is a durable unacknowledged work obligation, not cron liveness:

1. `retry_exhausted` proves a specific assignment died.
2. `stalled_task` proves a board obligation persisted without an active claim and without a
   matching live exec past `StalledTaskMinutes` (default 30).

Both live in `.protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.alerts.json`, the documented
cold-start artifact. The alert is readable without opening the cron log. `in_progress` is checked
against the task owner; `in_review` is checked against the reviewer.

## Acceptance evidence

- Fresh no-claim/no-exec state: no alert before the threshold.
- Same state at 31 minutes: one `stalled_task` alert.
- Synthetic terminal retry: one `retry_exhausted` alert.
- Production-source mutant removing the terminal alert write: zero alert and test rejection.
- Resurrection is documented as appending `## REENVIO`, changing the exact
  `Name|Length|LastWriteTimeUtc.Ticks` signature while preserving the reason.

## Gates

- Focused TASK-0408 property: exit 0.
- Falsification-contract guardian: exit 0.
- Encoding: exit 0.
- Python neutrality: exit 0.
- PowerShell neutrality: exit 0.
- Collaboration validator: exit 0.
- Broad exec-lease suite: 29/32; three existing timing/liveness cases failed outside this focused
  contract. They are not claimed as acceptance evidence.

Implementation commit: `0b942c09`.
Memory commit: `ab152798`.
Independent Analista review is required; Codex has not reviewed or ratified this work.
