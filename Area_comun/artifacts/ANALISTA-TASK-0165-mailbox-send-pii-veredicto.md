---
artifact_id: ANALISTA-TASK-0165-mailbox-send-pii-veredicto
task_id: TASK-0165
author: Analista
type: review_verdict
created_at: 2026-06-24
product_commit: 1493f86
protocol_anchor: 7d1199020a4245ee7d743ac8623449bc3d273a5a
recommendation: CAMBIO-REQUERIDO
---

# ANALISTA TASK-0165 - mailbox_send / PII / no-bypass

## Veredicto

CAMBIO-REQUERIDO. No cierro TASK-0165.

El no-bypass server-side basico pasa: `mailbox-send` rechaza `actorId` e `intents` del cliente, usa actor
server-side `Arquitecto`, limita la accion a claim acquire/release file-scoped y `mailboxWrites`, y valida el
agente contra el roster real. Pero encontre dos escapes falsables en el plano publicable:

1. El MSG generado por `mailbox-send` queda con `requires_response: true` sin `requested_action` ni `question`.
   Al materializar ese MSG en una copia limpia del protocolo, `validate_collaboration_state.py` sale 1. Esto
   rompe el canonico en el primer envio real.
2. El hilo read-only del front no redacta toda la familia PII que el backend ya reconoce. `buildAgentThread`
   deja visibles email, telefono, documento y nombre propio en respuestas del mailbox.

Firma: Analista.

## Ancla canonica

| Item | Valor |
|---|---|
| Producto revisado | `D:/Agentes/Zeus/Zeus-protocol` |
| Commit producto citado | `1493f86 feat(front): add governed agent prompt console` |
| Protocolo instruccion | `7d1199020a4245ee7d743ac8623449bc3d273a5a` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260624-Arquitecto-to-Analista-REVISAR-TASK-0165.md` |
| SPEC | `Area_comun/specs/SPEC-0088-panel-operar-agentes-q2-consola-prompts.md` |

## Reproduccion

| Gate / prueba | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout 1493f86; npm test` | corrida 1 exit 1: fallo ajeno en local-vlm `127.0.0.5 must be accepted`; corrida 2 exit 0, 58/58 |
| Dry-run propio contra servidor temporal `POST /api/protocol/actions/submit` action `mailbox-send` | exit 0 del harness Node; `dryRun=200`, `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400` |
| MSG generado por dry-run, escrito en copia limpia de protocolo y validado | `validate_collaboration_state.py --root <tmp>` exit 1 |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo limpio sin secretos `python scripts/validate_collaboration_state.py --root <clean clone>` | exit 0 |
| Drift vivo | exit 0, `has_drift=false`, `up_to_seq=1514` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` antes del veredicto | exit 0 |
| #4 `protocol.config.json` | byte-identico, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| AC1 combo desde roster real | PASA | `loadAgentRoster` lee `protocol.config.json` `agent_registry` y suma workers de producto; dry-run `badAgent=400` para `Ghost`; UI usa `model.agents.registry` para poblar el select. |
| AC2 / AC17 no-bypass cliente | PASA | Payloads con `actorId:"Codex"` e `intents:[...]` devolvieron 400; la respuesta dry-run fija `actorId:"Arquitecto"` y `directLedgerWrites:false`. |
| AC2 mailbox_send solo salida mailbox gobernada | PASA con limite declarado | La transaccion contiene solo `claim acquire` y `claim release` file-scoped sobre `Area_comun/state/CLAIMS.json#CLAIM-FRONT-MAILBOX-SEND-*` y el MSG concreto; no crea `task_upsert`, `decision`, `task_status` ni capability. |
| AC2 prompt no concede autoridad nueva | PASA | `operator_directive:true` queda en el MSG; no modifica `protocol.config.json`, registry ni capabilities; actor efectivo sigue siendo server-side `Arquitecto`. |
| MSG mailbox bien formado | SLIPS | El contenido generado incluye `requires_response: true` y `response_owner: Codex`, pero no incluye `requested_action` ni `question`. Al escribirlo en `Area_comun/mailbox/open/` de una copia limpia, el validador falla con: `Mailbox message requires response but has no requested_action` y `Compact mailbox message requires response but has no question`. |
| AC3 prompt ASCII y redaccion | PASA parcial | Prompt propio con `NIT 900.123.456` y `SELECT * FROM dbo.saldos` sale en el MSG como `[NIT-REDACTED]` y `[SQL-REF-REDACTED]`; no contiene raw NIT ni raw SQL. |
| AC4 hilo read-only canonico | PASA | `buildAgentThread` consume `mailbox.open/answered/archived`, filtra por `to/from` del agente y solo renderiza; no escribe. |
| AC4 hilo no expone PII | SLIPS | Payload propio con `persona@example.com`, `+57 300 123 4567`, `cedula 123456789` y `Juan Perez` queda sin redactar por `public/app.js::redactRequirementText`; el backend `src/server.js::redactPublicText` si cubre email/phone/document/proper_name. |
| AC5 error amable | NO BLOQUEANTE | No encontre regresion nueva: el flujo reutiliza `friendlyGovernedError`; el foco de esta pasada no era AC72 completo. |
| AC6 #4 byte-id / sin riesgo config | PASA | `protocol.config.json` byte-identico; hash arriba. |

## Residuales

- La primera corrida de `npm test` fallo por el caso local-vlm `127.0.0.5`; la repeticion completa fue verde.
  No lo uso como bloqueo principal porque el escape de MSG invalido es determinista y suficiente.
- `mailbox-send` acepta `messageType:"QUESTION"` pero `buildMailboxSendMarkdown` escribe siempre `type: DIRECTIVE`.
  No lo elevo a bloqueo separado porque la UI no expone selector de tipo y el defecto es DIRECTIVE, pero conviene
  alinear el contrato si se mantiene `messageType`.

## Recomendacion

CAMBIO-REQUERIDO:

1. Hacer que el MSG generado sea valido para el canonico: o `requires_response: false`, o incluir
   `requested_action` y `question` coherentes cuando se use rr=true.
2. Unificar el redactor del hilo con la familia del backend (`email`, `phone`, `document`, `proper_name`, ademas de
   NIT/legal/sql), o mover el render del hilo a un campo ya saneado por el lector canonico.

Tras el cambio, repetir: clean clone producto `npm test`, payload dry-run de `mailbox-send`, validator contra un MSG
generado materializado en copia limpia, y payload de hilo con email/telefono/documento/nombre.
