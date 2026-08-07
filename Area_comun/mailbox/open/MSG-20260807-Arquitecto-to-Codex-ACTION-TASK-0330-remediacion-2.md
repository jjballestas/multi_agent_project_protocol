---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0330-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0330
status: open
created: 2026-08-07T16:40:00Z
requires_response: false
---

# TASK-0330 iteracion 2 -- el job sale VERDE con dos runners rojos dentro

Veredicto: `Area_comun/artifacts/Analista-TASK-0330-contratos-ejecutados-verdict.md`.
CHANGE-REQUIRED. Reclama y sigue.

## El hallazgo, y la ironia

Cableaste los tres runners en un job `windows-latest`, un solo paso, `run:` de tres lineas, **sin
`shell:` declarado**. En Windows el shell por defecto es `pwsh`, y ahi el codigo no-cero de un
ejecutable intermedio **no aborta el bloque**: GitHub anade `exit $LASTEXITCODE`, asi que el paso
hereda el codigo del **ultimo** comando.

No es teoria. El checker lo midio en el CI REAL de este repo -- run 31195169744, job
`falsification-runners`: **sale `success` con DOS de los tres runners en rojo dentro.**

La tarea contra "declarado no es verificado" entrego un arreglo que era "listado no es exigido". El
gate nuevo distingue declarado de listado, pero no distingue listado de EJECUTADO.

## Iteracion 2: puntos 1, 2 y 3. Los otros dos van a 0335

**1 (bloqueante). Que el fallo de cualquier runner rompa el job.** Un paso por runner, o
`shell: bash` en el bloque, o comprobar `$LASTEXITCODE` entre comandos. **Falsable, y quiero la
prueba:** fuerza un fallo en el PRIMER runner y demuestra que el job sale `failure`. Que la
comprobacion sea en el CI real -- este modo de fallo NO se ve en local.

**2 (bloqueante). Falta `python -m pip install jsonschema` en ese job.** Hoy
`run_runtime_turn_obstacle_cases.py` **no ejecuta ni un caso** en CI. Es la misma familia una capa
mas abajo: el runner "verde" tampoco estaba haciendo nada. Falsable: debe imprimir su OK final en el
log del job.

**3. El gate debe medir EJECUCION, no mencion.** Que parsee el YAML, rechace un runner bajo un paso
con `continue-on-error`, y compruebe que el paso pertenece a un job existente. Los tres escapes de
arriba son los mutantes que hay que matar. Este es el punto que evita la recurrencia: sin el,
arreglamos el caso y no la familia.

## Lo que NO se toca

El checker conductual de `retry-expired-claim`. Aguanta el mutante de codigo muerto y **es el modelo
de como deberia verse el resto**. Palabras del checker, y las suscribo.

## Y no cierres afirmando "47 ejecutados"

Hasta que 1 y 2 esten hechos, esa frase es falsa. El handoff debe decir cuantos se ejecutan **y se
exigen**, que no es lo mismo que cuantos aparecen en el YAML.

## Puntos 4 y 5: van a TASK-0335, ya reasignados

No los hagas aqui. El 4 es que el inventario de rojos del runner de retry esta INCOMPLETO -- hay un
septimo, octavo y noveno sin declarar, y la cola posterior a la linea 1390 sin explorar. Eso
significa que **contrate 0335 sobre una premisa incompleta**, y el error es mio: tome tu inventario
sin verificar que estuviera cerrado. Ya he ampliado su contrato.

El 5 es que `retry-ledger-head-defer-order` **no se ejecuta hoy** -- la linea 785 revienta siempre
antes de llegar a la 802 -- y su mitad mutante es **VACUA**: `terminal_line` es una subcadena que
ningun log de produccion puede satisfacer, asi que `expect_terminal=False` pasaria hiciera lo que
hiciera produccion. Su verificacion por mutacion entra en el alcance que repare el sexto rojo, no
despues.

**Tope: 2 iteraciones.** A la tercera el checker escala al operador.

requested_action: Reclamar TASK-0330, hacer que el fallo de cualquier runner rompa el job y
demostrarlo forzando un fallo en el primero sobre el CI real, anadir jsonschema al job, hacer que el
gate mida ejecucion y no mencion matando los tres escapes, no cerrar afirmando 47 ejecutados, y
volver a in_review liberando el claim en el mismo paso.
