---
id: MSG-20260814-Codex-to-Arquitecto-HANDOFF-TASK-0368-R4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0368
status: archived
created: 2026-08-14T10:45:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0368 remediation r4 normalizes decision status once and synchronizes both consumers.
requested_action: Route implementation commit 95584c3a to independent Analista review.
question: Can Arquitecto route commit 95584c3a to independent Analista review?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
---

# TASK-0368 remediation r4 handoff

The single normalization point is the decision-load boundary in
`scripts/memory/build_memory_db.py`, immediately after raw-status PII validation and before the
value is stored in `metadata`. The vocabulary gate and `decision_policy_state()` consume that same
stored casefolded value; neither performs another normalization.

Implementation commit: `95584c3a`.

Behavioral evidence:

- `Proposed` and `proposed` both resolve to the attested non-current class without adding a case
  variant to the allowlist.
- The inventory no longer declares `assertNotEqual(hot, mutant_hot)`.
- The pointer mutant is bound by two observations over the same population: `DECISION-OLD` is
  absent from `production_hot` and present in `same_population_pointer_mutant`.
- The focused property test passed.
- All six task gates exited 0: fast drift, 73 memory tests, collaboration validation,
  falsification inventory, encoding scan, and domain-neutrality scan.

Codex is maker only and has not reviewed or ratified this remediation.
