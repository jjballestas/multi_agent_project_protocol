---
handoff_id: HANDOFF-TASK-0188-codex-to-arquitecto-1
task_id: TASK-0188
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-26
product_commit: 6220833
---

# HANDOFF TASK-0188 - Codex to Arquitecto

TASK-0188 queda listo para review en `D:/Agentes/Zeus/Zeus-protocol`.

## Implementado

- `scripts/architect-runtime-launcher.mjs`: wrapper off-by-default para usar como `architectBridge.command`.
- Inner configurable por entorno:
  - `ARCHITECT_RUNTIME_COMMAND` obligatorio.
  - `ARCHITECT_RUNTIME_ARGS` como JSON array de strings o lista simple separada por espacios.
  - `ARCHITECT_RUNTIME_LOCK_PATH` opcional para lock/PID de instancia unica.
- Contrato stdin/stdout:
  - lee stdin por flujo y reenvia cada linea al inner.
  - mantiene un inner long-lived, preservando contexto entre turnos.
  - transmite stdout/stderr del inner line-buffered hacia el puente.
- Invariantes:
  - falla closed si no hay inner configurado.
  - no crea identidad, llaves ni registro; pasa el entorno existente al inner.
  - no importa `submit_intent`, `eventlog`, ni escribe `Area_comun/state` o `runtime/state/events.jsonl`.
  - lock/PID impide segunda instancia viva.
  - cierre limpio por EOF de stdin libera lock y termina inner.
- `tests/fixtures/architect-runtime-stub.mjs`: stub determinista para tests, sin Arquitecto real.
- `README.md`: documenta configuracion viva mediante `architect-bridge.runtime.json` con operador presente.

## Evidencia producto

- `node --check scripts\architect-runtime-launcher.mjs tests\fixtures\architect-runtime-stub.mjs tests\staticContract.test.js src\server.js public\app.js` OK.
- `git diff --check -- README.md scripts\architect-runtime-launcher.mjs tests\fixtures\architect-runtime-stub.mjs tests\staticContract.test.js` OK.
- Targeted `npm test -- --test-name-pattern "TASK-0188|TASK-0185 architect bridge|TASK-0186 Architect console|TASK-0187"` PASS: 9 pass / 4 slow skips.
- `npm test` PASS: 86 pass / 20 slow skips / 0 fail.
- `npm run test:ci` PASS: 106 pass / 0 fail.
- Smoke local puerto 4289 OK:
  - `/healthz` -> ok.
  - `/api/protocol/architect-bridge` -> `enabled:false`.
  - `/` contiene `architect-console-root`.

## Notas de review

- Commit producto: `6220833 feat(architect): add runtime launcher`.
- La activacion viva sigue fuera de alcance: requiere configurar el inner real en runtime config con el operador presente.
- No se cambio `architect-bridge.config.json`, `protocol.config.json`, genesis ni flags #4.
