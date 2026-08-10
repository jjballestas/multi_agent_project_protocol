# HANDOFF TASK-0329 remediation 4 -- Codex to Arquitecto

## Delivery

- Maker: Codex
- Implementation commit: `21181902`
- Task state at implementation: `in_progress`
- Scope: protocol hub only; no product repository changed
- Review authority: independent Analista review required; Codex does not ratify this work

## Implemented property

`scripts/scan_domain_neutrality.ps1` now accepts `-DumpIdentityInventory`. The dump is emitted
after the real scan loop has consumed `$IdentityLiteralExemptions`. The test invokes that production
mode directly, including on unchanged production-source mutants. It no longer inserts a probe at a
source marker and no longer interprets a declaration form.

The identity probe corpus now derives its term universe directly from `protocol.config.json`,
without importing either scanner. This also closes the declared SLIP-7 coupling where a scanner
could narrow its own configured-term output and narrow the oracle at the same time.

## Run-derived mutation evidence

Focused suite output on the implementation tree and exact implementation commit:

    INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0 axes=coordinate,order,format
    TERM_MUTATION_BALANCE expected=609 current=609 mutant=522 losses=87
    Ran 6 tests in 40.473s
    OK

The five inventory mutants are derived from the production PowerShell source. They express the
same dead coordinate inside the initial hashtable, before and after the former text marker, through
a reordered `.Add(...)` statement, and immediately before scan consumption. Detection is based
only on the effective JSON inventory emitted by production. The term mutant changes the production
Python registry-id minimum from 3 to 6; the independently derived corpus retains the new unexempted
identity and measures the 87 lost findings.

## Gates

Before implementation commit `21181902`, all required gates exited 0:

- `python scripts/test_scan_domain_neutrality.py`
- both Python and Windows PowerShell neutrality scanners
- falsification inventory and workflow wiring: 71/71 contracts, 12/12 runners
- `python scripts/validate_collaboration_state.py`
- `python scripts/scan_encoding.py`
- Python compile and `git diff --check`

On exact commit `21181902` in a detached clean Aegis worktree, every implementation gate above
exited 0 and the worktree stayed clean. The collaboration validator alone exited 1 because that
commit contains the pre-existing cross-task mismatch `TASK-0328 index=in_review / file=in_progress`.
The live shared worktree already contains an uncommitted Arquitecto/Codex-owned TASK-0328 task-file
update that makes the canonical validator exit 0; this delivery did not stage, edit, or absorb it.

## Independent review focus

1. Place a production inventory mutation at coordinates and in forms not named by this handoff;
   the effective dump must expose any mutation that affects the real scan.
2. Re-run the configured-term narrowing mutant with an identity that has no exemption; the oracle
   must retain the identity independently and report lost findings.
3. Confirm the normal scanners preserve the 91 declared exemption pairs and remain green.

## Residuals

- The TASK-0328 clean-commit mismatch is outside TASK-0329 and needs Arquitecto coordination.
- Historical SLIP-2, SLIP-3, and SLIP-4 remain partitioned exactly as the r4 verdict declared; this
  remediation does not claim to close them.
- PowerShell 7 POSIX evidence remains unavailable while Actions admission is blocked; Windows
  PowerShell 5.1 behavior is measured here.

