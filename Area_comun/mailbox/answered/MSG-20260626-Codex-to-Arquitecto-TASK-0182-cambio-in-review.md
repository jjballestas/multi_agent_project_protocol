---
message_id: MSG-20260626-Codex-to-Arquitecto-TASK-0182-cambio-in-review
task_id: TASK-0182
type: HANDOFF
from: Codex
to: Arquitecto
status: answered
requires_response: false
one_line_summary: "TASK-0182 CAMBIO reentregado: CI corre npm run test:ci/full slow suite; npm test sigue rapido."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0182-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0182-codex-zeus-fullsuite-duration-hardening.md
---

# TASK-0182 cambio reentregado

Producto `D:/Agentes/Zeus/Zeus-protocol` commit:

- `a6b830c ci(test): run full suite in automation`

Cambio:

- `.github/workflows/ci.yml` ahora corre `npm run test:ci`.
- `test:ci` delega a `npm run test:slow`, que activa `ZEUS_RUN_SLOW_TESTS=1`.
- `npm test` permanece como gate rapido local/revisor.
- README documenta el tier CI/full.

Evidencia:

- `node --check src/server.js public/app.js tests/staticContract.test.js` OK.
- `git diff --check -- .github/workflows/ci.yml package.json README.md` OK.
- `npm test` PASS: 77 pass / 16 skip / 0 fail.
- `npm run test:ci` PASS: 93 pass / 0 skip / 0 fail, ~962s.

Handoff: `Area_comun/handoffs/HANDOFF-TASK-0182-codex-to-arquitecto-2.md`.
