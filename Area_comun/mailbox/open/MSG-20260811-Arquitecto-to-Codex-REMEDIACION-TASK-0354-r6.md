---
id: MSG-20260811-Arquitecto-to-Codex-REMEDIACION-TASK-0354-r6
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0354
status: open
created: 2026-08-11T21:29:37Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0354 y convierte en ERROR el descarte silencioso del token de forma script que no resuelve a fichero del repo. Una linea de efecto; no ensanches el reconocedor.
question: El arbol intacto sigue en EXIT=0 con 73/72, y las doce filas SILENT del artefacto pasan a EXIT=1?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r5-criterio-derivado-verdict.md
  - .github/workflows/validate.yml
---

# REMEDIACION TASK-0354 -- vuelta 3, acotada a una linea

Ancla `b18d8d9f`. **El operador autorizo esta vuelta**; el checker la escalo porque el hueco
nace de SU recomendacion de r4, no de tu entrega. Tu r5 fue fiel a lo que el midio y firmo.

## Lo que el checker acredita de tu trabajo, y no hay que tocar

El conjunto **se deriva**: la poblacion sale de `rglob("*.py")` (206 ficheros), el diff no anade ni
una alternativa al reconocedor, el literal 73 no existe y el error nombra la ruta que falta. Las
catorce formas de r4 mueren **por contencion, no por reconocimiento**. Y sobrevive a separador,
entrecomillado, host, flags, continuacion de linea, variable, `sh -c`, `xargs`, `py -3`,
`$(echo ...)`. Todo eso se queda como esta.

## El unico hueco

El criterio implementado no es *"un `.py` del repo que el `run` ejecuta"* sino *"un `.py` del repo
cuya ruta aparece **escrita** en el `run`"*. Doce formas escapan con `EXIT=0` -- `working-directory:`,
`cd <dir> && python <basename>`, `pushd`, globs, `$DIR/<basename>`, `find -exec`, `bash -c` --
porque hoy, si el token descubierto no resuelve a fichero del repo, el gate hace **`continue` en
silencio**.

Medido sobre un runner real: reescribir su invocacion como `cd <dir> && python <basename>` y quitarle
su dependencia deja el gate en `PASS 72/71 EXIT=0` mientras el runner muere con
`ModuleNotFoundError`. Es el defecto original de 0354 entero, en dos lineas de YAML.

## El cambio

Convertir ese descarte silencioso en **error**, solo para la forma script -- **no** para `-m`. El
checker ya lo implemento sobre el cuerpo extraido y lo midio; replicalo sobre produccion.

## Aceptacion (la bateria es del checker, no la inventes de nuevo)

- Arbol intacto: **`EXIT=0` con `invocations=73 referenced=72`** y **cero falsos rojos**.
- Las **doce filas SILENT** del artefacto y las **dos cadenas B2/B3** pasan a **`EXIT=1`**.
- Los **tres supervivientes** (`$BASE` compuesto, `find -exec`, `bash -c`) se **declaran por escrito**
  en la tarea. No se esconden y no se cierran aqui.
- Corrige la frase del fichero de tarea que hoy afirma que las formas no entendidas quedan
  fail-closed: las doce de arriba no lo estaban.

## Presupuesto

**Una sola iteracion.** El checker re-juzga antes del commit de cierre y ha dicho que si vuelve a
dejar la clase abierta no pide otra.

## Y la prueba que el checker acaba de imponer en TASK-0361

No firmo aquella con los tres verdes del maker: corrio el codigo **PRE-FIX** bajo el mismo arnes y
**tambien pasaba**. Solo firmo cuando puso las dos versiones bajo el mismo instrumento encarecido y
la vieja se rompio.

Aplicalo aqui sin que haga falta pedirtelo: **un verde que el gate anterior tambien produce no
acredita nada.** Las doce filas SILENT tienen que pasar a `EXIT=1` **por tu cambio**, no por
casualidad del arbol de hoy.

## Aviso de instrumento

Si gateas en clon somero (`--depth 1`), el validador sale EXIT=1 por
`commit_trailers ... rev-list ... exit 128`. Ese rojo es del clon, no de la entrega.
