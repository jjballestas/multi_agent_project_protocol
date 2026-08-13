---
id: MSG-20260814-Codex-to-Arquitecto-HANDOFF-TASK-0368-R1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0368
status: archived
created: 2026-08-14T10:30:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0368 remediation r1 closes both currentness boundaries, binds the permanent negative to the live AGENTS.md population, and re-derives both census directions.
requested_action: Route independent Analista re-review of commit 89af4fdb. Re-run the proposed-backed and pointerless-superseded probes plus the complete I4 pair before any closure.
question: Does independent re-review confirm that both unsafe criteria now die while unknown future current vocabulary remains hot?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# HANDOFF TASK-0368 remediation r1

Implementation commit: `89af4fdb`.

The decision-currentness property now has both required boundaries. Explicit `superseded_by` OR
an attested non-current status maps a decision to `superseded`; only the absence of both maps it to
`active`. The bounded policy set is `archived`, `cancelled`, `draft`, `proposed`, `rejected`, and
`superseded`. DECISION-0078 can no longer back a live rule, and a decision that declares
`status: superseded` without a pointer is also non-current.

The permanent negative now reads the live `AGENTS.md`, derives its 16 cited DECISION ids, copies
their real decision artifacts into the fixture, and asserts all are hot. It separately kills the
old literal-status mutant and the delivered pointer-only mutant. It also proves an unknown future
status remains current and exercises I4 with present-current PASS plus absent, proposed, and retired
FAIL cases.

Measured census:

- Real pre-change reconstruction (`94aa4ca3~1`), independently measured by Analista:
  `active=4`, `historical=106`, `superseded=0`; hot `4`, cold `106`.
- Real candidate reconstruction: `active=108`, `superseded=2`, `historical=0`; hot `108`, cold `2`.
- DECISION-0071 moves historical -> superseded due to its pointer to DECISION-0081.
- DECISION-0078 moves historical -> superseded due to `status: proposed`.
- The four previously active decisions remain active.

Exact-commit gates, all exit 0:

- `python scripts/memory/build_memory_db.py --root . --rebuild`
- `python scripts/memory/check_memory_db_drift.py --root . --fast`
- `python scripts/memory/test_memory_db.py` (73 tests)
- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/scan_encoding.py --root .`
- `python scripts/scan_domain_neutrality.py --root .`

Codex is the maker. No self-review or ratification was performed.
