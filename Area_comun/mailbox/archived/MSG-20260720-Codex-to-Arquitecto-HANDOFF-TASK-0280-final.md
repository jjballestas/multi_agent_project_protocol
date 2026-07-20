---
message_id: MSG-20260720-Codex-to-Arquitecto-HANDOFF-TASK-0280-final
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0280 commit 9c6f546 to Analista for independent final re-judgement. Do not deploy the live harness before GO."
question: "Can you route the final re-judgement and keep the live harness unchanged until GO?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - scripts/ledger_head.py
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "TASK-0277 is done; TASK-0280 final remediation is committed with event-named path preservation and torn-tail deferral."
---

# HANDOFF - TASK-0280 final remediation

Commit `9c6f546` implements the requested final iteration.

- F-0280R1-01: rollback preservation no longer uses git change type. It derives the
  affected paths from applied events after the captured sequence, including both sides
  of a signed `mailbox_archive`, and excludes only those exact paths while restoring
  pre-exec patches.
- F-0280R1-02: the shared head reader accepts an unterminated malformed final line as a
  torn tail. The harness emits `ROLLBACK_DEFER reason=ledger_torn_tail` and leaves the
  queue untouched.
- Permanent negatives: the retry sandbox proves a staged governed mailbox move survives
  rollback, unrelated pre-dirty governed paths remain intact, and a torn queue defers
  without mutation.
- Verification: mailbox retry cases PASS; collaboration validator exit 0; encoding scan
  exit 0; domain-neutrality scan exit 0; `git diff --check` exit 0.
- TASK-0277 was flipped from `review_approved` to `done` at signed events 5461-5463.

The live harness was not redeployed.
