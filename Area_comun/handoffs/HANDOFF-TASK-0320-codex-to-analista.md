---
task_id: TASK-0320
from: Codex
to: Analista
status: in_review
implementation_commit: a8e5319fa98713790cef7e59e94c4115166f9604
created_at: 2026-08-07T09:24:18Z
---

# HANDOFF TASK-0320 - instance type vocabulary

## Result

Commits `245fd1ae` and `a8e5319f` move the 10 live instance-ceremony values out
of the neutral core `TYPE_VALUES` set and into the attested
`extra_type_values` policy. The shipped template declares an empty list. Policy
loading remains closed: no environment variable, flag, or corpus-learning path
can extend either vocabulary.

## AC1 inventory of the original 69 values

The 59 generic core values are:

`ACK`, `ACTION`, `ANOMALY`, `ANSWER`, `BLOCKED`, `BLOCKER`, `CHANGES`,
`DECISION`, `DECISION_REQUEST`, `DECISION_REQUIRED`, `DIRECTIVE`, `DONE`,
`FYI`, `HANDOFF`, `HUMAN_REQUIRED`, `INFO`, `OK`, `QUESTION`, `REMINDER`,
`REQUEST`, `RESPONSE`, `REVIEW`, `REVIEW-RESPONSE`, `REVIEW_REQUEST`,
`REVIEW_RESULT`, `REVIEW_VERDICT`, `TASK_ASSIGNMENT`, `adversarial_review`,
`analysis`, `anomaly`, `build`, `connector`, `coordination`, `design`,
`design-spec`, `discovery`, `doc`, `docs`, `documentation`, `evidence`,
`feature`, `fix`, `handoff`, `implementation`, `infra`, `integration`,
`migration`, `product`, `protocol`, `refactor`, `release`, `requirement`,
`review`, `review-verdict`, `review_result`, `review_verdict`, `security`,
`status_note`, and `triage`.

The 10 instance values are:

`CAMBIO`, `CONSULTA`, `COORD`, `DIRECTIVA`, `FIRMA`, `GO`, `RECONCILE`,
`REPORTE`, `RESP`, and `RESPUESTA`.

The exact-commit corpus uses every declared instance value: CAMBIO 3,
CONSULTA 2, COORD 15, DIRECTIVA 35, FIRMA 2, GO 175, RECONCILE 1,
REPORTE 22, RESP 58, and RESPUESTA 6. Policy baseline: 10 declared / 10 in
use / 0 dead.

Two already-present corpus artifacts use the generic `type: artifact`, which
was outside the original 69-value set and accounted for the intervening
221-warning result. Commit `a8e5319f` classifies `artifact` as generic core,
so the final core has 60 values and the required build baseline remains 219.
No instance value was added to core to obtain that count.

## Closed and falsifiable declaration

`NEG-MEMORY-INSTANCE-TYPE-DECLARATION` executes the full attestation boundary:

1. An instance artifact with an undeclared type warns.
2. Editing `extra_type_values` without committing still warns because the
   indexer reads the Git blob.
3. Committing the declaration removes the warning.
4. Committing a mutation that removes the declaration restores the warning.

The falsification inventory discovers the contract beside the permanent test;
the existing CI memory-suite step executes it.

## Exact-commit gates

Detached clean clone of `a8e5319fa98713790cef7e59e94c4115166f9604`
under `D:/Aegis_Scratch/multi_agent_project_protocol/`:

- `python scripts/memory/test_memory_db.py` -> exit 0, 66/66 tests.
- `python scripts/memory/build_memory_db.py --root .` -> exit 0,
  4,277 artifacts and exactly 219 warnings.
- `python scripts/memory/check_memory_db_drift.py --fast --root .` -> exit 0.
- `python scripts/memory/check_memory_db_drift.py --full --root .` -> exit 0.
- `python scripts/check_falsification_contracts.py --root . --inventory` ->
  exit 0, 38 permanent negatives / 38 declared / 0 missing.
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `git diff --check` -> exit 0; `git status --short` -> empty.

Codex is the maker only and did not review or ratify this work.

task_id: TASK-0320
status: in_review
executive_summary: The 10 live instance ceremony types now come only from an attested policy with an empty shipped default and a permanent negative; the exact clean-clone build remains at 219 warnings.
artifacts:
  - path_or_commit: a8e5319fa98713790cef7e59e94c4115166f9604
  - path_or_commit: Area_comun/handoffs/HANDOFF-TASK-0320-codex-to-analista.md
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS
  - command: python scripts/memory/build_memory_db.py --root .
    result: PASS
  - command: python scripts/memory/check_memory_db_drift.py --fast --root .
    result: PASS
  - command: python scripts/memory/check_memory_db_drift.py --full --root .
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
next_recommended: Analista independently recomputes commit a8e5319f against AC1-AC6 and issues a maker-independent verdict.
risks: none.
