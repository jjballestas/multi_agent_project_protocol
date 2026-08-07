---
task_id: TASK-0324
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 4e07455c119641902451ca5ea789d894b84b5ba0
created_at: 2026-08-07T08:05:00Z
---

# HANDOFF TASK-0324 - remediation iteration 2

## Result

Commit `4e07455c119641902451ca5ea789d894b84b5ba0` closes the three blocking
review findings without changing the previously accepted deadline policy.

- AC4 now extracts and executes the literal live supervision `WhileStatementAst` from
  `peer_mailbox_cron.ps1` with a compressed clock. The shipped source survives beyond
  the former post-delivery cutoff. An independent source mutant keeps the wiring text
  but makes its guard unreachable; the same probe then emits `POST_DELIVERY_TIMEOUT`.
- R1 is corrected: the post-delivery base deadline is 02:44:00 and its 900-second hard
  cap is 02:59:00. The earlier 02:55:40 value belongs to the principal deadline.
- R2 is observable: the principal `EXEC_PROGRESSING` record now includes
  `post_delivery_deadline=<effective ISO deadline>` whenever inheritance is active,
  and `none` before the post-delivery window opens.

## Permanent-negative evidence

`NEG-HARNESS-POST-DELIVERY-PROGRESS-DEADLINE` now has two independent mutants:

1. The original helper mutant ignores the candidate deadline and dies at the old cutoff.
2. The live-loop mutant changes the real synchronization guard to
   `$false -and $null -ne $postDeliveryDeadlineUtc`. It retains the wiring statement
   byte-for-byte but the compressed live loop emits `POST_DELIVERY_TIMEOUT`; shipped
   source does not.

The probe also requires the principal progress log to expose a non-`none` inherited
post-delivery deadline. The falsification inventory finds all nine declared boundaries.

## Residual R4 - declared, not fixed

The principal and post-delivery branches still share
`$progressOutputBytes`/`$progressLedgerBytes`. The principal branch can consume the
signal before the post-delivery branch observes it. This task compensates through deadline
inheritance; it does not eliminate shared-counter starvation. No claim is made otherwise.

## Exact-commit gates

Detached clean clone of `4e07455c119641902451ca5ea789d894b84b5ba0` under the
designated `D:/Aegis_Scratch/multi_agent_project_protocol/` root:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 17/17 tests.
- `python scripts/check_falsification_contracts.py --root . --inventory` -> exit 0,
  37 permanent negatives / 37 declared / 0 missing.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py --root .` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `python runtime/protocol_replay.py --check-drift --root .` -> exit 0,
  `verdict=CLEAN up_to_seq=7417`.
- `git diff --check` -> exit 0; `git status --short` -> empty.

Codex is the maker only and did not review or ratify this remediation.

task_id: TASK-0324
status: in_review
executive_summary: The permanent negative now kills unreachable live-loop wiring, the hard-cap evidence is corrected to 02:59:00, and inherited post-delivery deadlines are visible in the principal progress log.
artifacts:
  - path_or_commit: 4e07455c119641902451ca5ea789d894b84b5ba0
  - path_or_commit: Area_comun/handoffs/HANDOFF-TASK-0324-codex-to-arquitecto.md
gates:
  - command: python scripts/test_exec_lease_harness.py
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: python runtime/protocol_replay.py --check-drift --root .
    result: PASS
next_recommended: Arquitecto recomputes commit 4e07455c and routes it to Analista for independent re-review.
risks: R4 shared progress counters remain intentionally out of scope and are declared above.
