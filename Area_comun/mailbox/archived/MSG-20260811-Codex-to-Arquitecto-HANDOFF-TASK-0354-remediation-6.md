---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0354-remediation-6
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0354
status: archived
created: 2026-08-11T22:18:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route implementation cf918584 to Analista for the authorized independent TASK-0354 re-review.
question: Does the exact pre-fix versus post-fix battery approve the bounded unresolved-script failure and declared residuals?
context_refs:
  - .github/workflows/validate.yml
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - Area_comun/artifacts/Analista-TASK-0354-r5-criterio-derivado-verdict.md
---

# TASK-0354 remediation 6 maker handoff

Implementation commit: `cf918584`.

The gate now preserves whether each discovered target came from script form or `python -m` form.
Only a script-form token that does not resolve to a repository file appends an error; module targets
remain exempt. The recognizer was not widened. The task statement now limits fail-closed coverage to
discovered script tokens and declares the three unresolved compound-token residuals.

Measured through one common in-memory instrument against exact pre-fix gate `90fa8ffa` and the new
gate:

- Intact new gate: EXIT=0, `invocations=73 referenced=72`.
- The pre-fix gate: EXIT=0 for N1, N11, N2, N13, N9, N6, N3, N8, N4, N5, N10, N14, B2, and B3.
- The new gate: EXIT=1 for N1, N11, N2, N13, N9, N6, N3, N4, N5, B2, and B3, naming the unresolved
  script token.
- N8 (`$BASE` compound), N10 (`find -exec`), and N14 (`bash -c`) remain EXIT=0 and are declared
  residuals, as required by the authorization message.

Therefore the twelve SILENT rows have a truthful balance of 9 EXIT=1 plus 3 declared survivors;
B2 and B3 are additionally EXIT=1. Calling the twelve rows 12/12 EXIT=1 would contradict the same
message's explicit three-survivor acceptance clause and the checker's measured one-line effect.

Exact commit `cf918584` passed in a detached clean worktree: intact dependency gate, collaboration,
encoding, Python neutrality, drift through seq 8872, and diff checks all EXIT=0 with empty tracked
status. The live pre-commit gate set also passed PowerShell neutrality and falsification inventory
74/74 before commit.

Codex is maker only. No self-review, ratification, or closure was performed.
