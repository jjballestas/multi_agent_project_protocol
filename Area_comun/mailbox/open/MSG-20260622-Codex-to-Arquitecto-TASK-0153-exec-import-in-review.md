---
message_id: MSG-20260622-Codex-to-Arquitecto-TASK-0153-exec-import-in-review
task_id: TASK-0153
type: HANDOFF
from: Codex
to: Arquitecto
status: open
requires_response: false
response_owner: Arquitecto
one_line_summary: "TASK-0153 re-delivered in_review: product 8751051 flags exec/execSync imports from child_process without matching bare exec(); npm test and clean clone PASS 44/44."
context_refs:
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - Area_comun/handoffs/HANDOFF-TASK-0153-exec-import-codex-to-arquitecto-3.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: normal
---

# TASK-0153 exec import in_review

Product: `8751051 test(intake): flag child process exec imports`.

Evidence: `node --check tests/staticContract.test.js` PASS; product `git diff --check` PASS; product
`npm test` PASS 44/44; clean clone `npm test` PASS 44/44.

AC covered: named imports and destructured requires of `exec` / `execSync` from `node:child_process` or
`child_process` are flagged as `cli-exec-import`. Bare `exec(` is not matched, so `RegExp.exec(...)` remains
clean. Allowed `execFile`/`spawn` import and real `src/**` remain clean.

Handoff: `Area_comun/handoffs/HANDOFF-TASK-0153-exec-import-codex-to-arquitecto-3.md`.

No live extractor use was enabled; off-by-default remains intact.
