---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0237-hang-proof-npm-test
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-07-02
task_id: TASK-0237
context_refs:
  - Area_comun/tasks/TASK-0237-zeus-aegis-hang-proof-npm-test.md
one_line_summary: "GO a TASK-0237 (hang-proof del npm test en Zeus-Aegis), ya en ready. PRIORIZALA: es la CAUSA primaria de los jams (la suite se cuelga y cada tarea WS la corre)."
requested_action: "Reclamar TASK-0237 y hacer el npm test del producto a prueba de cuelgues segun el archivo de tarea: (1) vitest run SIN watch en el script test; (2) testTimeout/hookTimeout DUROS (falla-rapido, no cuelga); (3) teardown que mata esbuild/node/servidores al salir (mira el ERR_IPC_CHANNEL_CLOSED de 0222 -> teardown de workers; considera --no-file-parallelism si un worker IPC se cuelga); (4) CI=1 en el entorno de test. DoD: npm test en clon limpio TERMINA SIEMPRE (verde o rojo por assertion/timeout), NUNCA cuelga, demostrado N corridas en clon limpio. Reproducir el cuelgue de hoy (run 20260701T222832Z) y probar terminacion acotada. NO enmascarar bugs reales. Entregar a in_review; review Analista con repro; checker Arquitecto."
---

# GO TASK-0237 - hang-proof del npm test (la causa primaria)

Autorizada por el operador; ya en **ready**. **Priorizala sobre 0236**: la evidencia de hoy confirma que la CAUSA
primaria de los jams es que la suite `npm test` del producto **se cuelga** en clon limpio (run `20260701T222832Z`
= npm test colgado, sin avanzar). Como CADA tarea WS corre npm test en clon limpio como gate, un test que cuelga
traba al exec una y otra vez. Arreglar la suite en su origen desatasca todo el pipeline REQ-ZEUS (0229 incluido,
que quedo diferido esperando esto).

Spec completo en `Area_comun/tasks/TASK-0237-zeus-aegis-hang-proof-npm-test.md`. Repo producto `D:/Agentes/Zeus/Zeus-Aegis`.
`scope` producto, no toca el core. Conservar NOTICE MIT. Ambiguedad -> blocked + 1 pregunta concreta.
