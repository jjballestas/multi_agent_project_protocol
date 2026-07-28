---
handoff_id: HANDOFF-TASK-0300-codex-to-arquitecto
task_id: TASK-0300
from: Codex
to: Arquitecto
status: ready
created_at: 2026-07-28
implementation_commit: 971741b
---

# TASK-0300 implementation handoff

## Delivered

- `scripts/harness/peer_mailbox_cron.ps1` starts a configurable bounded
  `PostDeliveryTimeoutSeconds` window after it observes signed delivery evidence.
- Expiry emits `POST_DELIVERY_TIMEOUT`, terminates the exec tree, and preserves the
  existing transient retry/backoff behavior.
- Tree termination snapshots descendants, kills deepest-first, applies a root fallback,
  and emits complete/incomplete diagnostics.
- The Codex wrapper and recovery launcher expose the new setting. No process was
  restarted and no other agent harness was edited.

## Independent verification

Recompute commit `971741b`, then run:

```text
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
python scripts/validate_collaboration_state.py
python scripts/scan_encoding.py
python scripts/scan_domain_neutrality.py
git diff --check
```

Observed by the maker: all commands exited 0. The regression bank exercises a simulated
slow post-delivery phase at a two-second bound and a real root/child/grandchild process
tree with zero survivors.

## Review boundary

Codex implemented and tested the change but did not review or ratify it. Arquitecto
should recompute the evidence and route commit `971741b` to Analista for independent
review. Live propagation and cron restart remain a separate coordinated action.
