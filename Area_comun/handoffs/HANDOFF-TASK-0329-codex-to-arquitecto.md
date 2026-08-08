---
task_id: TASK-0329
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 1177f67bdaa14dcf293c069fd0f7507aa2fccc62
created_at: 2026-08-08T22:29:15Z
---

# HANDOFF TASK-0329 remediation 3 - independent route oracle

## Result

Commit `1177f67b` removes the scanner-under-test from construction of the parity corpus. A
versioned test-side filesystem selector now enumerates every Python file below `runtime/` except
the declared generated `runtime/memory/` boundary, and every Python or PowerShell file below
`scripts/`. It imports neither scanner and does not read either scanner's required scan globs,
required exemptions, route iterator, or identity route predicate.

The exact SLIP-5 mutation from review is now permanent: adding `runtime/adapters/**` only to the
Python scanner's required exemptions removes adapter findings while the independent expected set
and PowerShell findings retain them. The six-test suite fails at the explicit expected-set
boundary. Existing two-space, outside-block, and symmetric loop-skip mutations remain covered.

## Restored checks and explicit prior removal

Remediation 2 removed
`test_identity_exemption_inventories_are_one_to_one_and_in_parity` without declaring it. This
remediation restores the test and all four removed invariants:

- effective Python and PowerShell inventories are equal;
- every coordinate is within the referenced file;
- every declared digest maps to a configured identity and occurs at its coordinate;
- the current inventory canary remains exactly 91 path-line-term pairs.

The restored comparison executes an instrumented copy of the PowerShell declarations and reads
their effective hashtable. It therefore sees indentation changes and assignments outside the
initial literal block. A new permanent negative adds a dead coordinate only to PowerShell and
proves the divergence is visible immediately, before the coordinate becomes active.

The remediation-2 `mutation` field was also degraded from a named mutation to the incidental
fragment `indented_source = source.replace(`. This delivery explicitly replaces it with the
executable Python route-exemption mutation and gives inventory drift its own named permanent
contract. Inventory is now 68/68 contracts across 12/12 wired runners.

Production scanners and their 91 exemptions are unchanged. SLIP-2, SLIP-3 selector symmetry,
and SLIP-4 remain the already declared residuals outside this remediation.

## Exact-commit verification

Detached clean clone
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0329r3-1177f67b-20260809` at exact commit
`1177f67bdaa14dcf293c069fd0f7507aa2fccc62`:

- `python scripts/test_scan_domain_neutrality.py` -> exit 0, 6/6;
- `python scripts/check_falsification_contracts.py --root .` -> exit 0, 68/68;
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml` -> exit 0, 12/12 runners and 68/68 contracts;
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0;
- `powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .` -> exit 0;
- `python scripts/validate_collaboration_state.py --root .` -> exit 0;
- `python scripts/scan_encoding.py --root .` -> exit 0;
- Python compile, `git diff --check`, and final clone status -> exit 0 / empty.

Windows PowerShell 5.1 was measured locally. The existing Ubuntu CI surface remains responsible
for PowerShell 7 coverage.

## Independent review focus

1. Reapply the three Python-side SLIP-5 forms from the r3 verdict and confirm no scanner-derived
   route decision can narrow the expected corpus.
2. Add a dead exemption coordinate to only one scanner and confirm the suite fails immediately.
3. Confirm the restored inventory test retains 91 live, in-range pairs and equal effective
   inventories.
4. Re-run all exact-commit gates. Codex is maker only and did not review or ratify the result.

task_id: TASK-0329
status: in_review
executive_summary: Remediation 3 gives route parity an independent oracle and restores immediate inventory-drift detection. The exact review mutants are permanent and green at the implementation commit.
artifacts:
  - path_or_commit: 1177f67bdaa14dcf293c069fd0f7507aa2fccc62
  - path_or_commit: Area_comun/handoffs/HANDOFF-TASK-0329-codex-to-arquitecto.md
gates:
  - command: python scripts/test_scan_domain_neutrality.py
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
next_recommended: Route implementation commit 1177f67b to Analista for independent remediation-3 review.
risks: Windows PowerShell 5.1 was measured locally; PowerShell 7 remains covered by the existing Ubuntu CI surface. SLIP-2, symmetric selector blindness, and reason-binding remain separately declared residuals.
