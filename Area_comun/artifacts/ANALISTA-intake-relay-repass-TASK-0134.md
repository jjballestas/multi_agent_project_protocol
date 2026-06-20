# ANALISTA - RE-PASADA ADVERSARIAL del fix anti-impersonacion (TASK-0134)

> Voz: Analista (escepticismo externo: intento REFUTAR que la impersonacion este cerrada).
> Firma: Analista. Fecha: 2026-06-20. Condicion de cierre del operador (blocking).
> ANCLADO EN CANONICO: clon limpio de Zeus-protocol @ `ffeb558` (arbol limpio); protocolo HEAD==origin
> `b3646d5`. Verifique el codigo y CORRI la suite yo mismo; no asumi al maker ni al checker.
> NO promuevo, NO autoro SPEC, NO muto estado.

## VEREDICTO: PASA. No pude refutar el cierre de la impersonacion (#1).
Intente forjar un evento atestado firmado como Arquitecto por toda via que se me ocurrio; el remedio las
cierra en DOS capas independientes (rechazo de entrada del cliente + execute restringido a intake). Mis
CAMBIOS #3/#4/#5 del veredicto previo estan IMPLEMENTADOS y testeados. #6 queda como NOTA (no bloqueante).

## Reproduccion (clon limpio ffeb558, gate por exit code)
- `npm test` -> **22/22, exit 0** (incl. el test permanente de impersonacion + write real).
- `node --check` server/app/test OK (suite lo cubre).
- Protocolo: `validate_collaboration_state` exit 0, `scan_encoding` exit 0, drift `has_drift=false`
  up_to_seq 830, HEAD==origin.

## Vectores de impersonacion que intente y que el fix CIERRA (server.js @ ffeb558)
| Vector de forja | Resultado | Mecanismo |
|-----------------|-----------|-----------|
| `payload.actorId` (firmar como otro) | **400** | `hasOwnProperty(payload,"actorId")` -> ClientError 400 |
| `payload.intents` (intent arbitrario) | **400** | `hasOwnProperty(payload,"intents")` -> 400; builders server-side |
| Llaves extra top-level (route, etc.) | **400** | `assertAllowedKeys(payload, {actionId,mode,confirm,intake})` |
| Override estructural via `intake.*` (id/owner/type/relayed_by) | **400** | `assertAllowedKeys(intake, {title,narrative,acceptanceIntent,project,piiAcknowledged})` |
| Execute de accion NO-intake (decision/task_status/claim...) | **403** | `if submission.actionId !== "requirement-intake" -> 403` ANTES de runSubmitIntent |
| Spoof de `actionId` para saltar el 403 | imposible | actionId resuelto server-side de GOVERNED_ACTIONS; `submission.actionId = action.id` |
| Path traversal via `file` del task | imposible | `id = REQ-<stableHash hex>`; `file` = `req-<hex>-...md` (solo [0-9a-f]) |
| Inyectar 2do intent (task_status) via intake | imposible | `buildRequirementIntakeIntents` retorna array FIJO (claim->task_upsert requirement->release) |
| Otra ruta de escritura | ninguna | unico POST = `/actions/submit`; `runSubmitIntent` solo se alcanza en intake execute; resto GET |
| Shell injection en intents-json | no | `execFileAsync` (no shell) + `ascii()` + JSON.stringify |
| Prototype pollution (`__proto__` en payload/intake) | **400** | `Object.keys` lista la own-prop -> assertAllowedKeys la rechaza |

El unico camino de escritura real es `requirement-intake` execute, cuyos intents los CONSTRUYE el servidor
con forma fija y atribucion `author:Operador / relayed_by:Arquitecto / endorsement:none`; lo unico que el
cliente influye es el CONTENIDO de title/narrative/acceptanceIntent/project (sanitizado, ASCII, redactado).

## Mis CAMBIOS del veredicto previo: estado
- **#3 accountability -> RESUELTO.** `endorsement:"none"` es campo first-class del task_upsert (no solo
  relayed_by); el evento atestado distingue firmante (Arquitecto) de autor (Operador) y declara NO-aval. El
  test asserta `endorsement=none` en el requirement aterrizado y `deriveIntakeAccountability` en la UI.
- **#4 #4-intacto -> RESUELTO.** El test no se conforma con drift 0: asserta **byte-identidad** de
  `protocol.config.json`, `chain_manifest.json` y `secrets/eventauth-arquitecto.key` ANTES y DESPUES del
  write (epoca/genesis/keys sin cambio). Justo lo que pedi (drift 0 era necesario, no suficiente).
- **#5 verificacion del write real -> RESUELTO.** El test 99 EJERCE el `submit_intent` real contra un clon
  temporal (postJson al server, lee el `TASK_INDEX.json` real): applied:true, drift 0, evento actor=Arquitecto,
  key_id arquitecto-hmac:v1, requirement en TASK_INDEX (type/status/author/relayed_by/endorsement),
  idempotente (reenvio -> 1 sola task). Es test de COMPORTAMIENTO permanente (node --test), no string-match,
  no mock.
- **#2 render honesto -> ATENDIDO (behavior-test).** `deriveIntakeStatus` (dry_run->warn, execute applied->ok)
  y `deriveIntakeAccountability` (actorId Arquitecto -> author:Operador, endorsement:none) testeados; preview
  no se pinta verde; la UI declara firmante=Arquitecto, no "Operador firmo".

## #6 GUARDA PII -> PASA con NOTA (no bloqueante, no es impersonacion)
La redaccion estructural (NIT/razon social/SQL + ASCII) funciona y el test lo prueba (PII cruda ausente del
payload y del task aterrizado). PERO sigue siendo **por patrones (best-effort)**: PII de tercero que no case
esos patrones (nombre de persona, email, telefono, direccion) PASARIA al plano publicable. Recomendacion
permanente (para la SPEC, no bloquea el cierre): que la UI/`pii_guard.mode:"structural"` NO se lea como
"cero-PII garantizado"; declarar best-effort + ack del operador; **DEF-PII (TASK-0118) sigue siendo el gate**
real para citabilidad/publicacion.

## Conclusion
El remedio CIERRA la impersonacion (#1): no encontre via para forjar un evento atestado firmado como
Arquitecto. La prueba negativa permanente es exhaustiva sobre los vectores conocidos y el write real esta
demostrado. #3/#4/#5 resueltos; #2 atendido; #6 nota permanente. **A mi juicio, cerrable.** El cierre formal
(checker) y la decision son del Arquitecto + operador; yo no consolido ni cierro.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre la tarea. Ancle en canonico (ffeb558 / b3646d5), no
  working tree. Corri el write real solo contra clon temporal del propio test (no toca el ledger vivo).
