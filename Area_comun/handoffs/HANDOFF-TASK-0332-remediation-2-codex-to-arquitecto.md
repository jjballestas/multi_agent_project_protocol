# HANDOFF TASK-0332 remediation 2 -- production invariant and behavioral product

Implementation commit: `29175f01`.

The operator-authorized remediation changes production. `contains_pii` now completes a first pass
for every non-phone PII class across the complete input. Only a second pass applies `DATE_RE` as an
exemption from the phone heuristic. A date-shaped item can no longer stop the scan before a sibling
email or an instance term is evaluated.

The permanent negative executes a product derived from production-accepted coordinates:

    12 months x 24 hours x 1,684 ASCII offsets x 3 formats = 1,454,976 cases
    source positives = 1,454,976 / 1,454,976

Year, day, minute, second, and fractional length traverse their complete accepted ASCII marginal
ranges while that product advances. Each case places a real email after the exempt timestamp and
calls the production `contains_pii` entry point.

Three ephemeral mutants are derived from the production two-phase body. The AST is not an oracle.
The execution balance on exact commit `29175f01` is:

    TASK0332_BEHAVIOR product=1454976 source=1454976 mutants=3/3 coordinate=(False, True, False) order=(False, True) format=(False, True, False)

The coordinate mutant chooses month, hour, and offset from the generated domains rather than using
the checker probes. The order mutant makes a leading exempt timestamp stop the input scan. The
format mutant targets the production-accepted basic timestamp form. All three are production-source
mutants and all three diverge by execution.

The governed test rewrite shifted reviewed identity coordinates without adding identity literals.
Python and PowerShell neutrality inventories were moved in parity. Their behavioral contract remains
green with `total=5 caught=5 escaped=0`, and the term-derived minimum-length mutant still loses 87 of
609 expected findings.

Exact commit `29175f01` was verified in detached clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0332r2-29175f01`. The worktree had empty status.
Exit-0 gates:

- `python scripts/memory/test_memory_db.py` -- 72/72, 411.953 seconds;
- `python scripts/validate_collaboration_state.py`;
- `python scripts/scan_encoding.py`;
- Python and PowerShell domain-neutrality scanners;
- `python scripts/test_scan_domain_neutrality.py` -- 6/6;
- falsification inventory -- 71 declared / 71 permanent negatives;
- Python compile;
- protocol drift -- CLEAN through seq 8692;
- exact diff check.

Residual R0332-9 is explicit in the task: the finite corpus proves the full
month-by-hour-by-ASCII-offset-by-format product and complete marginals for other accepted ASCII
coordinates, not the impossible full Cartesian product over every coordinate simultaneously. The
production two-phase invariant is what prevents the strong sibling-PII suppression outside the
finite sample. R0332-3 for non-ASCII decimal digits remains owned by TASK-0322.

Codex is maker only. Codex has not reviewed or ratified this remediation. Independent Analista
re-review must choose new coordinate/order/format probes after this delivery.

task_id: TASK-0332
status: in_review
executive_summary: Production now prevents a date exemption from suppressing non-phone PII in another item. The 1,454,976-case behavioral product and three production mutants pass on exact commit 29175f01.
artifacts:
  - path_or_commit: 29175f01
  - path_or_commit: Area_comun/tasks/TASK-0332-muestreos-disjuntos-contrato-por-comportamiento.md
  - path_or_commit: scripts/memory/build_memory_db.py
  - path_or_commit: scripts/memory/test_memory_db.py
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS
next_recommended: Arquitecto routes independent Analista re-review at exact commit 29175f01.
risks: R0332-9 and inherited R0332-3 are explicitly declared; no self-review was performed.
