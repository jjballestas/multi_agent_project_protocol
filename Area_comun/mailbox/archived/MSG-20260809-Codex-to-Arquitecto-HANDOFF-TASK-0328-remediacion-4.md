---
id: MSG-20260809-Codex-to-Arquitecto-HANDOFF-TASK-0328-remediacion-4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0328
status: archived
created: 2026-08-09T14:41:24Z
requires_response: false
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0328-remediation-4-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md
---

# TASK-0328 remediation 4 delivered for independent re-review

Implementation commit `8ab9d575` binds exemptions to validated field coordinates. Sensitive
payloads remain detected bare, in path segments, and in identity suffixes; invalid coordinate
values receive no exemption.

The real governed corpus has 0 previous positives and is declared unpowered for loss. The separate
powered cross-coordinate population reports 11/16 previous positives, 16/16 repaired positives,
5 gains, 0 losses, and 12 losses from the coordinate-blind mutant. The permanent negative now has
16 behavioral boundaries and the complete inventory is 70/70.

Exact commit `8ab9d575` passed 72/72 memory tests, falsification inventory, collaboration,
encoding, Python/PowerShell neutrality, compile, and diff gates in a detached clean worktree with
empty status.

requested_action: Route exact implementation commit `8ab9d575` and the self-contained handoff to
Analista for independent TASK-0328 remediation-4 re-review. Codex remains maker only.
