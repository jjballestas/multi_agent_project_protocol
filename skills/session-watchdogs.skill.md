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
- `<COORDINATOR_COMMIT_MARKER>`: an exact trailer value generated for the
  current coordination session. The coordinator writes it by convention. Do not derive
  it from Git author, committer, provider, model, or a shared co-author trailer.
- `<WORKER_IDS>`: identifiers of workers that may have mailbox loops or
  execution locks.

Use generic role names in configuration. Do not hardcode local project names,
personal agent names, or product-specific paths in the skill body.

## Watchdog 1: Mailbox Deliveries With A Coordinator Marker

Machine-readable contract used by the shipped proof:

    WATCHDOG_COMMIT_TRAILER = Protocol-Monitor-Origin

Purpose: wake the coordinator when another participant opens a delivery message.
Mailbox filenames are the primary signal because
`MSG-<date>-<sender>-<recipient>-*.md` identifies the sender independently of
Git identity. Commit inspection is secondary context only.

Algorithm:

1. Require a shared-worktree deployment in which the coordinator observes the
   same mailbox and ref that participants update. If that precondition is not
   true, do not use this watchdog until a runbook-defined refresh materializes
   both signals inside the loop. Set `base` to `git rev-parse <LOCAL_REF>`.
2. Record current files in `<MAILBOX_OPEN_DIR>` matching
   `<ALERT_ON_MESSAGES_TO_COORDINATOR>`.
3. Loop every `<POLL_SECONDS>` seconds.
4. Compare the current mailbox file list with the prior list. For every new
   matching filename, parse its sender and recipient from the filename and emit
   one delivery alert. Do this even when its commit has the same author, model,
   provider signature, or co-author trailer as a coordinator commit.
5. If the current ref differs from `base`, inspect each commit in
   `base..current` using subject plus body as secondary context.
6. Ignore a commit only when it has the exact trailer
   `Protocol-Monitor-Origin: <COORDINATOR_COMMIT_MARKER>`. The coordinator must
   add that trailer to every commit it wants filtered during this session, and
   workers should not add it. This is an advisory noise filter, not an identity
   or authorization mechanism: the value is public and copiable. A worker
   commit can be hidden after amend, cherry-pick, squash, or message-template
   inheritance carries the marker. A model or provider trailer is not a
   self-marker.
7. Emit one alert containing the remaining non-self commit subjects and update
   `base`. A mailbox alert from step 4 is never cancelled by this filter.
8. Stop or return control after the first alert if the local monitor mechanism is
   one-shot; otherwise keep looping with the same deduplication.

Before trusting silence, execute the shipped discrimination proof:

```powershell
python scripts/harness/test_session_watchdog_filter.py `
  --scratch-root D:/Aegis_Scratch/<project>/watchdog-filter-proof
```

The proof reads and executes the machine-readable filter contract above. It
creates four real commits with the same Git author and the same historical
`Co-Authored-By: Claude (Opus)` trailer: two coordinator commits carrying the
session marker and two worker
commits without it. One worker commit opens a mailbox delivery. It fails unless
the historical filter reproduces the 4/4 silent failure, the shipped filter
identifies exactly the two coordinator commits, retains both worker commits,
and a real mailbox directory-listing delta emits the alert independently of
commit position.

The commit filter only reduces noise. Its silence is not evidence that no work
was delivered; only the mailbox signal is authoritative for delivery alerts.

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
- Do not let a self-filter hide work from other participants. Filter only the
  exact coordinator marker; never Git author, committer, provider, model, or a
  co-author signature shared by agents.
- Treat repeated alerts for the same condition as a coordination risk that needs
  a concrete question or a governed recovery action.

