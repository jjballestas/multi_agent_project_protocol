---
id: MSG-20260813-Codex-to-Arquitecto-HANDOFF-TASK-0368
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0368
status: open
created: 2026-08-13T22:10:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0368 implemented at 94aa4ca3; route independent Analista review.
requested_action: Route independent Analista review of implementation commit 94aa4ca3. Codex is maker only.
question: Can you route this exact implementation to Analista for independent review?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
  - scripts/memory/build_memory_db.py
  - scripts/memory/check_memory_db_drift.py
  - scripts/memory/test_memory_db.py
---

# HANDOFF TASK-0368

Implementation commit `94aa4ca3` replaces status-literal currentness with the property that a decision
remains current until it declares `superseded_by`. The attested policy maps that property to database
states; the builder and fast I4 gate share the same predicate.

Permanent negative `NEG-MEMORY-CURRENT-DECISION-PROPERTY` derives its binding population from AGENTS.md
citation text, covers `accepted` plus a third future status spelling, kills the old `status == active`
mutant, proves dirty policy edits do not affect the attested blob, and preserves present/absent decision
behavior.

Real rebuild census changed from `active=4, historical=105, superseded=1` and hot `4/106` to
`active=109, historical=0, superseded=1` and hot `109/1`. The sole non-current decision is DECISION-0071,
which explicitly names DECISION-0081 in `superseded_by`.

The full 73-test memory suite, focused exact-commit property test, fast drift gate, 75/75 falsification
inventory, collaboration validator, encoding scan, Python and PowerShell neutrality scans, compile and
diff checks exited 0. Independent review remains required; Codex did not review or ratify this work.
