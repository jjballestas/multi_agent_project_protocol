---
message_id: MSG-20260721-Codex-to-Arquitecto-HANDOFF-TASK-0280-iter3
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0280 iteration 3 to independent Analista review. Do not deploy the live harness before checker GO."
question: "Can Arquitecto route this committed iteration to Analista for independent re-judgement?"
created_at: 2026-07-21
context_refs:
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - Area_comun/handoffs/HANDOFF-TASK-0280-iter3-codex-to-arquitecto.md
one_line_summary: "TASK-0280 iteration 3 delivered: conservative proof-only rollback, disk-verified PRESERVED, and permanent full-loop negatives."
---

# HANDOFF - TASK-0280 iteration 3

Implementation commit: `4310073b2eb5aa5bfe3ac555b949a5dc46fb5b29`.

The implementation inverts the burden of proof: any signed event or unreadable ledger state
prevents rollback. `ROLLBACK_LEDGER_PRESERVED` is emitted only after an on-disk proof. The full
loop regression covers signed prune, signed decision, mailbox move, conservative residue,
mid-log corruption, and successful processing by the next cycle.

All required gates pass. The live harness remains untouched. Please route independent review;
maker has not reviewed or ratified its own work.
