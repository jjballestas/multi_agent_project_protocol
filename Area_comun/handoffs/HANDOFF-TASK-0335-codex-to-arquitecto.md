# HANDOFF TASK-0335 - Codex to Arquitecto

task_id: TASK-0335
status: in_review
executive_summary: Commit dbe9a508 replaces positional retry-log matching with semantic field assertions and proves both no-terminal and wrong-cause mutations. Remediation restores the unrelated exact assertion, records eight additional measured reds plus one preventive hardening, and repairs the cross-task fixture regression exposed by TASK-0331; production remains untouched.
artifacts:
  - path_or_commit: dbe9a50829c7aae5ef32273113823635b8901e47
  - path_or_commit: examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - path_or_commit: Area_comun/tasks/TASK-0335-asercion-acoplada-al-formato-del-log.md
gates:
  - command: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    result: PASS
  - command: python scripts/test_exec_lease_harness.py
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS (52/52)
  - command: python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml
    result: PASS (8/8 runners, 52/52 contracts)
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: git diff --check
    result: PASS
next_recommended: Route independent review to Analista; Codex must not review or ratify this maker delivery.
risks: No known residual in the explored runner. Scope-aware admission remains protected by its existing permanent negatives; production code was not changed.

## Remediation iteration 1

- Restored exact equality for the governed pre-dirty task file; no unrelated assertion remains
  relaxed.
- AC7 now records the measured result: eight additional red failures plus one separate preventive
  hardening in `run_disordered_ledger_case`.
- This was a cross-task fixture regression: the correct TASK-0331 fail-closed admission change
  exposed incomplete archived-task metadata in TASK-0335 fixtures. No TASK-0331 production code
  changed.

### Complete full-harness fixture scope inventory

The runner has nine fixture families that execute `peer_mailbox_cron.ps1`, for fourteen executions:

| Fixture family | Executions | Scope state |
|---|---:|---|
| deleted residue real loop | 3 | 2 resolvable; 1 deliberately unresolvable negative expects `message_scope_ambiguous` |
| unreadable ledger head | 3 | resolvable through the shared main sandbox metadata |
| unstaged residue | 1 | resolvable through the shared main sandbox metadata |
| disordered ledger | 1 | resolvable through the shared main sandbox metadata |
| post-delivery timeout | 1 | resolvable |
| exec-running heartbeat | 2 | resolvable |
| pre-delivery and liveness | 1 | resolvable |
| frozen exec with production freshness | 1 | resolvable |
| main retry/rollback loop | 1 | resolvable |

All six independently constructed fixture roots now provide both the hot task index and an empty
archive task index, plus a task file with `intake.scope_routes`. The three shared-sandbox families
reuse the main root. Thus thirteen executions are resolvable by construction and the sole
unresolvable execution is an explicit fail-closed negative.

### Complete extracted-function probe inventory

The runner has eleven sites that extract PowerShell function bodies. Nine are executable or feed
an executable probe; all nine now use `extract_powershell_function_closure`, which recursively
includes every harness function dependency and accepts only explicit probe-provided mocks. The
other two sites inspect text only and deliberately retain a single-body extraction.

| Probe site | Mode | Dependency state |
|---|---|---|
| outcome parser | executable | closure; root has no harness dependency |
| torn-tail rollback | executable | closure; resolves eight harness functions; `Write-Log` is provided by probe |
| large stderr drain | executable | fixed missing `Invoke-GitStatusPorcelainUtf8` and `Get-EmbeddedRepositoryRoots` via closure |
| expired-claim behavior | executable | fixed missing scope-resolution chain via closure; `Test-LeaseProcessMatches` is provided by probe |
| pure-append evidence | executable | closure resolves `Get-FilePrefixSha256`; `Write-Log` is provided by probe |
| useful-own-evidence | executable | closure resolves `Get-FilePrefixSha256`; `Write-Log` is provided by probe |
| UTF-8 residue path | executable | fixed missing two git-status dependencies via closure; `Write-Utf8NoBom` is provided by probe |
| frozen progress | body assertion plus full-runner execution | closure; root has no harness dependency |
| complete tree kill | executable | closure; `Write-Log` and `Test-LeaseProcessMatches` are provided by probe |
| nondestructive rollback contract | static inspection only | single-body extraction; no execution |
| git apply-failure contract | static inspection only | single-body extraction; no execution |

The three stale executable probes were one mechanism family: focused probes assumed their extracted
root remained dependency-free. `run_large_stderr_drain_case` was the deterministic cross-task
regression exposed by TASK-0334; the inventory also repaired the same latent assumption in the
expired-claim and UTF-8 residue probes before they could surface one by one. No third failure family
appeared, and no production file changed.
