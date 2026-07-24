---
skill_id: session-watchdogs
title: Session watchdogs
version: 0.1.0
neutral_core: true
---

# Session watchdogs

Use this procedure at session start when an operator or local runbook asks for
mechanical monitoring of a shared protocol workspace. The skill is read-only and
grants no authority: it only describes monitors and alert conditions. Any state
change, message move, process action, or lock cleanup still requires the normal
governed procedure for the instance.

## Required Inputs

Define these values from the instance configuration or local runbook before
starting any monitor:

- `<WORKSPACE_ROOT>`: absolute path to the protocol workspace.
- `<MAILBOX_OPEN_DIR>`: open message directory, relative to the workspace.
- `<STATE_DIR>`: state directory, relative to the workspace.
- `<RUNTIME_TMP_DIR>`: runtime temporary directory, relative to the workspace.
- `<LOCAL_REF>`: local ref to watch, usually `HEAD`.
- `<POLL_SECONDS>`: delivery monitor polling interval.
- `<EXEC_STALL_SECONDS>`: maximum age for a run log while a lock is held.
- `<TASK_DELAY_SECONDS>`: maximum age for an actionable request or active
  claim without progress.
- `<MAILBOX_THRESHOLD>`: open message count that triggers a hygiene alert.
- `<ALERT_ON_MESSAGES_TO_COORDINATOR>`: pattern for inbound delivery messages,
  for example `*-to-<COORDINATOR_ROLE>-*`.
- `<SELF_COMMIT_FILTER>`: expression that identifies commits produced by the
  same coordination session and should not wake the delivery monitor.
- `<WORKER_IDS>`: identifiers of workers that may have mailbox loops or
  execution locks.

Use generic role names in configuration. Do not hardcode local project names,
personal agent names, or product-specific paths in the skill body.

## Watchdog 1: Deliveries With Self-Filter

Purpose: wake the coordinator when another participant creates a delivery commit
or opens a delivery message.

Algorithm:

1. Set `base` to `git rev-parse <LOCAL_REF>` inside `<WORKSPACE_ROOT>`.
2. Record current files in `<MAILBOX_OPEN_DIR>` matching
   `<ALERT_ON_MESSAGES_TO_COORDINATOR>`.
3. Loop every `<POLL_SECONDS>` seconds.
4. If the current ref differs from `base`, inspect each commit in
   `base..current` using subject plus body.
5. Ignore commits matching `<SELF_COMMIT_FILTER>`.
6. Emit one alert containing the non-self commit subjects and update `base`.
7. Compare the current mailbox file list with the prior list. Emit one alert for
   new matching files.
8. Stop or return control after the first alert if the local monitor mechanism is
   one-shot; otherwise keep looping with the same deduplication.

Response after an alert:

1. Refresh from the configured remote if the local runbook requires it.
2. Read the referenced messages and task state.
3. Apply the governed reaction for the instance: request review, route a fix,
   acknowledge a question, or promote only the next allowed item.
4. Run configured gates before any commit or ledger write.

## Watchdog 2: Execution Health And Delayed Work

Purpose: detect silent failure modes that do not create delivery output.

For each id in `<WORKER_IDS>`:

1. Resolve the worker loop directory under `<RUNTIME_TMP_DIR>`.
2. If a loop lock exists, find the newest run error log under that loop.
3. If the newest run log age is greater than `<EXEC_STALL_SECONDS>`, emit one
   `HUNG_EXEC` alert for that worker. Reset the alert after the log becomes fresh
   or the lock disappears.
4. If the worker loop process is not alive and there is an actionable open
   message for that worker not recorded as seen, emit one `LOOP_DOWN_WITH_INPUT`
   alert.
5. If an actionable request has been seen for more than
   `<TASK_DELAY_SECONDS>` without a response, delivery commit, or status
   change, emit one `DELAYED_WORK` alert.
6. If an active claim for the worker has been held longer than
   `<TASK_DELAY_SECONDS>` and no execution is currently running, emit one
   `CLAIM_WITHOUT_PROGRESS` alert.

Required analysis before acting on an alert:

1. Read the latest run log for the worker.
2. Check the worker seen-file, active claims, task status, and relevant open
   message.
3. Decide whether the issue is a live long-running execution, a refused request,
   a stale lock, an orphan claim, or a missing response.
4. Use the instance's governed recovery procedure. The watchdog itself must not
   clean locks, kill processes, archive messages, or edit state.

## Watchdog 3: Open Mailbox Accumulation

Purpose: detect when open messages are accumulating faster than they are being
classified.

Algorithm:

1. Count files in `<MAILBOX_OPEN_DIR>` that match the instance message naming
   convention.
2. If the count is greater than or equal to `<MAILBOX_THRESHOLD>`, emit one
   `MAILBOX_ACCUMULATION` alert.
3. Reset the alert after the count drops below the threshold.
4. Repeat every configured mailbox polling interval.

Response after an alert:

1. Classify open messages as live, consumed, answered, superseded, or stale.
2. Run the instance's governed mailbox hygiene procedure during a safe window.
3. Leave live actionable messages open.

## Safety Rules

- Monitors are detectors only.
- Keep all paths and actor names parameterized.
- Prefer file-scoped claims for mailbox work when the instance requires claims.
- Do not turn a monitor alert into a state change without the normal governed
  ledger path.
- Do not let a self-filter hide work from other participants; filter only the
  current coordinator's own commits or explicitly configured auxiliary commits.
- Treat repeated alerts for the same condition as a coordination risk that needs
  a concrete question or a governed recovery action.
