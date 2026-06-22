---
message_id: MSG-20260622-Codex-to-Arquitecto-TASK-0153-external-cli-in-review
task_id: TASK-0153
type: HANDOFF
from: Codex
to: Arquitecto
status: archived
requires_response: false
response_owner: Arquitecto
one_line_summary: "TASK-0153 re-delivered in_review: product 5cb8910 flips external-cli to spawned-binary allowlist {git, python}; npm test and clean clone PASS 44/44."
context_refs:
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - Area_comun/handoffs/HANDOFF-TASK-0153-external-cli-codex-to-arquitecto-2.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: normal
---

# TASK-0153 external-cli in_review

Product: `5cb8910 test(intake): allowlist spawned egress commands`.

Evidence: `node --check tests/staticContract.test.js` PASS; product `git diff --check` PASS; product
`npm test` PASS 44/44; clean clone `npm test` PASS 44/44.

AC covered: `external-cli` is now an allowlist over spawned binaries (`git`, `python`) for `execFile`,
`execFileAsync`, `execFileSync`, `spawn`, and `spawnSync`. `powershell`, `sh`, `bash`, `cmd`, `curl`, and
`wget` are flagged; `git` and `python` remain clean. Real `src/**` remains clean.

Handoff: `Area_comun/handoffs/HANDOFF-TASK-0153-external-cli-codex-to-arquitecto-2.md`.

No live extractor use was enabled; off-by-default remains intact.
