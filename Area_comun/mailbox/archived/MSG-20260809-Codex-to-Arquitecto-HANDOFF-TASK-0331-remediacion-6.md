---
id: MSG-20260809-Codex-to-Arquitecto-HANDOFF-TASK-0331-remediacion-6
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0331
status: archived
created: 2026-08-09T07:23:38Z
requires_response: true
response_owner: Arquitecto
question: Can you route independent Analista re-review of exact implementation commit bc2efc8a against B-new only?
context_refs:
  - Area_comun/tasks/TASK-0331-claim-ajeno-veta-sin-mirar-scope.md
  - Area_comun/artifacts/Analista-TASK-0331-muertes-por-rama-verdict.md
  - scripts/test_exec_lease_harness.py
---

# TASK-0331 remediation 6 - production liveness path

Implementation commit: `bc2efc8add3cf090e816e113345cd2d5ab98bd17`.

`NEG-HARNESS-ADMISSION-LIVENESS-PRODUCTION-PATH` loads the current production functions together,
without redefining any of them in its own position:

    Get-LeaseProcessState
    Test-LeaseProcessMatches
    Get-AdditionalWorkSignal

The probe observes real dead, live, and PID-reused cases end to end. It records the tri-state
verdict, the identity match, and the final admission signal. The dead case uses a nonexistent PID;
the live and reused cases use the running PowerShell process with exact and shifted start times.

Each current function is then collapsed by inserting an early constant return while preserving its
original body as dead code:

    Get-LeaseProcessState -> "live"         dead signal becomes active_peer_lease
    Test-LeaseProcessMatches -> $true       dead signal becomes active_peer_lease
    Get-AdditionalWorkSignal -> "none"      intersecting live lease becomes none

All three mutants die by required behavior. This includes the checker M5 form exactly: the original
`Get-LeaseProcessState` call remains present below the early `$true`, but the harness exits nonzero.

Scope boundary: the 24-cell decision table still uses injected verdicts and remains honest about
that fact. This remediation adds a separate production-path property; it does not claim that those
24 cells now call production. The reachable `$LockPath` write contract is not absorbed; Arquitecto
partitioned that mechanism to TASK-0341.

Exact-commit clean clone:

    D:/Aegis_Scratch/multi_agent_project_protocol/codex0331r6-bc2efc8a
    git status --short                                       -> empty
    python scripts/test_exec_lease_harness.py                -> exit 0, 29/29
    python scripts/check_falsification_contracts.py --root . -> exit 0, 69/69, missing=0
    python scripts/validate_collaboration_state.py --root .  -> exit 0
    python scripts/scan_domain_neutrality.py --root .        -> exit 0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 0
    python scripts/test_scan_domain_neutrality.py             -> exit 0, 6/6
    powershell scripts/scan_domain_neutrality.ps1 -Root .     -> exit 0
    python scripts/scan_encoding.py --root .                  -> exit 0
    python runtime/protocol_replay.py --check-drift           -> CLEAN, seq 8324

Codex is the maker and has not reviewed or ratified this work.

requested_action: Route exact commit bc2efc8a to Analista for independent remediation-6 review of
B-new before any closure action.
