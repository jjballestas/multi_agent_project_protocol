---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0317-remediacion-r4
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0317
status: archived
created: 2026-08-07T01:20:00Z
requires_response: false
---

# ACTION TASK-0317 -- remediacion r4: cambiar un payload por el barrido de familia

Vuelve a `changes_requested` por **un cambio de una asercion**, y el fix funcional NO se toca: sigue
aprobado desde r2 sobre `3d64a7c`.

## Que encontro el checker

Le pedi expresamente que atacara el CONTRATO y no el test -- que buscara si existe otra forma de
mover la exencion que `NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` no cubra. **La hay.** Existe un mutante
que el contrato no caza porque la asercion conductual usa **un unico payload**.

Y no lo dejo en teoria: midio que el **barrido de la familia de 333 cadenas** -- la que ya genera
`test_supported_timestamps_and_medium_priority_are_accepted` -- queda verde sobre `f2c6c315` **y caza
ese mutante (3 de 333)**.

## Lo pedido

En `scripts/memory/test_memory_db.py`: sustituir el payload unico de la asercion conductual por el
barrido de esa familia, que ya existe en el archivo. Nada mas.

## Por que r4 y no cerrar con el hueco declarado

El checker me ofrecio las dos opciones y elijo plegarlo, por coherencia con el criterio que vengo
aplicando: **R-N2 entro en esta tarea precisamente para dar dientes al fix**. Unos dientes que fallan
un mutante **conocido y medido** no son dientes. Cerrar ahora seria declarar cubierto lo que sabemos
que no lo esta.

Es el mismo estandar que hemos aplicado toda la ronda: en 0316 el problema fue codigo muerto que
parecia cobertura; en 0319, un test que mockeaba el formato en discusion. Aqui es una asercion de un
solo caso donde la familia ya estaba disponible.

requested_action: Reclamar TASK-0317, flipearla de changes_requested a in_progress, sustituir en
test_memory_db.py el payload unico de la asercion conductual del contrato por el barrido de la
familia de 333 cadenas que ya genera el test de timestamps soportados, verificar por mutacion que
ahora si caza el caso que se escapaba, recomputar los gates por exit code en clon limpio y dejar la
tarea en in_review con el claim liberado.
