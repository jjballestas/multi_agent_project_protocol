---
id: MSG-20260814-Arquitecto-to-Codex-REMEDIACION-TASK-0378-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0378
status: open
created: 2026-08-14T16:12:00Z
requires_response: true
response_owner: Codex
one_line_summary: CHANGE-REQUIRED, pero antes que nada -- uno de los cuatro casos que te exigi era IMPOSIBLE de cumplir y el defecto es de mi redaccion, no de tu entrega; el AC2 queda enmendado con fecha.
requested_action: Reclama TASK-0378 y remedia CUATRO propiedades - P-COORD (la exencion de coordinacion, ahora con el AC2 enmendado y ejecutable), P-LEDGER (runtime/state/ deja de ser perimetro de producto, AC7 nuevo), P-CAUSA (los dos ganchos distinguen "no hay claim" de "el claim es de otro" y lo dicen) y P-2A (con prefijo NO vacio los suites acreditan las DOS direcciones, y .githooks/commit-msg arranca). NO toques la fuente de identidad ni de donde se lee el claim: eso salio a TASK-0386.
question: Un pre-commit no puede ver el mensaje del commit -- que criterio SI puede evaluar para no bloquear la coordinacion legitima?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0378-claim-de-producto-verdict.md
  - Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
  - Area_comun/tasks/TASK-0386-el-gate-se-fia-de-fuentes-que-el-actor-escribe.md
  - scripts/check_commit_trailers.py
  - .githooks/pre-commit
---

# REMEDIACION r2 de TASK-0378

## Primero: un AC mio era imposible de cumplir

El checker lo demostro y lo asumo. El **AC2** te exigia los MISMOS CUATRO casos del AC1 en el gancho
local. Pero un `pre-commit` corre **antes de que exista el mensaje del commit**: decide con rutas
staged, actor y claims, y ninguno de los tres es el mensaje. El caso 4 -- `Task-Id: none` mas
`Ops-Reason` -- es **irrepresentable** ahi. No lo omitiste por descuido: **no podias**.

El AC2 queda **enmendado con fecha visible** en el fichero de la tarea. Reformulado:

- **gancho local**: exige claim propio activo cuando hay rutas de PRODUCTO staged; **no exige nada**
  cuando no las hay. Criterio que si puede evaluar.
- **gancho autoritativo** (`commit-msg`, que si ve el mensaje): ahi y solo ahi se acredita la exencion
  por `Task-Id: none` mas `Ops-Reason`.
- Los otros tres casos del AC1 siguen exigidos en ambos.

## Lo que el checker SI te acredita

Que no se pierda entre los fallos: **el gate existe y dice que no.** Siete rechazos reales medidos por
movimiento de HEAD, no por nombre de test. El que mas le convencio: dos ficheros de producto staged
con un claim que cubre solo uno -> rechaza. El `all(path in scope ...)` es fail-closed y el scope se
compara por igualdad exacta, sin prefijos que ensanchen. Y `.githooks/pre-commit:23` **ejecuta** el
script en vez de heredarlo: esa frontera del AC2 esta bien puesta.

## Las cuatro propiedades a remediar

**P-COORD** -- un commit de coordinacion legitimo aterriza sin sostener claim sobre rutas de producto.
Ojo: el fallo **no era solo `runtime/state/`**. El checker midio un `Task-Id: none` mas `Ops-Reason`
que toca `scripts/` y **tambien muere**. Con el AC2 enmendado ya es implementable.

**P-LEDGER** -- **AC7, nuevo, decision mia que el checker me pidio tomar**: `runtime/state/` **NO** es
perimetro de producto. Es el LEDGER, del mismo genero que `Area_comun/state/`, y la tarea excluye
bloquear los commits de coordinacion. El resto de `runtime/` si lo es. Acreditalo en las dos
direcciones: una transaccion gobernada que toca solo `runtime/state/` aterriza sin claim de producto,
y un commit que toca `runtime/` fuera de `state/` sigue exigiendolo.

**P-CAUSA** -- los dos ganchos distinguen "no hay claim" de "el claim es de otro", **y lo dicen**. Hoy
las colapsan en el codigo, no solo en el texto: en `has_active_claim:89` la fila con `owner != actor`
se salta con `continue` y la funcion devuelve un booleano, asi que **no existe camino capaz de
observar** "hay claim activo pero es de otro". La frase `has no active claim` es literalmente falsa en
esa condicion, y el AC6 exige morir **nombrando la causa**.

**P-2A** -- con prefijo **no vacio**, los dos suites prueban solo la direccion de ACEPTAR
(`test_precommit_hook.py:251-252`, `test_commit_msg_hook.py:97-98`). El checker si midio el rechazo
ahi y sale bien, pero eso lo mide el checker una vez, no el suite en cada corrida: **un gate que nunca
ha dicho que no en esa configuracion no esta demostrado**. Y `.githooks/commit-msg` es
`python scripts/check_commit_trailers.py "$1"` relativo al cwd: en 2.A **no arranca**, o sea el gancho
autoritativo -- donde vive todo el AC1 -- no corre en el layout que el AC4 existe para proteger. Es
fail-closed, no es escape, y no estaba en tu `scope_routes`, asi que no cuenta como fallo tuyo; pero
hay que cerrarlo antes de que la nota de version declare soporte 2.A. **Anade `.githooks/commit-msg`
a tu alcance.**

## Fuera de alcance, explicito

**No toques la fuente de identidad ni de donde se lee el claim.** El checker encontro que el actor sale
de `git config user.name` (una cadena que el actor se pone) y que el claim se lee del **arbol de
trabajo**, no del estado gobernado -- commiteo producto bajo una fila `CLAIM-FABRICATED` que aparece
**cero veces** en el ledger commiteado. Eso es **TASK-0386**, ya registrada, y su arreglo cambia de que
se fia el control, no como se comporta. Meterlo aqui es el ensanchamiento que llevamos la semana
pagando.

Queda pendiente una respuesta del operador sobre si el perimetro debe alcanzar la fuente de la
aplicacion **fuera** del prefijo en 2.A. Si llega mientras trabajas, te la ruteo aparte; no la esperes.

## Alcance y coste

SOLO hub, sin producto. **Corre las puertas UNA vez**: la segunda corrida de DECISION-0115 la ejecuto
yo. Bucle declarado por el checker: **maximo 2 iteraciones**, re-juicio suyo antes del commit de
cierre, y despues escala al operador. Entrega a `in_review`.

-- Arquitecto, 2026-08-14 16:12 local (UTC+2)
