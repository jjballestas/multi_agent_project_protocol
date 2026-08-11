# HANDOFF TASK-0342 remediation 4 - AC4 ready for independent re-judgment

task_id: TASK-0342
owner_maker: Codex
delivery_status: in_review
implementation_commit: `14686290`
memory_commit: `97d784b9`
deferred_acceptance: AC5

## Delivered implementation

- `scripts/scan_encoding.ps1` constructs one policy object. Every `Should-Scan` decision consumes
  that object, and `-DumpPolicy` serializes the same object after the scan calls consume it.
- The parity fixture derives directory, root-relative directory, suffix, case, boundary-neighbor,
  and non-excluded control coordinates from the effective Python and PowerShell policies.
- The runner no longer parses the PowerShell declaration line or reserves `dist` as a control.
  Mutants are inserted at the policy construction/consumption boundaries and judged from dumped
  values plus observed scan sets.
- The final line reports PowerShell parity as `UNMEASURED` when the branch did not run and reports
  measured parity only when `pwsh` ran on a case-sensitive filesystem.

## Checker criteria measured

On WSL2 Ubuntu with `pwsh 7.4.6` and a case-sensitive ext4 fixture:

- G9a, G9b, G9c, and G9d: each emitted `CAUGHT_DIVERGENCE` and the runner exited 0.
- A4 and A7: each emitted `CAUGHT_DIVERGENCE`.
- A5 and A8: each emitted `ACCEPTED_EQUIVALENT`.
- Independent source variants G6six, G6ord, and G6ws: each full runner exited 0 without editing
  the runner for the coordinate.
- `NEG-ENCODING-SKIP-PATH-SEPARATOR`: 16 declared boundaries; inventory 73/73.

## Exact-commit evidence

Exact implementation `14686290` passed in a detached clean worktree with empty tracked status:

- collaboration validator, encoding, Python neutrality, and PowerShell neutrality: exit 0;
- falsification contract gate and inventory: exit 0, 73/73;
- WSL2 PowerShell parity runner: exit 0 with measured parity;
- Python compile, protocol drift (`CLEAN up_to_seq=8779`), and diff gate: exit 0.

The four exact-commit and G6 scratch worktrees were removed after verification as required by the
scratch discipline.

## Deferred boundary

AC5 is not claimed. Per the operator instruction, real Actions admission remains deferred while
billing prevents jobs from starting. This handoff requests the single authorized independent
Analista re-judgment of AC4 only. TASK-0342 cannot reach `done` until AC5 is later measured or the
operator records a different closure decision. Codex is maker only and has not reviewed or
ratified this implementation.
