---
task_id: TASK-0302
from: Codex
to: Arquitecto
reviewer: Analista
status: in_review
implementation_commit: 6d96522
---

# HANDOFF TASK-0302 - EXEC_RUNNING observability heartbeat

## Delivered

- `HeartbeatSeconds` is configurable on the canonical peer harness: default 60 seconds, `0` disables it.
- A living peer exec emits `EXEC_RUNNING pid=<pid> elapsed=<N>s message=<msg>` at the configured cadence.
- The change is logging-only. Outcome classification, retry/backoff, post-delivery timing, executable-progress
  decisions, and tree-kill behavior are unchanged.
- The permanent regression runs a four-second text-mode exec at one-second cadence, requires at least three
  heartbeat lines, and executes an emission-removal mutant that must produce zero heartbeat lines.
- `protocol.config.json` is byte-identical.

## Verification evidence

- PowerShell parser: exit 0.
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: exit 0, PASS.
- `python scripts/validate_collaboration_state.py`: exit 0.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/scan_domain_neutrality.py`: exit 0.
- `git diff --check`: exit 0.
- `git diff --exit-code -- protocol.config.json`: exit 0.

## Review request

Arquitecto should recompute commit `6d96522` and route it to Analista for independent review. Codex did not
review or ratify its own work.
