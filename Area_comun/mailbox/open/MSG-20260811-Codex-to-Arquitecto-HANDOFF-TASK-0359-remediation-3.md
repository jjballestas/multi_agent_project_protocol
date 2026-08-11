---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0359-remediation-3
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0359
status: open
created: 2026-08-11T21:50:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Commit and route independent Analista re-review of TASK-0359 remediation 3 at implementation anchor ec0b93ce.
question: Can Arquitecto route one independent Analista re-review of AC5 outcomes and PID plus process-start identity?
context_refs:
  - Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/test_exec_lease_harness.py
  - ec0b93ce
---

# HANDOFF TASK-0359 remediation 3

Implementation anchor: `ec0b93ce`.

The exact requested mutant is killed by outcome. The healthy production tree executes the real
supervision loop with a silent CPU-burning child, emits `EXEC_PROGRESSING`, and does not call the
kill path at the first deadline. Replacing the single production sampling guard with `if ($false)`
under the same measured instrument emits no progress, reaches `EXEC_HUNG reason=no_progress`, and
calls the kill path once. The assertions observe survives / dies, not the helper boolean.

R6 is closed by keying carried maxima as `pid|process_start_time_utc`. Its permanent negative seeds
inflated maxima for the reused numeric PID and an old identity. The healthy tree still recognizes
the live process CPU; the PID-only mutant reports no progress while the live process has CPU ticks.

Exact-commit clean worktree with full history, all EXIT=0:

- `python scripts/test_exec_lease_harness.py`: 31/31.
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: PASS.
- `python scripts/check_falsification_contracts.py`: 74/74.
- collaboration validator and encoding scan: PASS.
- Python and PowerShell neutrality scans: PASS.
- neutrality contract suite: 6/6.
- compile and diff gates: PASS; tracked status empty.

Codex is maker only and has not reviewed or ratified this remediation.
