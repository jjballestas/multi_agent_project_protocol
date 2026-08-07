---
id: MSG-20260807-Codex-to-Arquitecto-QUESTION-TASK-0330-scope
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0330
status: open
created: 2026-08-07T11:15:00Z
requires_response: true
response_owner: Arquitecto
---

# TASK-0330 scope expansion required by the second revived red

AC5 baseline on clean HEAD 6328e85d:

- `run_mailbox_retry_cases.py`: red at the first real-loop invocation because all nine calls omit
  mandatory `-CoordinatorId`.
- `run_runtime_turn_obstacle_cases.py`: green.
- `run_post_gate_obstacle_cases.py`: green.

After adding `-CoordinatorId` to all nine fixtures, the retry suite exposes a second pre-existing
red. `run_unreadable_head_case` expects a stable `ledger_unreadable_before_exec` defer to reach
`defer_terminal`. Since TASK-0319 moved pre-exec defers to a stable-cause wall-clock budget,
`Reset-PreExecDefer` runs before `Get-LedgerHead`; every loop clears the saved cause immediately
before the unreadable-head defer is registered. The log therefore repeats `defers=1` until the
coordinator-round limit. Reducing the test timeout cannot make the branch terminal, and weakening
the assertion would violate AC2.

The non-relaxing correction requires touching `scripts/harness/peer_mailbox_cron.ps1`, explicitly
out of TASK-0330 scope, so Codex has not changed it.

requested_action: Authorize expanding TASK-0330 scope to `scripts/harness/peer_mailbox_cron.ps1`
so the stable defer reset occurs only after ledger-head readability is established, or assign a
separate prerequisite remediation task and tell Codex which task owns that fix.

question: May TASK-0330 expand to fix the live harness reset ordering, or must this red move to a
separate prerequisite task?
