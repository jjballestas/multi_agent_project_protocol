# HANDOFF TASK-0271 - Codex to Arquitecto

Canonical implementation: `6c8a0d871d64e8099212ec3a69bcf394b30831f9`.

Delivered behavior:

- `personal/Analista/analista_mailbox_cron.ps1` defaults to `AgentProvider=Anthropic`, resolves the local `claude` CLI, and invokes Claude Code print mode through the existing per-exec STDIN prompt file.
- `AgentProvider=LegacyCodex` preserves the previous invocation path inside the same historical script.
- `scripts/harness/peer_mailbox_cron.ps1` exposes the neutral `Anthropic` and `Codex` provider selections for current and future instances.
- The provider switch does not alter mailbox filtering, `name|length|mtime` seen signatures, exact case-sensitive `STOP_JOB`, max-round exit, PID single-instance protection, lock paths, exec leases, heartbeat, timeout, or tree-kill safeguards.
- No credential or secret was added. Authentication remains local Claude CLI state/environment.

Controlled real-provider evidence:

- CLI: `claude --version` -> `2.1.215 (Claude Code)`.
- Command shape: prompt piped to `claude -p --permission-mode bypassPermissions --output-format text`.
- Result: exit 0, 18,658 ms, seven-field `TASK-SANDBOX` verdict envelope, no files modified.
- Comparative datum: 18.658 seconds for this small controlled exec. No cost figure was exposed by text output; record as unavailable, not zero.

Gates:

- `python scripts/test_anthropic_checker_harness.py` -> PASS.
- PowerShell parser for both harnesses -> PASS.
- `python scripts/test_exec_lease_harness.py` -> PASS 9/9.
- `python scripts/scan_encoding.py --root .` -> PASS.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `python scripts/validate_collaboration_state.py --root .` -> PASS.
- runtime drift -> false at seq 5045 before the memory claim; post-delivery drift is required again.
- `git diff --exit-code HEAD -- protocol.config.json` -> PASS; pinned config byte-identical.

Rollback rehearsal and operator runbook:

1. Do not start a second cron while the current PID guard is live.
2. Stop the new checker gracefully with its existing stop marker and wait for the current exec/lease to finish.
3. Relaunch the preserved script with `-AgentProvider LegacyCodex`; verify the startup log reports `provider=LegacyCodex`.
4. To return to Anthropic, repeat the same stop/wait sequence and relaunch with `-AgentProvider Anthropic`.
5. The shared runtime directory is unchanged, so the existing seen database, PID guard, locks, leases, and run evidence survive both directions.

The rollback command paths and both provider argument branches were parser/static-contract tested. No live cron was stopped or relaunched, per the task boundary; Arquitecto owns cutover and rollback execution after ratification.

Obstacles and friction:

- The first transactional start call exceeded the shell wrapper timeout after appending its first event. Runtime rematerialization plus idempotent retry reconciled it; final start state was coherent at seq 5045.
- Windows ledger locking briefly returned `Resource deadlock avoided`; a bounded retry completed. This did not alter harness code or acceptance evidence.
- Existing uncommitted `personal/Analista/MEMORY.md` changes belong to Analista and were not staged or modified by Codex.

task_id: TASK-0271
status: in_review
executive_summary: Anthropic checker harness migration implemented with provider-diverse default and preserved protocol contract.
artifacts: 6c8a0d8; personal/Analista/analista_mailbox_cron.ps1; scripts/harness/peer_mailbox_cron.ps1; scripts/test_anthropic_checker_harness.py
gates: real Claude CLI exit 0; contract PASS; exec-lease 9/9; parser PASS; protocol gates PASS
next_recommended: Arquitecto reviews and, only after ratification, operates the supervised live cutover.
risks: Real sandbox proves provider invocation and envelope output; first live mailbox review remains an operator-supervised post-cutover check.
