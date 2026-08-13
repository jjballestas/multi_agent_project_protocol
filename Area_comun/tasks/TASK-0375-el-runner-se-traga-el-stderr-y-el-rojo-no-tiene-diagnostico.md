---
id: TASK-0375
title: El runner se traga el stderr, y por eso el rojo nuevo del job de Windows no tiene diagnostico
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0375-el-runner-se-traga-el-stderr-y-el-rojo-no-tiene-diagnostico.md
created: 2026-08-13
reviewer: Analista
intake:
  type: fix
  goal: >
    Residuo 2 del veredicto r1 de TASK-0364, declarado por el checker como NO perteneciente a esa
    tarea. El job de Windows tiene un rojo NUEVO en `run_agent_executable_resolution_cases`, el test
    que nacio con la resolucion de ejecutable del agente. El checker sospecho deriva del host y su
    propio `git diff` lo desmintio: es un test nuevo de +59 lineas. Falla en
    `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <probe>.ps1`, que es exactamente la
    forma que el maker declara que la politica del servicio rechaza bajo PowerShell 5.1 -- pero **no
    se puede probar**, porque el runner invoca con `capture_output=True, check=True` y se traga el
    stderr. El rojo existe, su causa es plausible y NADIE puede verla. Es la clase de defecto que ya
    nos costo caro: un fallo sin diagnostico hizo que siete fallos de la misma causa parecieran
    independientes. El primer paso no es arreglar el rojo: es hacerlo legible.
  acceptance:
    - "AC1 (el diagnostico primero, y es lo que cierra esta tarea): cuando un caso del runner falla,
      su salida identifica la causa -- al menos el comando, el exit code y el stderr del proceso que
      fallo. Se acredita provocando un fallo real y ensenando que el mensaje nombra la causa. Un
      `check=True` que revienta con la traza de Python y sin la voz del proceso hijo no acredita."
    - "AC2 (medido sobre el rojo que lo destapo): con el diagnostico puesto, se ejecuta
      `run_agent_executable_resolution_cases` en el job de Windows y se reporta lo que dice. Si
      confirma la hipotesis de la politica del servicio bajo 5.1, se declara; si la refuta, tambien
      -- y entonces el rojo tiene otra causa y esta tarea la ha encontrado."
    - "AC3 (la clase, no el caso): el criterio de que un fallo publique su diagnostico se aplica a
      TODOS los casos del runner, no solo al que fallo. Se acredita mostrando que el mecanismo es el
      mismo para cualquier caso, no un `try/except` alrededor de uno."
    - "AC4 (el negativo discrimina): un caso que pasa sigue pasando y sigue callado. Anadir
      diagnostico no puede convertir un verde en ruido ni, peor, en rojo."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/
    - .github/workflows/validate.yml
  out_of_scope:
    - "Arreglar la causa del rojo antes de poder verla: si tras AC1 el diagnostico dice que la causa
      es otra cosa, esa correccion es una tarea distinta. Aqui se compra visibilidad."
    - "La resolucion del ejecutable del agente por proveedor: es TASK-0367, en remediacion."
    - "El ancho de la guardia de metadatos persistentes: es TASK-0374."
  risk: low
  estimate: S
---

# TASK-0375 -- un rojo que nadie puede leer

## Como aparecio

El checker, revisando TASK-0364, vio que el rojo del job de Windows **cambio de identidad entre sus
dos rondas**. Sospecho deriva del host -- la explicacion comoda -- y fue a comprobarlo: el `git diff`
le dijo que `run_agent_executable_resolution_cases` es un test nuevo, +59 lineas.

Falla en:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File <probe>.ps1

que es literalmente la forma que el maker declara que la politica del servicio rechaza bajo 5.1. La
hipotesis encaja. Y no se puede confirmar, porque el runner llama con `capture_output=True,
check=True`: cuando el hijo falla, lo que sale es la excepcion de Python, no lo que el hijo dijo.

## Por que el orden es este

No pido arreglar el rojo. Pido **poder verlo**. Un fallo sin diagnostico ya nos hizo creer que siete
fallos de una misma causa eran independientes, y aqui el patron esta a medio formar: el checker tuvo
que reconstruir por `git diff` lo que el propio runner podria haber dicho en una linea.

Cuando el mensaje exista, el rojo se explicara solo -- y si lo que dice contradice la hipotesis
comoda, mejor: esta tarea habra encontrado la causa de verdad.
