---
task_id: TASK-0336
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-08
---

# TASK-0336 remediation 2 delivery - Bash line continuation is visible to the gate

Implementation commit `e21e617a` closes the single C.1 escape family. The checker preserves
physical-line position before converting path separators, then rejects a direct runner invocation
when an executable Bash line immediately before it ends in an odd backslash and therefore consumes
the invocation through line continuation.

Permanent behavioral coverage rejects the escape through step Bash, implicit Ubuntu Bash, job
defaults, and workflow defaults. It also proves that a comment ending in a backslash remains
accepted. The canonical workflow remains accepted at 8/8 runners and 55/55 contracts;
`NEG-FALSIFICATION-RUNNER-WIRING` now declares 25 boundaries.

The certification remains explicitly limited to static wiring and is not presented as execution
evidence. Its residuals are unchanged. `.github/workflows/validate.yml` was not touched, no new
escape family was absorbed, and no protocol boundary changed.

Full maker evidence and independent review focus are in
`Area_comun/artifacts/Codex-TASK-0336-remediation-2-handoff.md`.

Codex is the maker only and did not review or ratify this remediation.
