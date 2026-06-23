---
handoff_id: HANDOFF-TASK-0165-codex-to-arquitecto-1
task_id: TASK-0165
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-24T00:30:00+01:00
product_commit: 1493f86
---

# TASK-0165 - Handoff Codex to Arquitecto

## Entrega

- Producto: `D:/Agentes/Zeus/Zeus-protocol`.
- Commit producto: `1493f86 feat(front): add governed agent prompt console`.
- Implementa consola "Operar Agentes" dentro de Operate: combo poblado desde `agent_registry` y workers de producto, textarea de prompt, PII acknowledgement, boton `Enviar`, estado de envio, e hilo read-only por agente.
- Implementa accion gobernada server-side `mailbox-send`: el servidor valida agente real, ASCII/redaccion PII, compone `MSG-...` con `from: Operador`, `relayed_by: Arquitecto`, `to: <agente>`, `type: DIRECTIVE`, `operator_directive: true`, escribe solo `Area_comun/mailbox/open/MSG-*.md`, usa claim file-scoped y entra en auto commit/push si esta habilitado.
- No toca `protocol.config.json`, capacidades vivas, runtime wake/stop ni registry firmado.

## Evidencia

- `node --check src/server.js` OK.
- `node --check public/app.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `git diff --check` OK en producto.
- `npm test` OK: 58/58.
- Smoke local producto puerto 4210 OK: `/healthz` y `/api/protocol/observe`; roster observado `Arquitecto,Codex,Analista,Extractor`.

## Notas de revision

- El envio real usa el mismo endpoint gobernado `/api/protocol/actions/submit`; el front no escribe archivos directos.
- El hilo se deriva del mailbox canonico open/answered/archived y redacta el render con los mismos patrones del intake.
- La respuesta amable AC72 queda cubierta por `friendlyGovernedError`: `ledger-busy` se muestra como `Canal ocupado, intente mas tarde`.
