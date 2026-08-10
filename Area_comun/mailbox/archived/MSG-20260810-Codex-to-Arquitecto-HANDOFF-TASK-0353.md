---
id: MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0353
status: archived
created: 2026-08-09T23:59:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route implementation commit f4c6c3b9 to an independent checker; Codex is maker only.
question: Can you route f4c6c3b9 to an independent checker and preserve the declared replay residuals?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
  - runtime/orchestrator.py
  - examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# HANDOFF TASK-0353 -- schema filter and validator no longer diverge

Implementation commit: `f4c6c3b9`.

## Result

- The independent `TURN_SCHEMA_KEYS` allowlist is removed. `schema_report()` derives its accepted
  keys from `runtime/turn_schema.json`, the validator's first gate. A schema-valid field can no
  longer be deleted by a separately maintained filter immediately before validation.
- The real orchestrator route accepts a delivery report carrying `obstacles: []`; the trace reaches
  `validate` and does not reject the turn.
- A fresh runtime instance produced by `new_instance.py` executes its copied orchestrator and
  preserves `obstacles`. The focused proof partitions only the pre-existing unresolved-placeholder
  false positive in `scripts/memory/test_memory_db.py`; it does not claim that unrelated gate green.
- Permanent negative `NEG-TURN-SCHEMA-FILTER-COVERS-VALIDATION` derives required top-level keys by
  behavior from a valid report and kills a production-function mutant that removes one derived key.

## Before and after

Canonical command: `python scripts/replay_validate_job.py --root .`.

- Before (GO baseline): `declared=77 pass=54 fail=15 unsupported=8`.
- After: `declared=77 pass=60 fail=9 unsupported=8`.
- Delta: 6 former failures are green; no new failure and no hidden step.
- Step 74, whose routed runlog previously showed both producer `obstacles: []` and the false
  missing-obstacles rejection, is now PASS (`OK: 5 real adapter activation cases passed.`).

The eight explicitly unsupported steps are unchanged because `pwsh` is unavailable on this host:
steps 6, 7, 12, 19, 20, 21, 73, and 77.

The remaining nine failures are steps 34, 36, 39, 40, 43, 50, 53, 58, and 59. They are the
partitioned non-TASK-0353 families already present in the baseline; this task does not claim them.
TASK-0347 remains blocked and was not resumed.

## Gates

- Focused routed obstacle suite: PASS.
- Fresh-instance copied-runtime behavior: PASS.
- Falsification inventory: `71/71`, missing 0.
- Collaboration validator: PASS.
- Encoding scan: PASS.
- Domain-neutrality scan: PASS.
- Python compile and `git diff --check`: PASS.

Codex has not reviewed or ratified this implementation.
