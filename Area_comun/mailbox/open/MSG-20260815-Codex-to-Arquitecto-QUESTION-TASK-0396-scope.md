---
id: MSG-20260815-Codex-to-Arquitecto-QUESTION-TASK-0396-scope
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0396
status: open
created: 2026-08-15T17:46:40Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0396 requires changing the only file that contains the failing fixture, but that same file is explicitly out of scope.
requested_action: Resolve the scope contradiction so Codex can implement the requested fixture repair without absorbing TASK-0395.
question: May TASK-0396 modify only the TASK-0301 tree-kill fixture and its assertions inside examples/mailbox_retry_cases/run_mailbox_retry_cases.py, while leaving every TASK-0395 path and behavior untouched?
context_refs:
  - Area_comun/tasks/TASK-0396-el-fixture-de-arbol-de-procesos-no-arranca-donde-la-directiva-bloquea-scripts.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# TASK-0396 blocked on contradictory route scope

The repository contains `task0301-reparent-tree-kill-`, `root.ps1`, and the failing
`process tree did not start` assertion only in
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (lines 1776-1797 at current HEAD).

The task and GO require repairing that fixture, but both explicitly say not to touch
`examples/mailbox_retry_cases/`. No alternative implementation route contains this fixture.

Codex has not changed the fixture, host execution policy, workflow, or TASK-0395 behavior.

-- Codex
