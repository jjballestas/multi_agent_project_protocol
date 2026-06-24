---
handoff_id: HANDOFF-TASK-0166-codex-to-arquitecto-4
task_id: TASK-0166
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-24T13:50:00Z
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 58c713c
---

# TASK-0166 fix4 handoff

## Resultado

Corregido el defecto AC2 de `action` no-string en `/api/protocol/agent-runtime/control`.

`src/server.js::applyRuntimeControlAction` ahora exige `typeof input.action === "string"` antes de cualquier
normalizacion/coercion. Los valores no-string devuelven 400 controlado con `runtime action must be activate or stop`,
sin `TypeError` publico y sin crear heartbeat.

Commit de producto: `58c713c fix(runtime): reject non-string runtime actions`.

## Cobertura permanente

`tests/staticContract.test.js` amplifica el test de runtime control con negativos para:

- `action: ["activate"]`
- `action: { toString: "activate" }`
- `action: 42`
- `action: true`
- `action: null`

Cada caso espera 400, verifica que no exista `Codex.heartbeat`, y confirma que el agente sigue `dormant`.
El happy path string `"activate"` / `"stop"` queda verde.

## Evidencia

- `node --check src/server.js` OK.
- `node --check public/app.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `git diff --check` OK.
- `node --test --test-name-pattern "runtime control" tests/staticContract.test.js` PASS 2/2.
- `npm test` PASS 72/72. Primer intento completo: timeout local a 184s; rerun completo PASS.
- Smoke local `http://127.0.0.1:4173/healthz` OK. `/api/protocol/observe` respondio 200; la proyeccion de smoke fallo por esperar una propiedad legacy `source`, no por error del endpoint.

## Notas de alcance

- No se tocaron `protocol.config.json`, genesis, registry, keys, capabilities ni configuracion #4.
- No se anadio ruta nueva de escritura.
- Los fixes previos de TASK-0166 quedan cubiertos por la misma suite: mtime futuro -> dormant, control-char
  `agentId` -> 400, `agentId` no-string -> 400.
