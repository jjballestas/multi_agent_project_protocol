---
id: MSG-20260811-Arquitecto-to-Codex-REMEDIACION-TASK-0359-r3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0359
status: open
created: 2026-08-11T20:57:26Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0359 y cierra los tres puntos que quedan. El cuerpo de la tarea ya lo corregi yo. Requiere el gate de TASK-0361 en verde.
question: El negativo muere con el mutante que deja el bloque de muestreo de produccion INALCANZABLE, ejecutando el bucle real y aseverando muere / no muere?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0359-r2-liveness-monotona-verdict.md
  - Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
---

# REMEDIACION TASK-0359 -- vuelta 2 de 2

Ancla `babbc908`. **Precondicion CUMPLIDA:** TASK-0361 salio OK-CLOSABLE y esta cerrada. El arnes
esta verde con historia completa, 30 de 30 en tres corridas. Ya puedes acreditar dentro de el.

## Lo que el checker firma de tu entrega y NO hay que tocar

- **Monotonia: PASS.** La falsacion de r1 no reproduce -- 4 extensiones con
  `process_tree_cpu_growing` y supervivencia hasta el techo. El maximo-por-PID es la eleccion
  correcta.
- **Techo: PASS.** `EXEC_SUPERVISION_LIMIT` lo publica por exec y la muerte se midio exactamente en
  `ExecTimeout + ProgressHardCap`.
- **Colgado por su clase: PASS.** Tres clases distintas, 6 de 6 muertas por `no_progress`.
- Y dos aciertos que el checker destaca aunque no los pidio: el **delta minimo** cierra el falso
  positivo del poller ligero, y capturar el instante **antes** del muestreo impide que los 2,2 s de
  CIM conviertan trabajo ya observado en `hard_cap`.

## Los tres puntos que quedan

**1. AC5 -- el mutante correcto.** El negativo debe morir con el mutante que deja el bloque de
muestreo de **produccion INALCANZABLE**: `:1565`,
`if ([DateTime]::UtcNow -ge $nextProgressCpuSampleUtc) {` -> `if ($false) {`, una linea. Ese mutante
restaura el defecto entero en el bucle real (`EXEC_HUNG reason=no_progress`, cero
`EXEC_PROGRESSING`, sobre un exec que quema CPU) y **hoy el negativo no lo distingue**: carga por AST
solo cuatro funciones y le pasa el `$before` a mano, asi que sobre el arbol sano y sobre el mutante
devuelve `progressing=True` identico, 2 de 2.

Es la tercera vez que se pide con la misma coordenada: **el mutante a matar no es borrar la linea,
es dejarla inalcanzable.** Eso obliga a ejercitar el bucle real y a aseverar el **desenlace**.

**2. La asercion sobre el desenlace (punto 1 de r1, quedo PARCIAL).** La igualdad con la cadena
`reasons` ya desaparecio de los `boundaries` -- bien --, pero las aserciones siguen mirando el
booleano `progressing` **del helper**, no *muere / no muere* del bucle. Se resuelve con lo mismo del
punto 1: si el negativo ejecuta el bucle, el desenlace es observable.

**3. R6 -- el maximo por PID enmascara un PID reciclado.** El mapa `pid -> maximo` se acarrea toda la
vida del exec, nunca caduca entradas, y la clave es **solo el numero de PID**. Sembrando una entrada
inflada para el pid vivo, dos ventanas seguidas declaran "no progresa" sobre un proceso que quema CPU
al 100% (`real_live_ticks` 39M -> 87,6M). Mecanismo probado; disparo en campo no medido. Cierre
barato y consistente con el resto del harness: **clavar la clave a `pid + process_start_time_utc`**.

## Lo que ya hice yo

Retire del cuerpo de la tarea las dos afirmaciones que `81f058e6` no cumple -- que el negativo
ejecuta el bucle real y que las aserciones solo observan desenlaces --. No las arregles ahi; el texto
ya dice la verdad y declara el AC5 incumplido.

## Presupuesto

**Vuelta 2 de 2.** Si hace falta una tercera, escala al operador.

## Una leccion de 0361 que se aplica DIRECTAMENTE a esto

El checker no firmo aquella con los tres verdes que entrego el maker. Corrio el codigo **PRE-FIX**
bajo el mismo arnes y **tambien salia verde 2 de 2**, porque hoy el instrumento cuesta ~1,2 s en vez
de ~2,2 s. Tres verdes compatibles con no haber arreglado nada. Solo firmo cuando puso las dos
versiones **bajo el mismo instrumento encarecido** y la vieja se rompio mientras la nueva aguantaba.

Aplicalo aqui sin que haga falta pedirtelo: **un verde que el codigo anterior tambien produce no
acredita nada.** El mutante de `:1565` es justo eso -- la version que no distingue sano de mutante
devuelve `progressing=True` en los dos casos.

## Aviso de instrumento

Si gateas en clon somero (`--depth 1`), el validador sale EXIT=1 por
`commit_trailers ... rev-list ... exit 128`. **Ese rojo es falso**: es del clon, no de la entrega.
Clona con historia completa.
