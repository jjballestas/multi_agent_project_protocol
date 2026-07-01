---
handoff_id: HANDOFF-TASK-0236-codex-to-arquitecto-1
task_id: TASK-0236
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-02
---

# TASK-0236 handoff - cron harness remediation

Implemented in the protocol repo:

- `personal/Codex/codex_mailbox_cron.ps1`
- `personal/Analista/analista_mailbox_cron.ps1`
- `personal/Arquitecto/arquitecto_cron.ps1`
- `scripts/test_exec_lease_harness.py`

Changes:

- Prompts are now per exec under `runs/<timestamp>-<message>.prompt.txt`; the shared prompt path was removed from the active execution path.
- Deadline cleanup now calls `taskkill.exe /PID <pid> /T /F` through `Stop-LeaseProcessTree`, with deny-kill checks for `submit_intent`, `git`, `npm test`, `vitest`, and validator command lines.
- Startup now enforces a single live cron instance using `pid + process_start_time_utc` persisted beside the pid file.
- Startup self-heal now removes dead PID leases before deadline and tree-kills matching live expired orphan leases before clearing lock+lease.
- Stop-order detection now requires exact `STOP_JOB` equality in `requested_action` or `one_line_summary`; prose that only mentions the token no longer stops the cron.
- Arquitecto cron now has the same exec-lease contract as Codex/Analista for prompt, lock, lease, deadline, and cleanup behavior.

Evidence:

- `python -m py_compile scripts\sweep_cron_zombies.py scripts\test_exec_lease_harness.py` PASS.
- PowerShell parser PASS for Codex, Analista, and Arquitecto harnesses.
- `python scripts\test_exec_lease_harness.py` PASS 9 tests, covering dead-PID cleanup, kill-mode lock+lease cleanup, owner/checker exclusions, dry-run default, exec-lease contract, no deadline wait for dead PID cleanup, per-exec prompts, tree-kill plus single-instance guard, and exact stop-order matching.
- `git diff --check` PASS for touched files.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` exit 0.
- `python scripts\validate_collaboration_state.py --root .` PASS.
- Drift PASS: `has_drift=false`, byte-identical, `up_to_seq=3041`.

Notes:

- `D:/Agentes/Zeus/Zeus-protocol` was clean and untouched; TASK-0236 scope is protocol cron infrastructure.
- Existing unrelated untracked files under peer/operator personal areas were left untouched.
