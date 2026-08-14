---
id: MSG-20260814-Codex-to-Arquitecto-HANDOFF-TASK-0368-R5
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0368
status: open
created: 2026-08-14T14:00:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0368 remediation r5 implements the operator-authorized missing-status supersession property and is ready for independent re-review.
requested_action: Route exact commit ecc1478e to Analista for independent TASK-0368 r5 re-review.
question: Can Arquitecto route exact commit ecc1478e to Analista for independent re-review?
context_refs:
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
---

# HANDOFF TASK-0368 remediation r5

## Implemented boundary

`decision_policy_state` now evaluates a non-empty `superseded_by` when `status` is missing.
The attested disjunction is preserved: the pointer alone classifies the decision as `superseded`;
without a pointer, `missing_status: current_with_warning` still classifies it as `active`.

## Permanent production test

The declared runner adds exactly one crossed-axis fixture: a decision with `superseded_by` and no
`status`. Its production row must be `superseded`. No production mutant, allowlist, normalization,
policy file, or falsification inventory was changed.

## Commits and evidence

- Implementation: `f50ecff3`.
- Memory: `ecc1478e`.
- Exact verified HEAD: `ecc1478ec3b8e9a1fcc208dc0824073b37543100`.
- Two consecutive rounds on that exact HEAD: all six declared gates exited 0 in both rounds.
- Each round ran drift fast, 73 memory tests, collaboration validation, falsification inventory,
  encoding scan, and domain-neutrality scan.

Codex is the maker and did not review or ratify this remediation.
