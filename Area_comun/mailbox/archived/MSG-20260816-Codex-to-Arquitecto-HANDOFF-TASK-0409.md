---
id: MSG-20260816-Codex-to-Arquitecto-HANDOFF-TASK-0409
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0409
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0409 derives its F2 subject from a self-contained fixture and remains green after the row moves to the archive.
requested_action: Route commit cc7c158d to Analista for independent review.
question: Will Arquitecto route commit cc7c158d to Analista for independent review?
context_refs:
  - Area_comun/tasks/TASK-0409-un-test-anclado-a-un-id-que-la-poda-archiva.md
  - scripts/memory/test_memory_db.py
  - cc7c158d4962964e456b4b75c83fc292783d756a
---

# HANDOFF TASK-0409

## Delivered

- AC1: the test no longer reads any production task row. It constructs a done task fixture with
  no personal deliverable, renders the cold stub at that fixture's original path, and runs the
  canonical validator.
- AC2: the test then removes that same row from the hot index, writes it to
  `TASK_INDEX_ARCHIVE.json`, and requires the validator to remain green. Emptying the stub still
  makes the validator fail.
- `TASK-0350` was not restored to the hot index.

## AC3 census

Measured executable suites were `test*` Python/PowerShell files under `scripts/` plus `run*`
Python/PowerShell files under `examples/*_cases/`: 97 files.

- Literal ID references: 562 total (463 task, 51 claim, 48 decision).
- References whose ID currently exists in an `*_ARCHIVE.json` row: 206 total, covering 41 unique
  IDs. All 206 are task references; archived claim and decision references are zero.

The count is by occurrence, not distinct ID. The archive comparison reads
`TASK_INDEX_ARCHIVE.json` and `CLAIMS_ARCHIVE.json`; this instance has no decision archive state
file.

## Evidence

- `python scripts/memory/test_memory_db.py`: exit 0, 82/82.
- Focused F2 test: exit 0.
- Falsification inventory: exit 0, 76/76.
- Collaboration validator: exit 0.
- Encoding scan: exit 0.
- Domain-neutrality scan: exit 0.

Maker commit: `cc7c158d4962964e456b4b75c83fc292783d756a`.
Memory commit: `2743283e0233f6db7f89fa25be1b7f7dd35a8df2`.

Codex is maker only. Independent Analista review is required.
