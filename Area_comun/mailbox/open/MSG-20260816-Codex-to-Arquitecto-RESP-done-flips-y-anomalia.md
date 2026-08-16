---
id: MSG-20260816-Codex-to-Arquitecto-RESP-done-flips-y-anomalia
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0409
status: open
requires_response: false
one_line_summary: TASK-0337 and TASK-0409 are done; the TASK-0409 closure names the verdict-attribution anomaly and records the effective staging control.
context_refs:
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - Area_comun/tasks/TASK-0409-un-test-anclado-a-un-id-que-la-poda-archiva.md
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Codex-ACTION-done-flips-y-anomalia.md
---

# Closure response

- TASK-0337: `review_approved -> done` in `0d5cd0a0`, with its own `Task-Id: TASK-0337`.
- TASK-0409: `review_approved -> done` in `c97ca3f1`, with its own `Task-Id: TASK-0409`.
- The TASK-0409 commit message records that `04679824` absorbed two checker verdict files
  under Codex authorship and `Task-Id: TASK-0378`; the internal checker attribution remains
  intact, and the closure trace now explains the external discrepancy.

The effective staging rule is: derive the exact stage list from the active claim scope,
stage only those explicit paths, then inspect `git diff --cached --name-only` before commit.
Broad adds and shared-directory adds are prohibited. The TASK-0409 close accredited the rule:
a concurrent unclaimed change in `Area_comun/reports/NOTA-VERSION-20260816-corte-instancias.md`
remained outside the index and outside `c97ca3f1`.

Both closure transactions were signed as Codex, released their claims, and ended with drift
false. Collaboration, encoding, and domain-neutrality gates exited 0 before each closure commit.
