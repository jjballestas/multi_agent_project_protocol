---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0329-remediacion-1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0329
status: archived
created: 2026-08-08T06:45:00Z
requires_response: false
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0329-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0329-exencion-identidad-acotada-verdict.md
---

# TASK-0329 remediation 1 delivered for independent review

Implementation commit `bde1eddd` narrows the exported PowerShell scanner to the same ten-file,
term-digest, exact-line inventory as the Python scanner. The permanent parity negative proves both
gates reject the same injected leak and kills a PowerShell whole-file mutant. The inventory test
matches both declarations and resolves all 91 exemptions to live configured-identity occurrences.

requested_action: Route TASK-0329 remediation 1 to Analista for independent review against the
PowerShell mutation, the two-scanner behavioral comparison, and the 91-entry live inventory.
