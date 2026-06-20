---
decision_id: DECISION-0052
title: Relay acotado del intake del operador - firma = origen+transporte (NO aval), builders server-side, anti-impersonacion (remediacion de seguridad)
status: accepted
ratified_at: 2026-06-20
date: 2026-06-20
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amends: [DECISION-0051]
relates_to: [DECISION-0051, DECISION-0040, DECISION-0045, DECISION-0046, DECISION-0018]
phase: P2
---

# DECISION-0052 - Relay acotado del intake del operador + anti-impersonacion

> ACCEPTED por el operador (2026-06-20, GO-ratifica-remediacion-relay-v2; verificado en canonico cb18b7b).
> Amends DECISION-0051 (mecanismo de escritura del intake). REMEDIACION DE SEGURIDAD de un defecto critico
> ya mergeado (anomalia DECISION-0018). NO toca el config/genesis/keys (#4 epoca 1.14.0 PINNED, byte-identica).

## Contexto (pasada adversarial del Analista, verificada por el operador y el Arquitecto)
El front canonico (Zeus 42e7931) tenia un DEFECTO DE SEGURIDAD CRITICO:
```
server.js: actorId = action.actorId || payload.actorId || "Arquitecto"   (linea 384)
           intents (no-intake) = payload.intents  (linea 371; solo valida el kind, no la forma)
           endpoint 127.0.0.1 SIN auth
```
-> un POST local (o pagina drive-by a localhost) podia FORJAR una decision/claim/task_status ATESTADO
firmado como Arquitecto. El enforce #4 NO lo para (Arquitecto es firmante valido). Rompe la integridad de la
atestacion. El "no-bypass" previo (string-match de rutas) no protege contra payload.actorId/intents forjados.

## Decision (relay ACOTADO + anti-impersonacion)
1. **El servidor NUNCA confia en el cliente para autoria ni forma.** Se elimina `payload.actorId` y los
   `payload.intents` crudos como fuente. Cada accion gobernada = **builder SERVER-SIDE con forma estricta**:
   construye el intent canonicamente desde campos de datos validados; el cliente no inyecta intents.
2. **Relay acotado:** la firma-como-Arquitecto EN NOMBRE del Operador aplica **SOLO a la forma exacta del
   `requirement-intake`** (`task_upsert` de `type:requirement`, `author:Operador`). Cualquier otro
   intent/forma que intente firmarse como Arquitecto por esta via -> RECHAZADO (prueba negativa permanente).
3. **Firma = ORIGEN + TRANSPORTE, NO AVAL (accountability).** Que el Arquitecto firme el relay significa
   "originado por el Operador, transportado/registrado por el runtime", NO aval tecnico. El aval es la SPEC
   que el Arquitecto autora despues (revision adversarial). Evento: `author:Operador`, `relayed_by:Arquitecto`,
   `endorsement:none`. Un relayado NO cuenta como autorado por el Arquitecto.
4. **#4 intacto y byte-identico:** el relay NO toca `protocol.config.json` (signer set), genesis, keys ni
   `protocol_version`. Se aserta byte-identidad antes/despues (drift 0 es necesario, NO suficiente). Sin
   re-genesis; epoca 1.14.0 PINNED.

## Descartes
- (a) Actor no-firmante: el runtime firma POR `event.actor`; no hay actor sin secreto sin cambiar el modelo.
- (c) Re-genesis para volver al Operador firmante: ceremonia RF-9 roster, DIFERIDA; camino futuro.

## Endurecimiento del endpoint local (recomendado; severidad menor con #1 cerrado)
Con builders server-side + relay acotado, un cliente local ya no puede forjar intents arbitrarios; lo peor que
resta es inyectar una SEMILLA de intake falsa. Follow-on (token de confirmacion/same-origin/loopback-auth en
EXECUTE) contra drive-by; sub-item de TASK-0134, no bloqueante del cierre de #1.

## Boundaries
No toca INTENT_TYPES ni el config ni la epoca. Mantiene un solo writer (submit_intent). Neutralidad intacta.

## Rollback
Deshabilitar la accion intake en el front. La remediacion de #1 (builders server-side, sin trust de
actorId/intents) es un endurecimiento que permanece aunque el intake se apague.
