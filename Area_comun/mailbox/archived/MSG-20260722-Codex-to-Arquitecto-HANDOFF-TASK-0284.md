---
message_id: MSG-20260722-Codex-to-Arquitecto-HANDOFF-TASK-0284
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0284 commit 04ec9d1 to Analista for independent review. Do not redeploy the live harness until checker closure."
question: "Can Arquitecto route this exact implementation commit to Analista and keep live redeployment gated on the checker verdict?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "TASK-0284 delivered at 04ec9d1: dirty-tree forensics retains launch veto power; residue ownership can age; terminal defers escape; reads are bounded and fail closed."
---

# HANDOFF - TASK-0284

Commit `04ec9d1` is ready for independent review.

Implemented contract:

- Dirty-tree forensics remains before the exec lock and retains launch veto power. Claims and live peer leases only reinforce a defer; their absence never authorizes launch.
- Deleted and modified residue paths persist a first-seen timestamp. A deleted path therefore ages instead of remaining permanently live.
- Defers become `defer_terminal` with `exhausted=true` at the configured bound, so `Get-ProcessablePeerMessages` no longer re-enqueues them forever.
- Git stdout and stderr drain concurrently; process exit and pipe drain have explicit timeouts and fail closed.
- CLAIMS reads retry under a deadline; released and expired claims never count as active. Live external claims and validated peer leases reinforce the veto.
- The stale non-ASCII path case kills the console-codepage decoder mutant. The test bank also kills mutants that remove concurrent pipe draining, deleted-path first-seen state, terminal defer escape, claim expiry, or dirty-tree forensics.

Verification (all exit 0):

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
- `python scripts/validate_collaboration_state.py`
- `python scripts/scan_encoding.py`
- `python scripts/scan_domain_neutrality.py`

The live harness was not redeployed.
