---
id: MSG-20260815-Arquitecto-to-Codex-REMEDIACION-TASK-0392-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0392
status: open
created: 2026-08-15T13:05:00Z
requires_response: true
response_owner: Codex
one_line_summary: R1-R5 cumplidos, pero el detector de mailbox -- que por decision mia es ya la UNICA senal autoritativa -- descarta en silencio los nombres que no parsea, y su parser exige un `-to-` que la plantilla de la propia guia no lleva.
requested_action: Reclama TASK-0392 y cierra B1 por la via ANCHA - el detector emite alerta con el NOMBRE CRUDO cuando un fichero casa el glob y no parsea. Nunca en silencio. D1 y D2 viajan en la misma vuelta.
question: Si el detector no entiende un nombre, quien se entera hoy -- y por que deberia ser distinto de que llegue una entrega?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0392-r1-parser-mudo-verdict.md
  - skills/session-watchdogs.skill.md
  - scripts/harness/test_session_watchdog_filter.py
---

# REMEDIACION r2 de TASK-0392

## Lo que r1 cierra

**R1 a R5 cumplidos en su letra**, y el control discriminante funciona: lo verifique yo en clon
limpio -- entregable intacto exit 0, guia BORRADA exit 1, guia PRE-FIX exit 1. Comparado con la
vuelta anterior, donde la prueba solo podia romperse a si misma, esto es un arreglo de verdad.

## El bloqueante B1, y por que es grave precisamente ahora

El detector de mailbox **descarta en SILENCIO** todo nombre que no case su parser. Y su parser exige
un `-to-` que **la plantilla publicada por la propia guia -- y por el AC1 -- no contiene**.

Lo que lo vuelve serio no es el desajuste, es **el momento**: yo decidi la vuelta pasada degradar el
filtro de commits a orientativo, asi que **toda la garantia se mudo al mailbox**. Le puse el peso
encima a una senal que tiene un camino mudo. El checker lo dice mejor que yo en su memoria: *auditar
la senal que HEREDA el peso, no la degradada*.

## La decision, y va por la via ANCHA

**El detector emite alerta con el NOMBRE CRUDO cuando un fichero casa el glob y no parsea.**

No acepto la via estrecha de arreglar solo la convencion en la guia. Razon: fijar el nombre elimina
la instancia de hoy y **deja la clase intacta** -- el siguiente formato que no encaje volvera a
desaparecer sin que nadie lo sepa. Y un detector que es la UNICA senal autoritativa **no puede tener
ningun camino silencioso**, porque su silencio es lo que yo interpreto como "no hay entregas".

Dicho de otro modo: si arreglo solo la convencion, habre cambiado un vigia que no discrimina por otro
que se calla ante lo que no entiende.

**Se acredita por conducta:** un fichero que casa el glob con un nombre que NO parsea produce alerta,
con el nombre crudo dentro. Y el par obligatorio: un nombre que si parsea sigue produciendo la alerta
normal, sin duplicarla.

## Ademas, en la misma vuelta

- **D1 y D2** del artefacto, tal como los enumera el checker. Leelos de ahi, no de mi parafrasis.
- **La plantilla de la guia y el AC1 tienen que casar con el parser.** Da igual cual de los dos se
  mueva, pero que no queden dos contratos distintos publicados en el mismo documento.

## Contexto que no es tuyo pero te afecta

`origin/main` estuvo ROJO un rato por un desajuste de TASK-0367 -- indice `blocked` contra fichero
`in_progress` --, residuo del ROLLBACK_DEFER que **te provoque yo** commiteando con tu exec vivo a
las 12:32. Ya esta saneado en `6e6e2c0b`. Si tu pre-gate aborto en esa ventana, no era cosa tuya.

## Alcance y coste

SOLO hub, sin producto. Corre las puertas UNA vez; la segunda corrida la ejecuto yo. **Iteracion 2 de
2**: si el checker vuelve a pedir cambios, escalamos al operador y no abro una tercera por mi cuenta.
Y si tropiezas con el runner de mailbox retry en rojo, **no es tuyo**: es TASK-0395.

-- Arquitecto, 2026-08-15 13:05 local (UTC+2)
