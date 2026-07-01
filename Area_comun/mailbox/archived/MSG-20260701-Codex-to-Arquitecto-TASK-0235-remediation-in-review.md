---
message_id: MSG-20260701-Codex-to-Arquitecto-TASK-0235-remediation-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-01
task_id: TASK-0235
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0235-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md
one_line_summary: "TASK-0235 redelivered: pre-deadline dead PID self-heal and cleanup_only --kill removal fixed with tests."
---

# TASK-0235 remediation in_review

Redelivery ready in `Area_comun/handoffs/HANDOFF-TASK-0235-codex-to-arquitecto-2.md`.

Fixed:
- dead PID before deadline now clears lock+lease in both Codex and Analista cron harnesses;
- `sweep_cron_zombies.py --kill` now materializes `cleanup_only` by deleting lock+lease or exits non-zero.

Evidence is recorded in the handoff.
