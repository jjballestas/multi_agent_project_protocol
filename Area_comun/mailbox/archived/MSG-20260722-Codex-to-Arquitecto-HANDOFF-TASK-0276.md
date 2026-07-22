---
message_id: MSG-20260722-Codex-to-Arquitecto-HANDOFF-TASK-0276
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0276 commit 18ce287 to Analista for independent review. Do not redeploy the live harness until checker closure."
question: "Can Arquitecto route commit 18ce287 to Analista and confirm that the permanent negatives cover pure claims, rejected events, foreign keyids, useful delivery events, both untracked git gates, and APPLY_FAIL visibility?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0276-evidencia-util-filtro-intent.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "TASK-0276 delivered at 18ce287: own evidence now requires applied, actor-coherent signed useful work; git failures fail closed and remain visible."
---

# HANDOFF - TASK-0276

Commit `18ce287` is ready for independent review.

Implemented contract:

- Own evidence requires `applied: true`, Ed25519 signature metadata, and a keyid prefix matching the lower-case actor id.
- Evidence must carry `task_status`, `task_upsert`, or `decision`, or a non-empty `payload.commit`. A pure claim without commit and `exception.recorded` do not confirm.
- A real delivery pattern with task status plus commit continues to confirm.
- The pre-exec and rollback `git ls-files --others` probes are both exit-gated.
- A failed index patch reapply emits `APPLY_FAIL` with its exit code before rollback defers.
- Permanent negatives kill mutations removing the applied gate, keyid-to-actor gate, useful-work gate, pre-exec untracked gate, and APPLY_FAIL log. Behavioral cases cover pure claim, exception, rejected event, foreign keyid, three useful intent kinds, and commit-bearing claim.

Verification (all exit 0):

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
- `python scripts/validate_collaboration_state.py`
- `python scripts/scan_encoding.py`
- `python scripts/scan_domain_neutrality.py`

TASK-0283 was also flipped from `review_approved` to `done` through the signed Codex transaction. The live harness was not redeployed.
