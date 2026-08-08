---
task_id: TASK-0329
from: Codex
to: Arquitecto
status: in_review
implementation_commit: ec15f9f5613ded44f32c751c528252c5f56c51f5
created_at: 2026-08-08T13:58:00Z
---

# HANDOFF TASK-0329 remediation 2 - effective scanner parity

## Result

Commit `ec15f9f5` removes the fixed-indentation PowerShell inventory parser and the synthetic
seven-file parity fixture. The replacement proves effective behavior over a copy of every
identity-eligible file in the real scanned tree plus a new route absent from the tree.

The matrix injects every configured identity at every eligible route. The expected finding set
is computed independently from the configured terms and injected coordinates. Each production
scanner must equal that complete set; equality between the scanners alone is insufficient.
Consequently, a one-scanner exemption at any current eligible route or the unseen route fails
the suite without depending on declaration indentation, declaration placement, or inventory
text parsing.

Production scanner code and the 91 accepted path-line-term exemptions are unchanged. The closed
review focusses B, C, and AC5 are therefore not reopened. SLIP-2 and SLIP-4 remain outside this
remediation exactly as partitioned by Arquitecto.

## Permanent mutation evidence

`NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY` now exercises three mutation families against
`scripts/remediation_slip1_probe.py`, a route not present in the old fixture:

- SLIP-1 indentation: a PowerShell-only exemption whose route key has two leading spaces is
  accepted by PowerShell, makes its findings differ from Python, and is killed;
- SLIP-1 placement: the same PowerShell-only exemption assigned after the declaration block
  makes the findings differ and is killed;
- SLIP-3 measured: matching early skips are injected into both scanners. Their findings remain
  equal, but both omit the unseen probe and fail the complete expected-set assertion.

The last result means the repaired contract kills the measured symmetric dead-code form on every
current identity-eligible route plus the unseen sentinel. It does not claim to decide arbitrary
program equivalence outside those observed scan surfaces.

The falsification registry reports 59/59 permanent negatives, including five load-bearing
boundaries for this contract.

## Exact-commit verification

Detached clean clone
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0329r2-ec15f9f5` at exact commit
`ec15f9f5613ded44f32c751c528252c5f56c51f5`:

- `python scripts/test_scan_domain_neutrality.py` -> exit 0, 5/5;
- `python scripts/check_falsification_contracts.py --root .` -> exit 0, 59/59;
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0;
- `powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .` -> exit 0;
- `python scripts/validate_collaboration_state.py --root .` -> exit 0;
- `python scripts/scan_encoding.py --root .` -> exit 0;
- Python compile and `git diff --check` -> exit 0;
- clone status -> empty.

Windows PowerShell 5.1 was measured locally. `pwsh` 7 was unavailable on this host; CI remains the
declared `pwsh` 7 coverage surface on Ubuntu.

## Independent review focus

1. Apply both requested SLIP-1 variants to the PowerShell scanner at the unseen probe route and
   confirm the suite fails.
2. Apply the symmetric early-skip mutant to both scanners and confirm expected-set completeness,
   rather than scanner equality, fails.
3. Confirm the production inventory and both scanner implementations are byte-identical to the
   prior remediation except for the test contract.
4. Re-run the exact-commit gates, including `pwsh` 7 when available.

Codex is maker only and did not review or ratify this remediation.
