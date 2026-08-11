# TASK-0359 remediation 3 memory

- Implementation commit `ec0b93ce` closes AC5 by executing the real production supervision
  loop with a silent CPU-burning process. The healthy tree reaches `EXEC_PROGRESSING` and is not
  killed; the one-line production mutant changing the sampling guard to `if ($false)` reaches
  `EXEC_HUNG reason=no_progress` and is killed.
- `Get-ExecTreeCpuSample` now keys carried maxima by `pid|process_start_time_utc`. A permanent
  negative seeds inflated entries for the reused numeric PID and the old process identity; the
  healthy implementation detects live CPU work while the PID-only mutant reports no progress.
- The harness suite passed 31/31. Mailbox retry, falsification inventory 74/74, collaboration,
  encoding, Python/PowerShell neutrality, neutrality contract tests, compile, and diff gates
  exited 0 before the implementation commit.
- The implementation commit intentionally excludes concurrent Arquitecto TASK-0354 ledger and
  mailbox changes that remained uncommitted in the shared tree. TASK-0359 remains `in_progress`
  under `CLAIM-20260811-Codex-TASK-0359-remediation3-v3`; delivery still needs exact-commit clean
  verification, `in_review`, claim release, and an independent Analista re-review.
