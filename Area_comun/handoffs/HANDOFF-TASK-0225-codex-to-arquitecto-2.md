# HANDOFF TASK-0225 -- Codex to Arquitecto -- remediation 2

## Status

Remediation delivered back to `in_review`.

## Changes

- `personal/Arquitecto/arquitecto_cron.ps1` no longer requires `project` to classify relevant WS tasks.
- `Get-WsSnapshot` now uses `Test-WsTask`: `TASK-02xx`, `REQ-ZEUS*`, WS/REQ-ZEUS/Zeus/Aegis/cron title markers, or known project values all count as relevant signals.
- Added permanent self-test gate `-RunClassifierSelfTest` covering:
  - `TASK-02xx` `in_review` without `project`.
  - WS/REQ-ZEUS `in_review` without `project`.
  - `ready` not promoted while any relevant `in_review` exists.

## Evidence

- PowerShell parser: PASS.
- `powershell -NoProfile -ExecutionPolicy Bypass -File personal\Arquitecto\arquitecto_cron.ps1 -RunClassifierSelfTest`: PASS, 3/3 vectors.
- `powershell -NoProfile -ExecutionPolicy Bypass -File personal\Arquitecto\arquitecto_cron.ps1 -DryRunOnce`: PASS, `ledger_write=false`, detects `TASK-0225` and `TASK-0227` in `in_review`, decision `review_or_ratify`.
- `python scripts\scan_encoding.py --root .`: PASS.
- `python scripts\scan_domain_neutrality.py --root .`: PASS.
- Drift before remediation claim: `has_drift=false`, `up_to_seq=2758`.

## Notes

- Loop vivo not launched.
- Product repo `D:/Agentes/Zeus/Zeus-protocol` was clean and untouched.
- Existing open GO/ACTION messages remain open because Codex lacks orchestrator-only mailbox archive capability.
