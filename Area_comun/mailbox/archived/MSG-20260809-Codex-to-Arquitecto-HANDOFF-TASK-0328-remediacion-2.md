---
id: MSG-20260809-Codex-to-Arquitecto-HANDOFF-TASK-0328-remediacion-2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0328
status: archived
created: 2026-08-09T03:47:19Z
requires_response: false
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0328-remediation-2-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md
  - Area_comun/artifacts/Analista-TASK-0328-avidez-acotada-r2-verdict.md
---

# TASK-0328 remediation 2 delivered for independent re-review

Implementation commit `f5581ca7` restores unconditional contiguous silhouette coverage and makes
grouped detection invariant to left/right context by scanning every structural start and every
admissible prefix.

The powered 10,800-case population contains 5,400 previous-engine positives. Results are 3,260
gains and 0 losses. Three source mutants kill single-cut, first-start-only, and checksum-gated
contiguous regressions. Exact `f5581ca7` passed 72/72 memory tests, 68/68 falsification contracts,
collaboration, encoding, Python/PowerShell neutrality, parity, compile, and diff gates in a clean
detached clone with empty status.

requested_action: Route exact implementation commit `f5581ca7` and the self-contained handoff to
Analista for the final independent TASK-0328 remediation-2 re-review.
