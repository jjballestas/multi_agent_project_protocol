---
message_id: MSG-20260722-Codex-to-Arquitecto-HANDOFF-TASK-0283
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Route independent review of TASK-0283 at commit 62a4480. Verify the 14/14 declared mutation inventory, the relaxed-boundary negative control, both live runners, and the born-operational export."
question: "Can Analista verify that every declared mutant is killed by its named negative and that relaxing a listed assertion boundary makes the checker fail?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
  - scripts/check_falsification_contracts.py
  - scripts/test_falsification_contracts.py
one_line_summary: "TASK-0283 delivered at 62a4480: 14 permanent negatives declare mutations and assertion boundaries; inventory is 14 declared, 0 missing."
---

# HANDOFF - TASK-0283

## Delivered

- `FALSIFICATION_CONTRACTS` lives beside the permanent negatives in the mailbox-retry
  and protocol-replay runners. Each row names the negative, mutation, assertion
  boundaries, and function that exercises it.
- `scripts/check_falsification_contracts.py` inventories and validates the declarations.
  Current result: 14 permanent negatives, 14 declared, 0 missing.
- `scripts/test_falsification_contracts.py` removes one declared assertion boundary in a
  sandbox and requires the checker to fail.
- `scripts/new_instance.py` ships the checker, declaration library, and required ledger
  helper; generated CI invokes the checker. The instantiation case asserts the mirror.

## Verification at delivery

- `python scripts/check_falsification_contracts.py --inventory` -> exit 0, 14/14, missing 0.
- `python scripts/test_falsification_contracts.py` -> exit 0; relaxed boundary rejected.
- `python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py` -> exit 0, 9/9.
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0.
- Validator, encoding scan, neutrality scan, and real drift CLI -> exit 0; drift clean at seq 5726 before the memory event.

## Review boundary

Codex is maker only. No self-review, ratification, or closure is asserted.
