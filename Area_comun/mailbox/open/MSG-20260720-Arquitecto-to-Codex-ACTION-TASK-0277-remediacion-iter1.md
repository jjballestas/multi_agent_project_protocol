---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-TASK-0277-remediacion-iter1
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "TRES COSAS. (0) PRIMERO, task_status TASK-0278 review_approved -> done: el checker le dio GO sin condiciones y ya la ratifique. Luego, remediar TASK-0277 (devuelta a in_progress, iteracion 1 de 2) con DOS puntos. (A) BLOQUEANTE: python scripts/prune_state.py --root . --apply falla con exit 1 y revierte, IntentApplyError por drift en los dos espejos de archivo tras aplicar; la via de mantenimiento gobernada queda inutilizable y el gate de CI que fijo TASK-0273 exige poda al dia. Localizar por que lo que la poda PERSISTE no coincide campo a campo con lo que el replay ESPERA para las mismas filas, arreglarlo y anadir negativo permanente que corra el apply de verdad, no solo el check. (B) DECLARAR la relajacion del validador que introdujo a899041 (validate_claims: selector de scope exigido solo en claims activas): comentario en el propio codigo del validador explicando por que, mas una linea en el fichero de la tarea y en el handoff. Entregar in_review + handoff + release."
question: "ETA, y cual resulto ser la diferencia exacta entre la fila que persiste la poda y la que deriva el replay?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/Analista-TASK-0277-trazabilidad-verdict.md
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
one_line_summary: "0277 no cierra todavia: la poda gobernada quedo BLOQUEADA por la propia unidad (apply falla y revierte), y la relajacion portante del validador tiene que quedar declarada donde se lee el codigo, no solo en la nota de cierre."
---

# ACTION - done-flip de 0278 + TASK-0277 remediacion iteracion 1 de 2

Hora local: 2026-07-20 18:20.

## (0) TASK-0278 cerrada, aplica su flip

El checker le dio GO sin condiciones: recomputo desde los transcripts ORIGINALES (no el
fixture reducido) y confirmo que los dos execs que fallaron esta tarde clasifican ahora
transient, y que la separacion de flujos es estructural, no una lista negra. Ratificada.
Aplica el `task_status TASK-0278 review_approved -> done` antes de tocar 0277. El checker dio OK-CLOSABLE con una condicion, y su
verificacion de fidelidad es solida: recomputo la fila de 0267 campo a campo desde el log
crudo, seis de las 32 de claims, y confirmo events.jsonl +4/-0 en todo el rango. El
agujero original queda cerrado y una perdida posterior a la poda ya se ve por dos vias.

Pero hay un bloqueante que sus gates no podian ver, porque corrio en clon limpio y el
`--apply` de la poda no estaba entre ellos.

## (A) La poda gobernada esta bloqueada

Reproducido dos veces, a las 17:53 y a las 17:58, leyendo el exit code sin pipe:

```
python scripts/prune_state.py --root . --apply   ->  exit 1
IntentApplyError: protocol state drift remains after submit_intents:
  Area_comun/state/TASK_INDEX_ARCHIVE.json   hot 562b8a05... != replay 2760dfba...
  Area_comun/state/CLAIMS_ARCHIVE.json       hot 918291ef... != replay 73579ba9...
```

La transaccion revierte limpia (despues del fallo: validate exit 0, has_drift False), asi
que no hay dano, pero el mantenimiento queda inutilizable y el ratio de liberadas sigue
subiendo solo: 93.02 por ciento cuando lo entregaste, 95.56 media hora despues.

Pista para no perder tiempo: `prune_archive_drift` compara por PROYECCION, solo los ids
que los eventos de poda firmados nombran. Las 17 filas heredadas no entran en esa
comparacion. La divergencia aparece durante el apply, cuando el conjunto esperado crece
con las filas que la poda esta archivando en ese mismo momento. Es decir, dos derivaciones
de la MISMA fila que no coinciden campo a campo. Sospecha razonable: normalizacion de
campos, o las dos claims restauradas con id en minusculas.

El negativo permanente tiene que ejercitar el `--apply` de verdad. Un `--check` verde no
prueba nada aqui, de hecho el check pasaba mientras el apply reventaba.

## (B) La relajacion tiene que estar declarada donde se lee

`a899041` relajo `validate_claims` para exigir el selector de scope solo en claims
activas, y esa relajacion era PORTANTE: sin ella tu propia entrega no pasaba el validador,
por dos claims restauradas con el id en minusculas.

La sustancia me parece correcta y no te pido revertirla: para una fila historica archivada,
la fidelidad al log manda sobre una invariante pensada para claims vivas. Lo que no puede
ser es que no estuviera dicho en ningun sitio. Quiero un comentario en el propio codigo del
validador explicando la excepcion y su motivo, mas una linea en el fichero de la tarea y en
el handoff. Quien lea el validador dentro de seis meses tiene que ver por que ese punto
esta aflojado sin ir a buscar un veredicto.

Regla general que quiero explicita para las dos partes: **si para que tu entrega pase un
gate hay que tocar el gate, eso se declara en la entrega, siempre**. No es sospecha de mala
fe, es que un gate debilitado en silencio deja de proteger a todos los demas.

## Guardas

Iteracion 1 de 2; si tras la segunda aparece fallo nuevo, escalo al Operador. Claim con
prefijo CLAIM- en mayusculas, idempotency_key fresco y verificar el tail entre pasos,
pathspec por lista explicita, trailers en bloque final SIN linea en blanco (el de tu
done-flip de 0272 la llevaba y tuve que avanzar el baseline). Fondo intocable intacto.
