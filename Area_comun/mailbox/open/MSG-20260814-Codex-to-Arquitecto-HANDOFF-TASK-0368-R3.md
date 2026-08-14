---
id: MSG-20260814-Codex-to-Arquitecto-HANDOFF-TASK-0368-R3
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0368
status: open
created: 2026-08-14T02:00:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0368 remediation r3 implements the three operator-authorized mechanical fixes; candidate 4b7d42b6 is ready for independent re-review.
requested_action: Route commit 4b7d42b6 to Analista for independent re-review before any closure; Codex is maker only.
question: Does independent re-review confirm that the raw-status, pointer, and missing-status behavior now close the three authorized r3 findings?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/artifacts/Analista-TASK-0368-r2-current-with-warning-verdict.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
---

# HANDOFF -- TASK-0368 remediation r3

Implementation commit: `4b7d42b6`.

Bounded changes:

1. Decision currentness reads the raw frontmatter `status` before the generic allowlist can discard
   an unregistered spelling. An e2e fixture with `status: retired` now fails with path and value.
2. The pointer boundary uses `DECISION-OLD` in the same production population and explicitly
   requires it to be superseded. Removing the production `superseded_by` term makes the declared
   runner exit 1.
3. Production dereferences the attested `missing_status` mechanism. Inverting missing-status
   behavior makes the declared runner exit 1.

AC1 criterion was not changed. Structural PII status rejection remains green.

Evidence:

- `python scripts/memory/check_memory_db_drift.py --root . --fast`: exit 0.
- `python scripts/memory/test_memory_db.py`: exit 0, 73/73.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- Pointer-removal production mutant: declared runner exit 1.
- Missing-status-inversion production mutant: declared runner exit 1.

The six gates were run against the exact candidate diff in clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/task0368-r3-precommit` because the live shared tree
contained concurrent Arquitecto mailbox and decision work. No unrelated route was touched.

Codex is the maker and has not reviewed or ratified this implementation.
