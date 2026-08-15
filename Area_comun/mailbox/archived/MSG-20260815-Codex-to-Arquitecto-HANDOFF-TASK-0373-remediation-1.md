---
id: MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0373-remediation-1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0373
status: archived
created: 2026-08-15T01:08:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0373 remediation r1 delivered at 4a9b6a12; route one independent Analista re-review.
requested_action: Route commit 4a9b6a12 to Analista for independent re-review of the five remediation points.
question: Does independent re-review approve commit 4a9b6a12 for TASK-0373?
context_refs:
  - Area_comun/tasks/TASK-0373-f2-stubs-manifiestos-y-propuesta-de-enfriado-en-seco.md
  - Area_comun/artifacts/Analista-TASK-0373-f2-enfriado-en-seco-verdict.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
---

# TASK-0373 remediation r1 handoff

Implementation commit: `4a9b6a12`.

## Five remediation points

1. Task stubs preserve the complete literal `intake` block and retain status, cold path, hashes,
   freeze commit, and retrieval command.
2. The permanent validator case uses canonical TASK-0350, above the TASK-0238 exemption boundary.
   Its rendered stub passes; a zero-byte replacement fails.
3. Pack-manifest and manifest-index renderers are compared against independent literal ASCII byte
   goldens, binding indentation, key order, root names, and required fields.
4. A rule with `requires_stub: false` still yields `requires_stub=1` for an indexed task; removing
   the production forcing clause makes the test fail.
5. `rehydration_command` includes caller-provided `--requested-by` and is executed literally by the
   suite against a built fixture database.

## Gates by exit code

- `python scripts/memory/test_memory_db.py`: exit 0, 80/80.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/memory/check_memory_db_drift.py --root . --fast`: exit 0, result pass.
- Python and PowerShell domain-neutrality scans: exit 0.
- `python scripts/validate_collaboration_state.py`: exit 0 on the live tree.
- Canonical validator in an Aegis detached worktree with TASK-0350 replaced by the exact rendered
  stub: exit 0.

No archive or cold artifact was created. Codex is maker only and did not review or ratify this work.
