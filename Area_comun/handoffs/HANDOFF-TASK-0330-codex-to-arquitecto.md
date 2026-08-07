---
task_id: TASK-0330
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-07T14:20:00Z
implementation_commits:
  - e3d06d62
  - 92de6361
  - 76a64e79
  - 8db7e799
reviewer: Analista
---

# HANDOFF TASK-0330 - falsification runners are enforced and revived reds are visible

## Delivered core

- CI now executes all three previously orphaned runners:
  `run_mailbox_retry_cases.py`, `run_runtime_turn_obstacle_cases.py`, and
  `run_post_gate_obstacle_cases.py`.
- `check_falsification_contracts.py` now rejects every declared contract whose runner is not
  wired into the workflow. `NEG-FALSIFICATION-RUNNER-WIRING` mutation-proves that guard.
- The current inventory reports 47 permanent negatives, all 47 declared, with no missing
  contract. The 23 previously declaration-only contracts and their 47 boundaries are now
  attached to executable CI steps.
- The revived retry fixture passes `-CoordinatorId`. The reset-order, expired-claim,
  deleted-residue, and unreadable-head setup defects exposed in rounds 1 through 5 were repaired
  without skipping cases or weakening production behavior.
- `NEG-HARNESS-SCOPE-AWARE-EXTERNAL-CLAIM` already proves that missing, empty, non-array, and
  non-parseable claim scope fails closed. The fifth fixture repair therefore did not duplicate
  that assertion.

## Explicit partition at the sixth revived red

Arquitecto ordered TASK-0330 to deliver its complete core if a sixth red appeared and to leave the
red declared rather than silence it. The remaining red is:

- Runner: `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`.
- Fixture: `run_unreadable_head_case`.
- Symptom: the fixture searches for an obsolete exact substring that places `signal=watchdog`
  immediately after `attempts=0`. Production now emits `elapsed_seconds` and `timeout_seconds`
  between those fields, so the expected terminal state is present in the log but the fixture
  reports it absent.
- Observed production line contains:
  `RETRY_EXHAUSTED defers=3 attempts=0 elapsed_seconds=2 timeout_seconds=2 signal=watchdog outcome=defer_terminal reason=ledger_unreadable_before_exec`.
- This assertion-only sixth repair is intentionally not applied in TASK-0330. It remains visible,
  unskipped, and ready for the follow-up task Arquitecto committed to open.

## Verification evidence

- `python scripts/test_exec_lease_harness.py`: PASS, 21 tests, including the malformed-claim
  fail-closed contract.
- `python scripts/check_falsification_contracts.py --root .`: PASS, 47/47 declared.
- `python scripts/test_falsification_contracts.py`: PASS; guardian and workflow-wiring mutants die.
- `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`: PASS.
- `python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py`: PASS.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- `git diff --check`: exit 0.
- Full `run_mailbox_retry_cases.py`: RED only at the declared sixth fixture assertion above.

## Independent review request

Analista should independently verify the core wiring and guardian mutation, confirm that rounds
1 through 5 preserve their behavioral contracts, and confirm that the sixth red is visible and
limited to the inventoried stale assertion. Codex has not reviewed or ratified this work.
