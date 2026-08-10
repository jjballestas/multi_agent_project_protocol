---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0354-r2
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0354
status: open
created: 2026-08-10T10:05:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED con escalada al operador -- el gate mata el defecto original pero no cubre la clase, y el hueco esta instanciado hoy en el propio workflow.
requested_action: No cerrar TASK-0354 por tu cuenta. Iteracion 2 de 2 consumida, asi que sube al operador la eleccion entre cerrar con residual declarado o autorizar una vuelta 3 con los cinco puntos del veredicto.
question: El operador prefiere cerrar con el residual declarado (hoy ningun runner se queda sin dependencias, medido) o autorizar la vuelta 3 para que el descubrimiento del gate deje de depender de la forma de la invocacion?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r2-gate-dependencias-verdict.md
  - 269e5d1340f64ff320fd724f5fadfd0a9afaecda
  - a47bed116aea540dc5a324d23b4ad6d1c7c1c675
---

# VEREDICTO TASK-0354 r2 -- CHANGE-REQUIRED (escalada, iteracion 2 de 2)

Ancla `269e5d13`, implementacion `a47bed11`; el workflow es byte-identico hasta `origin/main`.
Solo el hub, sin producto en alcance. Veredicto completo con exit codes en el artefacto.

## Respuesta a tu pregunta

**Hay via.** Dos, reproducidas en clon limpio con el cuerpo del gate extraido del YAML por parser
independiente y corrido bajo un interprete que tiene solo lo que cada job declara:

- **G1 -- la forma de la invocacion.** El descubrimiento ancla a principio de linea
  (`^\s*python ... .py`). El propio workflow, **dos pasos por encima del gate**, invoca
  `if ! python scripts/prune_state.py --root . --check`. Descubrimiento del gate: 72 invocaciones.
  Amplio: 73. A/B con el mismo import externo no declarado inyectado en el mismo job:
  en `prune_state.py` (no descubierto) gate PASS EXIT=0 y el runner muere EXIT=1; en
  `run_runtime_prune_cases.py` (descubierto) gate FAIL EXIT=1. El discriminador es la forma, no la
  dependencia. Y el unico testigo, `runners=72`, no esta atado a nada: reescribir el runner como
  `cd . && python ...` o `python -m ...` baja el contador a 71 en silencio y el defecto pasa.
- **G2 -- una indireccion por un modulo del repo.** El gate parsea solo el fichero del runner y
  excluye todo nombre local sin seguirlo. Con modulos de produccion y el idiom de `sys.path` que los
  runners ya usan: el runner del job de Windows importa `runtime.turn_validate` (que tiene
  `import jsonschema` de nivel superior) -> gate PASS runners=72 EXIT=0, runner EXIT=1
  `ModuleNotFoundError: No module named 'jsonschema'`.

## Lo que si esta bien, y lo verifique mas fuerte que la entrega

- M1 reproducido: quitar `pyyaml` deja el gate en FAIL EXIT=1 con el diagnostico completo.
- Los runners del job nuevo pasan EXIT=0 en un venv con **solo** `jsonschema pyyaml`.
- El borrado del `pip install jsonschema` del job de Windows esta justificado: su runner pasa
  EXIT=0 con un interprete **sin ningun paquete**, y segui sus procesos hijo (`ledger_head.py`,
  `runtime.protocol_replay` via `python -c`): stdlib puro.
- `ast.walk` si atrapa imports dentro de funciones (medido); solo se escapa el import dinamico.
- Tus tres residuales de la vuelta 1 estan ahora en el **fichero de tarea**, no en un mensaje
  archivado: granularidad `github.ref` con la duplicacion push/PR aceptada, commits intermedios, y
  AC1 pendiente de acreditar. Eso era exactamente lo que faltaba.
- AC6 re-derivado por mi de las anclas con `--job`: `2767b2c7` 4/0/0/4 y 269e5d13 1/0/0/1 en
  `falsification-runners`, y 3 PASS en `falsification-runners-python`. Cuadra.
- AC4: **0 invocaciones de runner perdidas**; la unica linea perdida es el `pip install` de Windows,
  verificado por comportamiento. AC3 sin movimientos nuevos de job/host.

## Por que escalo en vez de pedir la vuelta 3

Al cerrar la vuelta 1 declare "iteracion 1 de 2; si la clase reaparece en la segunda, escalo al
operador humano en vez de pedir una tercera". La clase reaparece por otra coordenada, asi que
cumplo lo declarado. Los dos lados, para que el operador decida con datos:

- **Cerrar con residual:** medi el cierre transitivo de todos los runners del workflow y **hoy
  ninguno se queda sin sus dependencias**. Lo que protege el arbol no es el gate, son los imports
  perezosos guardados; pero el riesgo vivo es cero.
- **Vuelta 3:** el hueco vive hoy en el mismo fichero y el contador no esta atado, asi que el
  proximo refactor de una linea lo abre sin dejar senal.

Minimo que cerraria la clase, todo falsable: descubrir por propiedad y no por forma (falsable con
`cd . && python ...` y `python -m ...`), atar `runners=N` a un inventario esperado, seguir un salto
de indireccion local o declarar por escrito que no se sigue, honrar `if:`/orden al contar una
declaracion, y declarar las formas `.ps1`/procesos hijo y el acoplamiento del mapa de paquetes al
entorno del job `validate`.

## Residuales de mi propia revision

Sin CI real: todo local, el gate nunca ha corrido en Actions y su veredicto depende de los paquetes
de la imagen `ubuntu-latest`. No termine la corrida completa de los 78 pasos del job `validate`
(limite de ventana, igual que el maker); verifique el paso nuevo y los cuatro primeros en clon
limpio. `pwsh` 7 ausente en mi host: el job de Windows sale `unsupported` en el replicador y por eso
ejecute su runner a mano.

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
