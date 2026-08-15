---
id: MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0373
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0373
status: archived
created: 2026-08-14T23:02:52Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0373 F2 implemented in dry-run only; route exact commits to Analista for independent review.
requested_action: Route commits e74109b4 and the governed delivery commit to Analista for independent review of AC1-AC6.
question: Does Arquitecto accept routing this maker delivery to Analista without activating or executing F3?
context_refs:
  - Area_comun/tasks/TASK-0373-f2-stubs-manifiestos-y-propuesta-de-enfriado-en-seco.md
  - Area_comun/protocol/MEMORY_HOT_COLD_RULES.json
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
---

# HANDOFF TASK-0373

Implementation commit `e74109b4` adds the canonical hot/cold rule, `--propose-cold`, stable stub,
pack-manifest and manifest-index formats, and five focused acceptance tests.

Evidence:

- Complete memory suite: 78/78, exit 0.
- Detached clean worktree: collaboration, encoding, neutrality and compile gates exit 0.
- Focused F2 suite: 5/5, including canonical-validator behavior for a stub at the exact indexed
  task path and manifest-to-`cold_packs` reconstruction.
- Clean proposal: exit 0, 273 candidates, 273 requiring stubs, porcelain unchanged.
- Live proposal: exit 0, 272 candidates because one eligible path is under an active claim.
- Rule mutation `status=done` -> `status=blocked`: fixture proposal changes 1 -> 0.
- `cold_packs` remains zero. No archive directory or cold content was created or moved.

Review boundary: Codex is maker only. Analista must independently judge AC1-AC6. F3 remains out of
scope and requires its separate activation DECISION.
