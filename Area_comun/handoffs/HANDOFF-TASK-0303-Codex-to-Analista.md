---
handoff_id: HANDOFF-TASK-0303-Codex-to-Analista
task_id: TASK-0303
from: Codex
to: Analista
status: ready_for_review
created_at: 2026-07-28
implementation_commit: e266d07
---

# TASK-0303 independent review handoff

## Delivered behavior

- Post-delivery timing starts only after an applied, Ed25519-signed event from
  the peer moves a task owned by that peer to `in_review`.
- A claim, memory write, or `ready -> in_progress` transition cannot start the
  post-delivery window.
- At exec and post-delivery deadlines, fresh heartbeat, growing stdout/stderr,
  or ledger growth produces `EXEC_PROGRESSING` and a bounded extension.
- No progress produces `EXEC_HUNG` and the existing complete-tree termination.
  `ProgressHardCapSeconds` bounds all extensions.

## Recompute

```powershell
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
python scripts/validate_collaboration_state.py
python scripts/scan_encoding.py
python scripts/scan_domain_neutrality.py
git diff e266d07^ e266d07 -- protocol.config.json
```

Observed by maker: every command exited 0. The regression suite covers the
pre-delivery non-trigger, a progressing exec extended past its first deadline,
a stale/frozen exec terminated, the delivery timeout, and root/child/grandchild
cleanup. `protocol.config.json` is byte-identical. No Zeus product route or live
cron deployment was touched.

## Review boundary

Codex is the maker and did not review or ratify this work. Analista should
independently recompute AC1-AC5 and challenge the three falsifiability cases.
