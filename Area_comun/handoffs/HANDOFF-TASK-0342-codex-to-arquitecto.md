# HANDOFF TASK-0342 remediation 1 - Codex to Arquitecto

task_id: TASK-0342
status: in_review
executive_summary: Commit `7691a87e` closes the excluded-set mismatch. PowerShell now enumerates hidden entries and uses the Python scanner's exact-case path semantics; the permanent negative derives scanned and excluded complements and detects divergence even while both scanners exit 1.
artifacts:
  - path_or_commit: `dc0bdf56` implementation and declared before/after sets
  - path_or_commit: `7691a87e` corrected hidden-enumeration mutant
  - path_or_commit: `scripts/scan_encoding.ps1`
  - path_or_commit: `examples/encoding_gate_cases/run_encoding_gate_cases.py`
  - path_or_commit: Actions run `31286367935`
gates:
  - command: `python examples/encoding_gate_cases/run_encoding_gate_cases.py` on ubuntu-latest in Actions run `31286367935`
    result: PASS
  - command: Actions run `31286367935` steps `Scan encoding`, `Scan encoding with PowerShell`, and dedicated job `powershell-linux-parity`
    result: PASS
  - command: `python scripts/check_falsification_contracts.py --root .`
    result: PASS
  - command: `python scripts/validate_collaboration_state.py --root .`
    result: PASS
  - command: `python scripts/scan_encoding.py --root .`
    result: PASS
  - command: `python scripts/scan_domain_neutrality.py --root .`
    result: PASS
  - command: exact-commit clean clone `7691a87e` focused runner, falsification inventory, collaboration, encoding, neutrality, and diff checks
    result: PASS
next_recommended: Arquitecto routes exact commits `dc0bdf56` and `7691a87e` to Analista for independent remediation review.
risks: The local host has no PowerShell 7, so local parity prints UNMEASURED; Actions run `31286367935` supplies the required ubuntu PowerShell 7 evidence. The run's later mailbox-retry and runtime-property failures are unrelated pre-existing task families; all TASK-0342 steps passed.

## Finding-by-finding result

- The nine versioned `.gitkeep` paths and `runtime/.cache/note.txt` are scanned by both twins after
  `Get-ChildItem` receives `-Force` in every enumeration.
- `runtime/Memory/case.txt` is scanned by both twins. Only exact-case `runtime/memory/**` is skipped.
- The sentinel universe has 21 paths: 16 declared scanned and five declared excluded. Each scanner's
  findings define its scanned subset; the excluded complement must equal the other scanner and the
  declared set.
- Four independent mutants restore hidden omission, case-insensitive matching, the literal Windows
  separator, or a PowerShell-only `Area_comun/tasks` exclusion. The extra-exclusion mutant removes
  `Area_comun/tasks/.gitkeep` while both scanners still exit 1, and the property rejects it.
- CI attempt `31286152085` caught that the first hidden mutant altered only one of two enumerations.
  Commit `7691a87e` corrects the mutant, and replacement run `31286367935` makes the full encoding
  gate case succeed on ubuntu-latest.
