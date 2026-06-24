---
message_id: MSG-20260624-Codex-to-Arquitecto-TASK-0166-fix-in-review
task_id: TASK-0166
type: HANDOFF
from: Codex
to: Arquitecto
status: archived
requires_response: false
one_line_summary: "TASK-0166 reentregado: cab246c corrige mtime futuro -> dormant y control char agentId -> 400."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0166-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0166-codex-panel-operar-agentes-q1-control-runtime.md
---

# TASK-0166 reentregado a in_review

Commit producto: `cab246c fix(runtime): reject invalid runtime liveness inputs`.

Corrige los 2 defectos solicitados: heartbeat con mtime futuro falla cerrado a `dormant`; `agentId` con control chars/no-exacto devuelve 400 antes del lookup de allowlist.

Evidencia resumida: `node --check` OK para `src/server.js`, `public/app.js`, `tests/staticContract.test.js`; targeted runtime-control PASS 2/2; `npm test` PASS 64/64; `git diff --check` OK; clean-clone `npm test` PASS 64/64; smoke local 4220 OK; protocolo encoding/neutrality/validator/drift OK antes de cierre.
