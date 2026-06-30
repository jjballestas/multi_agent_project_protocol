# Arquitecto Cron Runbook

## Purpose

`personal/Arquitecto/arquitecto_cron.ps1` is the headless operator-launchable harness for the Arquitecto role. It mirrors the Codex and Analista mailbox crons: runtime directory under `.protocol-tmp`, pid/log/seen/lock/stop files, configurable interval, hidden runtime process, prompt passed through stdin, and an operator stop-order detector.

The harness does not mutate the ledger directly. Ledger changes, if any, are made only by the Arquitecto runtime through governed protocol tooling.

## Files

- Harness: `personal/Arquitecto/arquitecto_cron.ps1`
- Prompt source: `personal/Arquitecto/arquitecto_cron.prompt.txt`
- Runtime dir: `.protocol-tmp/arquitecto_cron/`
- Stop marker: `.protocol-tmp/arquitecto_cron/arquitecto_cron.stop`
- Logs: `.protocol-tmp/arquitecto_cron/arquitecto_cron.log`
- Per-run stdout/stderr: `.protocol-tmp/arquitecto_cron/runs/`

## Start

Run only by explicit operator action:

```powershell
powershell -ExecutionPolicy Bypass -File personal\Arquitecto\arquitecto_cron.ps1 -IntervalSeconds 300
```

If the runtime executable is not discoverable, pass it explicitly:

```powershell
powershell -ExecutionPolicy Bypass -File personal\Arquitecto\arquitecto_cron.ps1 -AgentExe "C:\path\to\runtime.exe"
```

## Stop

Create the stop marker:

```powershell
New-Item -ItemType File -Force .protocol-tmp\arquitecto_cron\arquitecto_cron.stop
```

The harness also exits when it sees an operator message to Arquitecto containing a stop order for the Arquitecto cron/monitor.

## Dry Run

One dry-read cycle, no ledger writes:

```powershell
powershell -ExecutionPolicy Bypass -File personal\Arquitecto\arquitecto_cron.ps1 -DryRunOnce
```

Expected output shape:

```json
{
  "mode": "dry_run_once",
  "ledger_write": false,
  "prompt_source": "D:\\Agentes\\multi_agent_project_protocol\\personal\\Arquitecto\\arquitecto_cron.prompt.txt",
  "processable_messages": [],
  "ws_snapshot": {
    "in_review": [],
    "ready": [],
    "codex_in_progress": [],
    "open_mailbox_messages": 0,
    "decision": "no_action"
  }
}
```

The `decision` value is a dry classification only: `review_or_ratify`, `promote_one_ready_task`, or `no_action`.
