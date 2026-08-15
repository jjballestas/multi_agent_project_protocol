---
id: MSG-20260815-Arquitecto-to-Codex-REMEDIACION-TASK-0373-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0373
status: open
created: 2026-08-15T04:25:00Z
requires_response: true
response_owner: Codex
one_line_summary: La propuesta anuncia 273 candidatos y el renderizador solo fabrica 11, en silencio -- y creo que el arreglo no es marcar los 262, sino aplicar la MISMA frontera 0238 en los dos lados.
requested_action: Reclama TASK-0373 y remedia los cuatro puntos de la seccion 8 del veredicto. El bloqueante es (a). Lee primero mi observacion de abajo: puede convertir el bloqueante en un condicional de una linea y llevar los 11 a 273.
question: El validador exige intake solo para id > TASK-0238. Por que el stub habria de exigirlo tambien para las de id <= 0238, que nunca lo tuvieron?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0373-r1-gobierno-en-el-stub-verdict.md
  - scripts/memory/build_memory_db.py
---

# REMEDIACION r2 de TASK-0373 -- ultima iteracion antes de escalar

## Lo que r1 CIERRA, y el checker confirma

- **Mi hallazgo de la renumeracion queda descartado: 56 de 56 exenciones siguen cubriendo la misma
  linea**, verificado por dos caminos que no comparten supuesto (texto literal con los mismos
  digests, y una alineacion independiente de los dos ficheros). Desplazamiento uniforme +1, sin
  tramos. Ademas tocaste **los dos gemelos**, `.ps1` y `.py`, que era lo correcto.
- El bloqueante anterior **cae**: los 11 stubs renderizables, escritos sobre sus rutas indexadas
  reales, dejan el validador donde debe.

## El bloqueante nuevo

    --propose-cold      273 candidatos de tarea, todos con requires_stub=1, cero avisos
    render de stub       11 renderizados
                        262 fallos -> ValueError: task stub source is missing intake block

La propuesta promete 24 veces lo que el renderizador puede hacer, **y no lo dice**. Un dry-run cuyo
conteo no corresponde con lo que ocurriria si se ejecutara no es una propuesta: es una estimacion
optimista disfrazada de censo.

## Mi decision sobre la pregunta del checker -- y una observacion que puede hacerla innecesaria

**Decision: MARCAR, no excluir.** Excluir dejaria una propuesta de aspecto limpio que **encoge la
cobertura en silencio**; marcar mantiene las dos verdades a la vista -- cuantos selecciona la regla,
cuantos son stubeables hoy, y por que no lo son los demas. El hueco queda medible en vez de
desaparecer.

**Pero antes mira esto, porque puede que no quede nada que marcar.** Los 262 fallos son tareas
**`id <= TASK-0238`**: las que estan **EXENTAS del hard-gate de intake** y por eso nunca lo tuvieron.
El validador canonico **no les exige** bloque intake. Entonces:

**el stub tampoco tiene por que exigirselo.**

La frontera 0238 ya existe y es la que uso el checker para cazar el defecto de la vuelta anterior.
Aplicarla en los DOS lados -- el stub conserva el intake cuando el validador lo exige, y no cuando no
-- es coherencia, no una excepcion nueva. Y si la medicion lo confirma, los 11 pasan a 273 y el
bloqueante se cierra sin marcar nada.

**No te lo impongo: mide.** Si al renderizar un stub sin intake para una tarea `id <= 0238` el
validador sigue verde, esa es la via. Si algo mas lo rechaza, entonces marca los que queden y dilo
en el conteo. Lo que no vale es anunciar 273 y poder 11.

## Los otros tres puntos

Los de la seccion 8 del veredicto, tal como los enumera. No los re-escribo aqui para no
parafrasearlos mal: **leelos del artefacto**, que es la fuente.

## Alcance y coste

SOLO hub, sin producto. Corre las puertas UNA vez; la segunda corrida la ejecuto yo. **Esta es la
iteracion 2 de 2**: si el checker vuelve a pedir cambios, escala al operador y no abro una tercera
por mi cuenta.

-- Arquitecto, 2026-08-15 04:25 local (UTC+2)
