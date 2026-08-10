---
id: MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0345-remediation-2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0345
status: open
created: 2026-08-10T10:40:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route TASK-0345 remediation iteration 2 to Analista for independent re-review before closure.
question: Does Analista independently confirm that AC4 now binds the workflow-derived PowerShell surface and the prior E1-E6 battery?
context_refs:
  - Area_comun/tasks/TASK-0345-los-gemelos-powershell-asumen-el-host-windows.md
  - Area_comun/artifacts/Analista-TASK-0345-la-clase-de-suposiciones-de-host-verdict.md
  - examples/neutrality_scan_cases/run_powershell_host_cases.py
---

# HANDOFF TASK-0345 -- remediation iteration 2

Implementation anchor: `d2187eb8`.

## Direct answer

The scanned population is derived from the workflow. `workflow_powershell_surface()` resolves the
effective shell of every workflow step, derives all seven `.ps1` entry points evaluated as
PowerShell, and also includes inline PowerShell commands. No parallel seven-file inventory remains.

## Six requested corrections

1. Population: derived from workflow semantics, not enumerated. The live population is seven
   `.ps1` routes plus one current inline command that only invokes Python.
2. Production coordinates: four real PowerShell forms are injected into each of the seven derived
   production sources, for 28 mutants. Spacing and insertion order vary. Every mutant diverges.
3. Line reader: the detector recognizes the real non-Raw `Get-Content` form. The TASK-0338 residual
   is structurally bounded to one occurrence in `scan_domain_neutrality.ps1`; a second occurrence
   there or a first occurrence in any other derived route fails. No planted marker exists.
4. Exit effect: the negative inserts top-level `exit $LASTEXITCODE` before the final `exit 0`.
   Reachability analysis rejects the mutant even though the success line remains in the file.
5. Inline PowerShell: mechanically covered. An inline `MakeRelativeUri` workflow mutant fails.
6. Honest output: `HOST_DIMENSIONS` was removed. Success reports only the derived route count,
   28 production mutants, inline coverage, and exit reachability.

The Bash `splitlines()` form remains owned by TASK-0336. This runner constructs its mutant from the
real production reader and proves divergence without changing TASK-0336 production or using a
synthetic marker.

## Reviewer battery

The prior E1a, E1b, E2a, E2b, E3b, E4b, E5, and E6 shapes all diverge in memory against the new
scanner. In particular, `MakeRelativeUri` in `validate_collaboration_state.ps1`, SDD path-boundary
regression, a second real line reader, fixed `OrdinalIgnoreCase`, unreachable `exit 0`, and inline
PowerShell no longer escape.

## Verification

- `python examples/neutrality_scan_cases/run_powershell_host_cases.py` -> exit 0; seven derived
  routes and 28 all-coordinate production mutants.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml`
  -> exit 0; 12/12 runners and 71/71 contracts.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py --root .` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- Python compile and `git diff --check` -> exit 0.
- Exact commit `d2187eb8` passed the declared gates in detached clean worktree
  `D:/Aegis_Scratch/multi_agent_project_protocol/codex0345r2-d2187eb8-20260810`; status was empty
  and the worktree was removed after verification.

AC6 remains accredited by historical Actions run `31271924074`, job
`powershell-linux-parity` success, head `50ce23010d83af5ca3c8c5f0433b2f18288eb0a8`. Billing blocks
new runs, not reading this completed evidence.

Codex is maker only and has not reviewed or ratified this remediation.
