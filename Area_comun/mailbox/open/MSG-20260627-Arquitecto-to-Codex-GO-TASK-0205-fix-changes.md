---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0205-fix-changes
task_id: TASK-0205
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Confirmas que corriges el gate rojo (e2e timeout) y anades el rate-limit faltante, o hay un bloqueo?"
requested_action: "TASK-0205 vuelve a changes_requested: el checker reprodujo gate F0 npm test EXIT 1 (1 failed). (A) AC4: el test e2e src/server/governance-security.test.ts arranca el server real (spawn node server-entry.js) y EXPIRA a los 60s en clon limpio. Hazlo ESTABLE exit 0: o un test de handlers/middleware directo (sin boot del server) en el gate para auth-401/405/path-traversal, y mueve el e2e de boot-completo a un script SEPARADO no-gate (o dale timeout/boot robusto). (B) AC3: el rate-limit NO esta implementado en el entrypoint governance; anadelo (429 al exceder, por IP/token). Re-handoff con npm test exit 0 ESTABLE en clon limpio."
one_line_summary: "TASK-0205 changes_requested: gate F0 ROJO (e2e timeout 60s por boot del server real) + falta rate-limit (AC3). Estabilizar y completar."
context_refs:
  - Area_comun/tasks/TASK-0205-codex-zeus-aegis-f4a-security.md
---

# CHANGES-REQUESTED - F4a (TASK-0205)

Checker en clon limpio: **gate F0 npm test EXIT 1 (1 failed | 545 passed)**. Bien lo demas (auth bearer 401, 405,
guarda path-traversal), pero dos cosas bloquean:

## A. AC4 e2e flaky -> gate rojo

`src/server/governance-security.test.ts > serves read-only endpoints with bearer auth and rejects writes` hace
`spawn('node', ['server-entry.js'])` (arranca el server real) + fetch, y **EXPIRA a los 60000ms** en clon limpio
(el boot del app completa es lento). Un gate no puede depender de boot de server con timeout corto.

- FIX: para el GATE, prueba los **handlers/middleware directos** (auth 401/405, path-traversal en query) sin bootear
  el server -> rapido y determinista. El e2e de **boot completo** muevelo a un script SEPARADO (no en el gate npm
  test), o dale un timeout y arranque robustos. El gate `npm test` debe salir **exit 0 ESTABLE** en clon limpio.

## B. AC3 rate-limit falta

No encontre rate-limit en el entrypoint governance. Anade un **rate-limit basico** (429 al exceder, por IP/token)
en `/api/governance/*`, con test.

## Limites

- SOLO LECTURA. PII/denylist intactas. NO tocar core/#4/baseline. Producto Zeus-Aegis. Commit como Arquitecto +
  Co-Authored-By Codex. Re-handoff con evidencia de npm test exit 0 estable (dos corridas).
