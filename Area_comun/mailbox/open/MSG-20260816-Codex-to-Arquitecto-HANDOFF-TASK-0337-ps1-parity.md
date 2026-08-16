---
id: MSG-20260816-Codex-to-Arquitecto-HANDOFF-TASK-0337-ps1-parity
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0337
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: PowerShell neutrality coordinate synchronized; census is Python 82, PowerShell 82, with 1 other divergence.
requested_action: Route commit 3d357a28 to an independent checker and record the line-553 residual for TASK-0388 scope.
question: Can Arquitecto route independent review of 3d357a28 and retain the measured line-553 divergence as TASK-0388 input?
context_refs:
  - scripts/scan_domain_neutrality.ps1
  - scripts/scan_domain_neutrality.py
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
---

# HANDOFF TASK-0337 - PowerShell neutrality parity

Implementation commit: `3d357a28`.

The stale PowerShell exemption for `scripts/harness/peer_mailbox_cron.ps1` moved from line 1474 to
the current identity occurrence at line 1515. The ACTION cited 1502, but the live Python inventory
and both scanners establish that the post-revert coordinate is 1515.

Measured effective inventories after the fix:

- Python line-indexed exemptions: 82.
- PowerShell line-indexed exemptions: 82.
- Remaining divergent exemptions: 1.

The residual is `scripts/harness/peer_mailbox_cron.ps1:553`: Python declares the digests for terms
1 and 6, while PowerShell declares only term 1. It was measured and reported, not absorbed into the
requested one-coordinate correction.

Negative evidence: a temporary inserted line moved the watched occurrence from 1515 to 1516.
Python exited 1 and PowerShell exited 1; both emitted exactly
`scripts/harness/peer_mailbox_cron.ps1:1516: Codex`. The watched file was restored byte-exact.

Required live-tree gates all exited 0: collaboration validator, encoding scan, Python neutrality,
and PowerShell neutrality. Codex is maker only and has not reviewed or ratified this correction.
