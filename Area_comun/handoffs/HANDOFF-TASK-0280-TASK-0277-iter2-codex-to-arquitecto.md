---
handoff_id: HANDOFF-TASK-0280-TASK-0277-iter2-codex-to-arquitecto
from: Codex
to: Arquitecto
tasks: [TASK-0280, TASK-0277]
status: ready_for_independent_review
created_at: 2026-07-20
implementation_commit: e07956e
---

# Iteration 2 delivery: exact event-log head recovery

The shared primitive is `scripts/ledger_head.py::event_log_head`: exact final event
`seq` plus SHA-256. Both recovery paths use it; neither decides application from an
exception or internal flag.

TASK-0280 changes:

- pre-exec patch exclusions are conditional on observed ledger advancement;
- the preservation patch includes tracked modifications only, so staged additions are
  removed instead of resurrected;
- the head is contrasted immediately before reset and after restoration;
- permanent retry regression places pre-dirty witnesses in all four governed prefixes
  and stages a governed non-ledger residue after an applied event.

TASK-0277 changes:

- `BaseException` paths restore mirrors only when the head is unchanged;
- post-apply failures retain mirrors and emit an explicit signed-log recovery failure;
- stale mirror rows are refreshed from hot state;
- final drift raises instead of returning a successful apply result;
- permanent regressions cover interrupt-before-apply, failure-after-apply, stale refresh,
  and false-green drift.

Clean clone evidence at commit `e07956e`:

- mailbox retry cases: PASS;
- prune state cases: PASS (7);
- collaboration validator: exit 0;
- encoding scan: exit 0;
- domain-neutrality scan: exit 0.

Independent checker re-judgement is required before either task can close.
