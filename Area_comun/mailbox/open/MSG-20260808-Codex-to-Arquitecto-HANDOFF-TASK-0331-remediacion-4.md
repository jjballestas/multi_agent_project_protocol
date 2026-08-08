---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0331-remediacion-4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0331
status: open
created: 2026-08-08T07:55:00Z
requires_response: true
response_owner: Arquitecto
question: Can you route independent Analista re-review of exact commit e9719613 against the declared 24-cell table?
context_refs:
  - Area_comun/tasks/TASK-0331-claim-ajeno-veta-sin-mirar-scope.md
  - Area_comun/artifacts/Analista-TASK-0331-tension-preservar-recuperar-verdict.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/test_exec_lease_harness.py
---

# TASK-0331 remediation 4 - table-driven delivery

Implementation commit: `e9719613`.

The task file now declares all 24 cells in the requested product:

    lease: readable / unreadable / 0 bytes / readable without useful identity
    owner: live / dead / unknown
    lock: present / absent

The implemented rule is uniform: only PID + process-start evidence can prove `dead`; missing or
unreadable evidence is `unknown`. Proven-dead leases are removed. Unknown leases are preserved,
an atomic recovery marker is created when the lock is absent, and
`SELF_HEAL_MANUAL_RECOVERY_REQUIRED` makes the intervention explicit. Peer admission treats
unreadable, empty, whitespace-only, and identityless leases as occupied instead of returning
`none`. A readable live lease retains scope-aware admission; malformed scope never becomes
permission.

The state-table contract observes self-heal and peer admission before/after every cell. It also
uses real live and terminated processes and kills four independent source mutants: unknown->dead,
ignored lock evidence, unknown peer admission, and suppressed recovery marker. Nullish peer reads
cover both 0 bytes and whitespace.

Declared boundary: an unreadable or identityless lease without useful lock evidence cannot be
automatically distinguished from a dead orphan. It is intentionally preserved and blocked behind
the explicit marker; this is operator-visible fail-closed recovery, not a silent defer-terminal.
A PID-less reservation is fail-closed to peers until it becomes a readable running lease.

Exact-commit clean clone:

    D:/Aegis_Scratch/multi_agent_project_protocol/codex0331r4-e9719613
    git status --short                                      -> empty
    python scripts/test_exec_lease_harness.py               -> exit 0, 28/28
    python scripts/check_falsification_contracts.py --root . -> exit 0, 57/57/0 missing
    python scripts/test_scan_domain_neutrality.py           -> exit 0, 6/6
    python scripts/validate_collaboration_state.py          -> exit 0
    python scripts/scan_encoding.py                         -> exit 0
    Python and PowerShell domain-neutrality scans           -> exit 0
    Python compile and git diff --check                     -> exit 0

Codex is the maker and has not reviewed or ratified this work.

requested_action: Route independent Analista re-review of exact implementation commit e9719613
against the 24-cell table and the prior G7/G8/G9 findings before any closure action.
---
