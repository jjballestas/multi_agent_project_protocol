---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0342-remediation-4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0342
status: open
created: 2026-08-11T13:22:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route the single authorized independent Analista re-judgment of AC4 at implementation commit 14686290; keep AC5 deferred.
question: Does independent review confirm G9a-d red, G6six/G6ord/G6ws green, and truthful measured versus UNMEASURED output?
context_refs:
  - Area_comun/tasks/TASK-0342-la-exclusion-del-gemelo-de-encoding-liga-la-barra-de-windows.md
  - Area_comun/handoffs/HANDOFF-TASK-0342-codex-to-arquitecto.md
  - scripts/scan_encoding.ps1
  - examples/encoding_gate_cases/run_encoding_gate_cases.py
---

# HANDOFF TASK-0342 remediation 4

Implementation `14686290` closes the AC4 gaps identified in the r4 verdict. One PowerShell policy
object is consumed by `Should-Scan` and dumped after consumption. The fixture derives every policy
coordinate and its non-excluded control from effective runtime values; it does not parse the
declaration or reserve `dist`.

Measured on WSL2 Ubuntu with `pwsh 7.4.6` and case-sensitive ext4:

- G9a, G9b, G9c, G9d: caught divergences.
- G6six, G6ord, G6ws: green full-runner controls.
- A4/A7: caught divergences; A5/A8: accepted equivalents.
- Permanent negative: 16 boundaries; repository inventory: 73/73.

The exact implementation passed collaboration, encoding, both neutrality gates, falsification,
inventory, measured WSL2 parity, compile, clean drift through seq 8779, diff, and empty tracked
status in a detached clean worktree. Full evidence and the deferred boundary are in the handoff.

AC5 remains unclaimed and deferred by operator instruction because Actions billing blocks job
admission. Codex requests only the one authorized independent AC4 re-judgment and has not reviewed
or ratified its own work.
