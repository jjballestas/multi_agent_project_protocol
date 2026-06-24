---
artifact_id: ANALISTA-TASK-0165-v2-mailbox-send-pii-veredicto
task_id: TASK-0165
author: Analista
type: review_verdict
created_at: 2026-06-24
product_commit: cf13e7f
protocol_anchor: e1c2666e0140ecf4e12916bef2181093132f9c32
recommendation: CAMBIO-REQUERIDO
---

# ANALISTA TASK-0165 v2 - mailbox_send / PII / no-bypass

## Veredicto

CAMBIO-REQUERIDO. No cierro TASK-0165.

El slip del MSG invalido queda corregido: `mailbox-send` escribe `requires_response: false`, el MSG generado valida
en copia limpia y el no-bypass basico sigue cerrado. Pero el hilo read-only sigue filtrando PII de terceros fuera de
la familia NIT/razon social/SQL que cubre el test nuevo. El escape es falsable en `public/app.js::buildAgentThread`:
email, telefono, documento, nombre propio, cuenta numerica larga y direccion quedan visibles cuando el mensaje no
contiene SQL que los tape por accidente.

Firma: Analista.

## Ancla canonica

| Item | Valor |
|---|---|
| Producto revisado | `D:/Agentes/Zeus/Zeus-protocol` |
| Commit producto citado | `cf13e7f8ad570f3e1ee375df4491bc50a8faab4b` |
| Protocolo instruccion | `e1c2666e0140ecf4e12916bef2181093132f9c32` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260624-Arquitecto-to-Analista-REVISAR-TASK-0165-v2.md` |
| SPEC | `Area_comun/specs/SPEC-0088-panel-operar-agentes-q2-consola-prompts.md` |

## Reproduccion

| Gate / prueba | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout cf13e7f; npm test` | exit 0, 59/59 |
| Execute propio `mailbox-send` contra servidor temporal y protocolo clonado | exit 0 del harness Node; execute HTTP 200/applied true |
| MSG generado por execute propio, validado en copia limpia | `validate_collaboration_state.py --root <tmp>` exit 0 |
| Payloads negativos no-bypass | `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400`, `routeState=400` |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo limpio sin secretos `python scripts/validate_collaboration_state.py --root <clean clone>` | exit 0 |
| Drift vivo | exit 0, `has_drift=false`, `up_to_seq=1523` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` antes del veredicto | exit 0 |
| #4 `protocol.config.json` | byte-identico, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| MSG validator-valido | PASA | Execute propio escribio `MSG-20260624T002406Z-Operador-to-Codex-agent-prompt-AF168DAE.md`; contiene `requires_response: false`, `operator_directive: true`, sin raw NIT/razon social, y `validate_collaboration_state.py --root <tmp>` salio 0. |
| AC17 no-bypass cliente | PASA | Payloads con `actorId`, `intents` y `route: Area_comun/state/TASK_INDEX.json` devolvieron 400; actor efectivo del execute fue `Arquitecto`; la transaccion solo acquire/release de claim file-scoped y write de mailbox. |
| Prompt saliente PII NIT/razon social/SQL | PASA | El MSG generado desde prompt `NIT 900.123.456 razon social: Cliente Secreto` no contiene `900.123.456` ni `Cliente Secreto`; el test suite cubre ademas SQL. |
| Hilo PII NIT/razon social/SQL | PASA parcial | `buildAgentThread` redaction cubre NIT, `razon social` y SQL. |
| Hilo PII familia amplia | SLIPS | Payload propio `Responder a persona@example.com`, `Llamar a +57 300 123 4567 hoy`, `cedula 123456789 del cliente`, `Juan Perez solicita cambio`, `Cuenta bancaria 1234567890123456 de Juan Perez`, `Direccion Calle 123 #45-67 Bogota` queda visible en `summary` y `body` de `buildAgentThread`. |

## Residuales

- El test nuevo solo asierta NIT/razon social/SQL. No prueba la familia PII que el backend `redactPublicText`
  ya reconocia en mi primera pasada: email, telefono y documento.
- `redactRequirementText` tambien tiene un comportamiento accidental: un SQL puede borrar hasta 80 caracteres y tapar
  PII posterior, dejando restos como `erez`. Eso no es una garantia de redaccion.

## Recomendacion

CAMBIO-REQUERIDO:

1. Unificar `public/app.js::redactRequirementText` con la familia del backend para, como minimo, email, telefono,
   documento y nombre legal/persona; anadir controles positivos de hilo para cada familia.
2. Repetir clean clone `npm test`, execute real de `mailbox-send` con validator sobre el MSG generado, y payloads de
   hilo con PII separada por familia sin SQL que la tape accidentalmente.
