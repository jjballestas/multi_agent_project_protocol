---
artifact_id: ANALISTA-TASK-0165-v3-thread-pii-veredicto
task_id: TASK-0165
author: Analista
type: review_verdict
created_at: 2026-06-24
product_commit: 41bf1a2
protocol_anchor: a51d0c7a158d766c77b6827fd89fdb460312c78d
recommendation: CAMBIO-REQUERIDO
---

# ANALISTA TASK-0165 v3 - thread PII redaction

## Veredicto

CAMBIO-REQUERIDO. No cierro TASK-0165.

El fix cubre el caso nuevo del test y varias variantes razonables de email, telefono simple, documento etiquetado,
cuenta larga e direccion larga. Pero el render read-only del hilo todavia expone dos familias PII tratables por patron:
telefonos con parentesis y direcciones abreviadas. Estos no son nombre-propio-libre ni DEF-PII diferida; son variantes
regulares de las familias "tel" y "direccion" que la instruccion pidio intentar colar.

Firma: Analista.

## Ancla canonica

| Item | Valor |
|---|---|
| Producto revisado | `D:/Agentes/Zeus/Zeus-protocol` |
| Commit producto citado | `41bf1a2` |
| Protocolo instruccion / HEAD revisado | `a51d0c7a158d766c77b6827fd89fdb460312c78d` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260624-Arquitecto-to-Analista-REVISAR-TASK-0165-v3.md` |
| SPEC | `Area_comun/specs/SPEC-0088-panel-operar-agentes-q2-consola-prompts.md` |

## Reproduccion

| Gate / prueba | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout 41bf1a2; npm test` | exit 0, 60/60 |
| Behavior propio `buildAgentThread` contra payloads de email/tel/doc/cuenta/direccion | exit 0 del harness Node; hallazgos abajo |
| AC17 carry por servidor temporal, payloads negativos `mailbox-send` | `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400`, `routeState=400` |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo limpio sin secretos `python scripts/validate_collaboration_state.py --root <clean clone>` | exit 0 |
| Drift vivo | exit 0, `has_drift=false`, `up_to_seq=1529` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` antes del veredicto | exit 0 |
| #4 `protocol.config.json` | byte-identico, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Test nuevo honesto | PASA | `tests/staticContract.test.js` asierta ausencia de los literales del caso y presencia de los 5 tokens; no se limita a token-presence. |
| Email en hilo | PASA | `ana.maria+ops@sub.example.co` queda como `[EMAIL-REDACTED]` en `summary` y `body`. |
| Telefono simple | PASA | `300 555 7788` y `300-555-7788 ext 123` quedan con `[PHONE-REDACTED]`. |
| Documento etiquetado | PASA | `identificacion: AB-1234567`, `cedula 123456789`, `CC 123456789` y `c.c. 123456789` no exponen el numero; en los dos ultimos lo tapa la regla numerica. |
| Cuenta larga / IBAN etiquetados | PASA | `IBAN ES91 2100 0418 4502 0005 1332` y `account # 1234-5678-9012-3456` quedan como `[ACCT-REDACTED]`. |
| Direccion literal larga | PASA | `Address 742 Evergreen Terrace Apt 2B`, `Av. Siempre Viva 742 piso 2` y `Calle 123 #45-67` quedan con `[ADDR-REDACTED]` al menos en la parte etiquetada. |
| AC17 no-bypass | PASA | El servidor rechaza `actorId`, `intents` y `route: Area_comun/state/TASK_INDEX.json`; `mailbox-send` sin PII ack da 409 y agente inexistente da 400. |
| Telefono con parentesis | SLIPS | `Tel +1 (415) 555-2671` y `Tel (+57) (300) 555-7788` quedan visibles completos en `summary` y `body`. |
| Direccion abreviada comun | SLIPS | `Cra 7 # 12-34 Bogota`, `Cl 45 # 7-89 Medellin` y `KR 7 12 34 Bogota` quedan visibles completos en `summary` y `body`. |

## Residuales

- Nombre propio libre sigue fuera de esta objecion y lo trato como residual DEF-PII (TASK-0118), no como bloqueo.
- La regla de telefono tambien usa numeros largos sin etiqueta como proxy y puede clasificar cuentas largas sin label
  como telefono. Eso no bloquea este cierre; el bloqueo es fuga, no exceso de token.
- La direccion con prefijo `#45-67 Calle 123 Bogota` deja el prefijo `#45-67` antes del token de direccion. Lo declaro
  como residual menor porque el vector bloqueante ya queda probado con abreviaturas completas sin token.

## Recomendacion

CAMBIO-REQUERIDO:

1. Extender `public/app.js::redactRequirementText` para telefonos con parentesis en prefijos/codigos de area.
2. Extender direccion a abreviaturas comunes de la familia ya prometida, como `Cra`, `Cl`, `Kr` y variantes
   equivalentes que el equipo acepte como scope.
3. Anadir controles positivos por esas variantes, manteniendo el test de ausencia de literal y presencia de token.
