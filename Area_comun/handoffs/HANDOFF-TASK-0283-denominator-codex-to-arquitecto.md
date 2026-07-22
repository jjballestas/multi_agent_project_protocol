---
handoff_id: HANDOFF-TASK-0283-denominator-codex-to-arquitecto
task_id: TASK-0283
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-22
implementation_commit: 2a52e0c
---

# TASK-0283 remediation handoff - independent denominator

## Delivered

- `PERMANENT_NEGATIVE:` function-docstring markers independently enumerate the permanent
  negative universe. They do not derive from `FALSIFICATION_CONTRACTS`.
- The checker calculates `missing = existing_ids - declared_ids`, reports the computed
  counts, and exits nonzero for missing or stale declarations.
- The guardian self-test injects `NEG-SHADOW` with a permanent-negative marker and no
  contract. It proves exit nonzero and the exact reachable inventory
  `permanent_negatives=2 declared=1 missing=1`.
- `new_instance.py` ships the self-test and generated runtime CI runs it. Repository CI
  runs both the inventory and guardian controls.

## Evidence at implementation commit `2a52e0c`

- `python scripts/check_falsification_contracts.py --root . --inventory` -> exit 0,
  `permanent_negatives=14 declared=14 missing=0`.
- `python scripts/test_falsification_contracts.py` -> exit 0; the undeclared shadow
  control was exercised and rejected.
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0.
- `python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py`
  -> exit 0, 9 cases.
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py`
  -> exit 0.
- Canonical validator, encoding scan, domain-neutrality scan, runtime drift check, and
  `git diff --check` -> exit 0.

## Review boundary

Codex is maker only and does not ratify this work. Please route commit `2a52e0c` to
Analista for independent re-judgement of Q2/Q3 and regression of Q1a/Q4.
