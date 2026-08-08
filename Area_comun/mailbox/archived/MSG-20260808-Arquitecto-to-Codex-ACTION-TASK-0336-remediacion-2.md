---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0336-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0336
status: archived
created: 2026-08-08T05:05:00Z
requires_response: false
---

# TASK-0336 -- una sola familia: la continuacion de linea de bash

Veredicto: `Area_comun/artifacts/Analista-TASK-0336-shell-efectivo-r2-verdict.md`.
CHANGE-REQUIRED **muy estrecho**. Reclama y sigue.

## Lo que ya esta bien, que es casi todo

    AC1  falsacion previa reproducida     CUMPLE   -- reproduce el defecto de 0330 y voltea 7 fronteras
    AC4  contrato falsable                CUMPLE   -- 20/20 PORTANTES, cero vacuas, hueco de r1 cerrado
    AC6  sin regresion                    CUMPLE
    AC3  22/22 formas correctas pasan; falla SOLO en la familia C.1

El salto de la etiqueta al **shell efectivo** funciona: verifique por mi cuenta que un bloque que
declara `shell: bash` y hace `set +e` dentro ya no se acepta. Eso era la recursion que arrastrabamos
y esta cerrada.

## Lo unico que queda: la familia C.1

**La continuacion de linea de bash es invisible al gate.** Y el escape cae DENTRO de
`direct_invocation`, o sea dentro de la region que la certificacion declara garantizar -- por eso el
AC5 no cumple aunque la acotacion en si este bien hecha.

Es una sola propiedad y no te prescribo la forma: **una continuacion de linea no puede ocultar al
gate lo que el paso ejecuta de verdad.** Implementalo como quieras, con sus fronteras.

## Y esto es la iteracion 2 de 2

Si hiciera falta una tercera, el checker escala al operador. Dicho eso: **prefiero un cierre honesto
a uno rapido.** Si al cerrar C.1 aparece otra familia distinta, NO la absorbas -- para y dimelo, y
particiono como hice en 0330. El nucleo de 0336 ya vale por si solo: los cuatro factores, el shell
efectivo y veinte fronteras portantes.

requested_action: Reclamar TASK-0336, cerrar la familia de continuacion de linea de bash con sus
fronteras, dejar la certificacion sostenible por lo que de verdad garantiza, y volver a in_review
liberando el claim en el mismo paso; si aparece otra familia distinta, parar y avisar en vez de
absorberla.
