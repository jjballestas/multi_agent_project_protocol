# DECISION-0052 (DRAFT v2 - REMEDIACION DE SEGURIDAD) - Relay acotado del intake del operador: firma = origen+transporte (NO aval), builders server-side, anti-impersonacion

- status: proposed (DRAFT v2 en personal/Arquitecto; NO promovido; espera ratificacion)
- type: protocol-surface / SECURITY / governance
- amends: DECISION-0051 (refina el MECANISMO de escritura del intake)
- relates: DECISION-0040 (PII), DECISION-0045/0046 (#4), DECISION-0018 (anomalia ya mergeada), RF-9 (re-genesis, diferido)
- proposed_by: Arquitecto · ratifies: Operador
- supersedes_draft: DRAFT-DECISION-0052 v1 (relay sin acotar)

## Por que v2 (pasada adversarial del Analista, verificada por el operador en canonico)
La v1 proponia firmar el intake como Arquitecto en nombre del Operador. La pasada adversarial destapo que
el RELAY ASI NO ESTA ACOTADO y que el front canonico (Zeus 42e7931, que YO aprobe como checker) tiene un
**DEFECTO DE SEGURIDAD CRITICO ya mergeado** (anomalia DECISION-0018):

```
server.js: actorId = action.actorId || payload.actorId || "Arquitecto"   (linea 384)
           intents (no-intake) = payload.intents  (linea 371; solo valida el kind, no la forma)
           endpoint 127.0.0.1 SIN auth
```

-> Un POST local (otro proceso o una pagina drive-by a localhost) puede **forjar una decision/claim/
task_status ATESTADO firmado como Arquitecto**. El enforce #4 NO lo para (Arquitecto es firmante valido; el
claim viaja en la misma tx). Rompe la integridad de la atestacion = el corazon de la tesis. El "no-bypass"
actual es string-match de rutas, no protege contra payload.actorId/intents forjados.

## Decision (mecanismo RELAY ACOTADO + anti-impersonacion)
1. **El servidor NUNCA confia en el cliente para autoria ni forma.** Se elimina `payload.actorId` y los
   `payload.intents` crudos como fuente. Cada accion gobernada tiene un **builder SERVER-SIDE con forma
   estricta**: toma solo campos de datos validados (p.ej. intake: titulo, narrativa, intencion, proyecto) y
   CONSTRUYE el intent canonicamente en el servidor. El cliente no puede inyectar intents arbitrarios.
2. **Relay acotado:** la firma-como-Arquitecto EN NOMBRE del Operador aplica **SOLO a la forma exacta del
   `requirement-intake`** (un `task_upsert` de `type:requirement`, `author:Operador`). Cualquier otro
   intent/forma que intente firmarse como Arquitecto por esta via -> **RECHAZADO** (prueba negativa
   permanente de impersonacion).
3. **Firma = ORIGEN + TRANSPORTE, NO AVAL (accountability).** Que el Arquitecto firme el relay significa
   "este requisito fue originado por el Operador y transportado/registrado por el runtime", NO que el
   Arquitecto lo avale tecnicamente. **El aval es la SPEC que el Arquitecto autora despues** (con revision
   adversarial). El evento marca `author:Operador`, `relayed_by:Arquitecto`, `endorsement:none`. Un relayado
   NO cuenta como autorado por el Arquitecto (test).
4. **#4 intacto y byte-identico:** el relay NO toca `protocol.config.json` (signer set), ni el genesis, ni
   las keys, ni `protocol_version`. Se asercion: genesis/keys/version **BYTE-IDENTICOS** antes/despues (drift
   0 es necesario, NO suficiente). Sin re-genesis; epoca 1.14.0 PINNED.

## Descartes
- (a) Actor no-firmante: el runtime firma POR `event.actor`; no hay actor sin secreto sin cambiar el modelo.
- (c) Re-genesis para volver al Operador firmante: ceremonia RF-9 roster, DIFERIDA; camino futuro.

## Endurecimiento del endpoint local (recomendado; severidad menor con #1 cerrado)
Con los builders server-side + relay acotado, un cliente local YA NO puede forjar intents arbitrarios; lo
peor que resta es inyectar una SEMILLA de intake falsa (un requisito espurio, no un evento de gobierno
forjado). Aun asi, recomiendo un follow-on: token de confirmacion/same-origin/loopback-auth en el endpoint
EXECUTE para mitigar drive-by. Lo trato como sub-item de TASK-0134 (no bloqueante del cierre de #1).

## Honestidad (lente Analista)
La UI declara: "registrado como evento gobernado, FIRMADO por el Arquitecto (runtime) EN NOMBRE del Operador;
firma = origen/transporte, no aval; el aval es la SPEC". Ningun render afirma que el Operador firmo, ni que
el Arquitecto avalo el contenido.

## Rollback
Deshabilitar la accion intake en el front. La remediacion de #1 (builders server-side, sin trust de
actorId/intents) es un endurecimiento que se queda aunque el intake se apague.
