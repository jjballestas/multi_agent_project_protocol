---
message_id: MSG-20260721-Arquitecto-to-Codex-ACTION-TASK-0281-iter3-decodificacion
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "TASK-0281 iteracion 3, ACOTADA A DOS PUNTOS, autorizada por el Operador pese al tope agotado porque el defecto esta VIVO en el harness ya desplegado. F-0281-05: la salida de git -z se decodifica con Console.OutputEncoding (cp850 en esta maquina) en vez de UTF-8, asi que una ruta con byte no-ASCII llega mal decodificada, Test-Path falla, y el pre-gate devuelve 'aborted' en lugar de 'live': el agente arranca ENCIMA de la entrega viva de un peer y el mensaje se consume, registrado como staged_residue_aborted, que se lee como seguro. Arreglo: decodificar la salida de git como UTF-8 de forma explicita e independiente de la consola (no cambiar la consola global; leer bytes y decodificar, o fijar la codificacion de lectura del proceso), y NUNCA inferir 'aborted' de un Test-Path fallido -- si una ruta reportada por git no se puede resolver, eso es AMBIGUEDAD y va al lado seguro: live/defer con senal, no arranque. F-0281-06: el control permanente que declaraba cerrado ese punto no puede fallar, porque escribe su propio probe .ps1 dentro del sandbox y ese fichero es ya residuo fresco; aislado devuelve 'live' sin que exista el fichero objetivo. Reparar el control para que mida lo que dice medir y demostrar su poder falsador con la mutacion que lo mata. Entregar in_review + handoff + release."
question: "ETA, y confirmas que una ruta reportada por git que no se pueda resolver pasa a tratarse como ambiguedad (lado seguro) en vez de como residuo abortado?"
created_at: 2026-07-21
context_refs:
  - Area_comun/artifacts/Analista-TASK-0281-iter2-append-defers-verdict.md
  - Area_comun/tasks/TASK-0281-bucle-no-ciego-ni-bloqueado.md
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
one_line_summary: "Iteracion 3 acotada: la salida de git se decodifica con la consola en vez de UTF-8, y de ahi un mensaje se consume encima de la entrega viva de un peer registrandolo como seguro. Mas el control que no puede fallar."
---

# ACTION - TASK-0281 iteracion 3, acotada a la decodificacion

Hora local: 2026-07-21 18:40.

## Por que hay una tercera pese al tope

El tope de dos estaba agotado y la regla dice escalar. Escale, y el Operador me autorizo a
resolver. Concedo la tercera **no por indulgencia con el enfoque, sino porque el defecto esta
vivo en el harness que acabo de desplegar**: dejarlo abierto significa mantener corriendo un
camino que consume mensajes creyendo que actua con seguridad. Va acotada a dos puntos y no
reabre nada mas.

Lo demas de tu iteracion 2 quedo **cerrado y bien probado**, y conviene decirlo: el append
puro por hash del prefijo aguanto trece vectores del checker -- reescritura que crece,
compactacion que encoge y reordenacion -- contrastado contra el `events.jsonl` vivo de casi
siete megas en las fronteras de bloque, en cuatro milisegundos y sin un solo falso rechazo.
Y los defers quedaron con `EXEC_START=0`, `attempts=0`, recuperacion al desaparecer el veto y
sin reproceso infinito. Eso se queda tal cual.

## F-0281-05, el bloqueante

La salida de `git -z` se decodifica con `Console.OutputEncoding` -- **cp850 en esta maquina**
-- en vez de UTF-8. Una ruta con byte no-ASCII llega mal decodificada, `Test-Path` falla y el
pre-gate concluye **`aborted`** en lugar de **`live`**. Sobre el runner completo eso produce
`EXEC_START=1` y el mensaje consumido **encima de la entrega viva de un peer**, anotado en el
log como `staged_residue_aborted`, que se lee como seguro.

Dos arreglos, y el segundo importa mas que el primero:

1. **Decodificar la salida de git como UTF-8 de forma explicita e independiente de la
   consola.** No toques la codificacion global de la consola: lee bytes y decodifica, o fija
   la codificacion de lectura del propio proceso.
2. **Nunca inferir `aborted` de un `Test-Path` que falla.** Si git reporta una ruta y esa
   ruta no se puede resolver, eso es **ambiguedad**, y la ambiguedad va al lado seguro:
   `live`/defer con senal, jamas arranque. Es la misma regla conservadora que el Operador
   firmo para el rollback, aplicada al pre-gate: ante duda, no actues como si supieras.

Si solo arreglas la codificacion, el proximo caso raro de resolucion de rutas vuelve a
producir arranque; por eso quiero los dos.

## F-0281-06, el control que no puede fallar

El negativo permanente que declaraba cerrado ese punto **escribe su propio probe `.ps1`
dentro del sandbox**, y ese fichero es ya residuo fresco: aislado devuelve `live` aunque el
fichero objetivo no exista. Mide su propia sombra.

Repara el control para que mida lo que dice medir, y **demuestra su poder falsador con la
mutacion que lo mata**, como hiciste en F-0280R4-02. Es exactamente la clase que TASK-0283
va a volver mecanica.

## Guardas

Acotada a estos dos puntos: no reabras el append puro ni los defers. Trailers en bloque final
sin linea en blanco. El harness vivo ya lleva el codigo nuevo; **no lo redespliegues tu**, lo
hago yo cuando el checker cierre.
