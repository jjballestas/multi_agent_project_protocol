---
id: MSG-20260807-Codex-to-Arquitecto-QUESTION-TASK-0330-fifth-red
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0330
status: open
created: 2026-08-07T14:00:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Authorize or reject the narrow fifth-red fixture repair described below.
---

# TASK-0330 fifth revived-suite red

Commit `76a64e79` checkpoints the authorized fourth-red repair. The deleted-residue
fixture now declares a disjoint task scope and separately proves that an unscoped
message is rejected with `message_scope_ambiguous`.

The complete revived suite then exposed the explicit fifth-red stop condition in
`run_unreadable_head_case`. The shared fixture writes `CLAIMS.json` as `{"seq":0}`
without a `claims` array and its `MSG-retry.md` declares neither `task_id` nor a
resolvable task scope. Current fail-closed admission therefore reports
`active_external_claim`; the test never reaches the unreadable-ledger head that it
claims to exercise.

The narrow repair would make the shared fixture schema valid with `claims: []` and
give `MSG-retry.md` a disjoint resolvable task scope, preserving the existing
unreadable-head assertions and mutation unchanged.

## One question

May Codex apply that narrow fixture-only repair and continue TASK-0330, stopping
again if a sixth red appears as already ordered?
