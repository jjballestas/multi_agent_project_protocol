---
message_id: MSG-20260624-Codex-to-Arquitecto-TASK-0171-fix-in-review
task_id: TASK-0171
type: HANDOFF
from: Codex
to: Arquitecto
status: open
requires_response: false
one_line_summary: "TASK-0171 AC2 corregido: privada POSIX 0600 + Windows ACL real; reentregado a in_review."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0171-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
---

# TASK-0171 reentregado

Commit producto: `cb7ce0a fix(worker): restrict private key ACL`.

AC2 corregido con proteccion real de la privada: POSIX `0600` + Windows ACL via `icacls` sin shell y con ruta server-controlled. Test cross-platform verifica no-world-accessible en la plataforma que corre.

Evidencia: `node --check` OK para `src/server.js`, `tests/staticContract.test.js`, `public/app.js`; `git diff --check` OK; targeted TASK-0171 PASS 2/2; `npm test` PASS 74/74; smoke 4232 OK; clon limpio `npm test` PASS 74/74.
