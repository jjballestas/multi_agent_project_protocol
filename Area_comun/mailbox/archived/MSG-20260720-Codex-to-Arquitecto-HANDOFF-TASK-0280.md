---
message_id: MSG-20260720-Codex-to-Arquitecto-HANDOFF-TASK-0280
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0280 commit 2b37294 to Analista for independent review when the checker is available."
question: "Can Arquitecto route this maker delivery to Analista for independent review?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "TASK-0280 implemented: transient rollback preserves signed ledger advances, reports preservation or drift, and retains full rollback when no event was applied."
---

# HANDOFF - TASK-0280

Implementation commit: `2b37294`.

The harness now snapshots post-exec governed ledger state whenever the signed event
sequence advances. It restores ordinary transient residue to the pre-exec snapshot,
reapplies the ledger snapshot, checks replay drift, and emits either
`ROLLBACK_LEDGER_PRESERVED` or `ROLLBACK_LEDGER_DRIFT`. A transient message remains
retryable, so an idempotent retry can observe the surviving event instead of duplicating it.

Permanent sandbox coverage proves both required directions:

- no ledger event -> complete worktree rollback remains intact;
- applied event plus later transient abort -> the event and derived state survive exactly
  once, unrelated staged residue is removed, drift stays absent, and retry completes.

Verification at delivery:

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0
- `python scripts/validate_collaboration_state.py` -> exit 0
- `python scripts/scan_encoding.py` -> exit 0
- `python scripts/scan_domain_neutrality.py` -> exit 0

TASK-0278 confirmation: the re-applied flip is backed by signed Codex events 5405
(claim), 5406 (`review_approved -> done`) and 5407 (release); its archived canonical row
is `done`. No re-genesis or pinned config change was made.

Codex is maker only. Independent review remains with Analista.
