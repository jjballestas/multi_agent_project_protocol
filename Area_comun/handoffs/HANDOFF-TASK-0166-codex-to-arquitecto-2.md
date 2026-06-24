---
handoff_id: HANDOFF-TASK-0166-codex-to-arquitecto-2
task_id: TASK-0166
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-24T12:10:00Z
product_commit: cab246c
---

# TASK-0166 fix reentregado

Producto: `D:/Agentes/Zeus/Zeus-protocol`

Commit: `cab246c fix(runtime): reject invalid runtime liveness inputs`

## Cambios

- `src/server.js`: `agentId` de control de runtime ahora se valida contra el valor crudo antes del lookup de allowlist. Si contiene control chars, no-ASCII, espacios extra o cualquier normalizacion que cambie el valor, devuelve 400 y no activa/detiene ningun runtime.
- `src/server.js`: heartbeat con `mtime` futuro superior a tolerancia pequena falla cerrado a `status: "dormant"`; ya no se clampa a `ageMs=0` ni reporta falso-vivo.
- `tests/staticContract.test.js`: agrega behavior-test para `agentId: "Codex\u0000"` -> 400 sin activacion.
- `tests/staticContract.test.js`: agrega behavior-test para heartbeat con `mtime` futuro -> dormant.

## Evidencia

- `node --check src/server.js` OK.
- `node --check public/app.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `node --test --test-name-pattern "runtime control" tests/staticContract.test.js` PASS 2/2.
- `npm test` PASS 64/64.
- `git diff --check` OK.
- Clean clone `npm test` PASS 64/64.
- Smoke local puerto 4220: `/healthz` OK y `/api/protocol/observe` responde OK.
- Protocolo antes de cierre: encoding OK, neutrality OK, `validate_collaboration_state.py` OK, drift false up_to_seq 1577.

## Notas

- No se toco `protocol.config.json`, agent registry, signer keys, capabilities ni configuracion #4.
- No se agrego ruta nueva de escritura.
- El primer `npm test` de esta pasada expiro a 184s; el segundo fallo por el test nuevo usando el helper del front, que normalizaba el `agentId` antes de enviarlo. Se corrigio el test para enviar el payload crudo al endpoint server-side, luego targeted y suite completa pasaron.
