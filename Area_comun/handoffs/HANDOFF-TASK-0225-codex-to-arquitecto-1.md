---
handoff_id: HANDOFF-TASK-0225-codex-to-arquitecto-1
task_id: TASK-0225
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-30
commit: a1cecb2
---

# HANDOFF TASK-0225 -- Arquitecto cron headless

## Delivered

- `personal/Arquitecto/arquitecto_cron.ps1`
  - `.protocol-tmp/arquitecto_cron` pid/log/seen/lock/stop/runs state.
  - Configurable `-IntervalSeconds`, `-MaxNoOperatorRounds`, `-AgentExe`, `-ReasoningEffort`.
  - Prompt source wired from `personal/Arquitecto/arquitecto_cron.prompt.txt` and passed by stdin to the runtime.
  - Operator stop-order detector for messages to Arquitecto mentioning a stop order for the Arquitecto cron/monitor.
  - `-DryRunOnce` mode that reads mailbox/state, detects WS candidates, and emits a no-ledger-write decision.
- `personal/Arquitecto/ARQUITECTO_CRON_RUNBOOK.md`
  - Start, explicit runtime path, stop marker, and dry-run commands.

`personal/Arquitecto/arquitecto_cron.prompt.txt` already existed and was not overwritten. The harness uses it as the prompt source; if absent, it falls back to an internal placeholder.

## Evidence

- PowerShell parser: PASS for `personal/Arquitecto/arquitecto_cron.ps1`.
- Dry-run: PASS, `powershell -ExecutionPolicy Bypass -File personal\Arquitecto\arquitecto_cron.ps1 -DryRunOnce` exited 0 and emitted `ledger_write: false`, open Arquitecto messages, WS snapshot, and dry decision.
- `git diff --check` on touched paths: PASS, with the known `runtime/state/snapshot.json` CRLF warning.
- `python scripts\scan_encoding.py --root .`: PASS.
- `python scripts\scan_domain_neutrality.py --root .`: PASS.
- `python scripts\validate_collaboration_state.py --root .`: PASS with pre-existing mailbox warnings only.
- Drift: `has_drift=false`, byte-identical, `up_to_seq=2709` before implementation commit.

## Notes For Review

- The script does not start a live cron in this delivery; launch remains operator-owned.
- The script itself does not write ledger state. It only invokes the configured runtime with stdin prompt.
- `Get-WsSnapshot` is a dry classifier for the harness; the authoritative promotion/review logic remains in the Arquitecto prompt/runtime.
