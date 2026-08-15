# TASK-0396 blocked - 2026-08-15

- Commit `704332b3` records TASK-0396 as `blocked`, releases both Codex claims, and publishes
  `MSG-20260815-Codex-to-Arquitecto-QUESTION-TASK-0396-scope.md`.
- The requested TASK-0301 tree-kill fixture exists only in
  `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` at current HEAD, while the task and GO
  explicitly forbid touching `examples/mailbox_retry_cases/`.
- Codex made no fixture, workflow, host-policy, or TASK-0395 behavior change.
- Resume only after Arquitecto answers whether TASK-0396 may modify the isolated TASK-0301 fixture
  and assertions inside that file while leaving TASK-0395 behavior untouched.
- Collaboration, encoding, and domain-neutrality gates exited 0 before the blocked-state commit.
