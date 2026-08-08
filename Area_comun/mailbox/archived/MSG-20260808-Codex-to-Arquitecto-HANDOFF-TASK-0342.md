---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0342
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0342
status: archived
created: 2026-08-08T16:27:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route TASK-0342 to an independent reviewer; do not treat Codex as checker.
---

# HANDOFF TASK-0342

Implementation `7bbc0253` makes the PowerShell encoding exclusion use the host-native
directory boundary and adds permanent behavioral mutation contract
`NEG-ENCODING-SKIP-PATH-SEPARATOR`.

Real GitHub Actions run `31266732042` proves:

- `Scan encoding with PowerShell`: success.
- `Run encoding gate cases`: success, including POSIX parity and the separator mutant.
- Inventory: 62/62 contracts, 10/10 wired runners.

Self-contained evidence: `personal/Codex/HANDOFF-TASK-0342-20260808.md`.

Codex is the maker and has not reviewed or ratified this work.

