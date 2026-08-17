---
id: TASK-0415
title: La tolerancia de instance_context despierta un fragmento hoy muerto que ningun negativo puede falsar
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0415-la-tolerancia-de-instance-context-despierta-un-fragmento-muerto.md
created: 2026-08-18
reviewer: Analista
intake:
  type: infra
  goal: >
    Registra el residuo declarado por el checker al cerrar TASK-0378 r5, con la medicion que lo
    acompana, para que no quede huerfano entre dos tareas. Hoy `instance_context()` revienta -- sin
    capturar -- cuando `git rev-parse --is-inside-work-tree` no devuelve `"true"`, y los dos ganchos
    rechazan. Ese rechazo es lo que hace INALCANZABLE el fragmento
    `if inside_work_tree != "true": return None` de `commit_actor()`. El checker lo midio con el
    mutante M6 -- quitar ese fragmento -- y M6 **SOBREVIVE las dos suites**, porque fuera de un repo
    el `git rev-parse` lanza excepcion y el `except` ya devuelve `None`: la asercion que parece
    cubrirlo pasa por OTRO motivo que la rama que dice probar. El dia que se haga `instance_context()`
    tolerante, ese fragmento pasa de muerto a alcanzable **y seguira sin tener falsador**.
    Y la direccion importa, tambien medida por el checker levantando el guardia en ambas versiones:
    la rama que r5 borro era un escape **fail-open**, 4 de 4 vuelcos (`core.bare` y dentro de `.git/`,
    en los dos ganchos: VIEJO acepta con exit 0, NUEVO rechaza con exit 1). Borrarla fue monotono en
    la direccion segura. Hacer `instance_context()` tolerante empuja en la direccion CONTRARIA, asi
    que la tolerancia no puede aterrizar sin su negativo.
  acceptance:
    - "AC1 (la tolerancia, acotada): `instance_context()` deja de reventar cuando
      `--is-inside-work-tree` no es `\"true\"` y devuelve un resultado utilizable. Se acredita por
      exit code en las cuatro posiciones medidas por el checker: `core.bare=true` y dentro de
      `.git/`, en pre-commit y en commit-msg."
    - "AC2 (el fragmento despertado TIENE falsador): con la tolerancia puesta, el mutante M6 --
      quitar `if inside_work_tree != \"true\": return None` de `commit_actor()` -- debe MORIR. Hoy
      sobrevive. Se acredita ejecutando el mutante, no describiendolo. Este AC es la razon de ser de
      la tarea: sin el, la tolerancia reintroduce un escape sin guardia."
    - "AC3 (no se reabre el fail-open que r5 cerro): tras la tolerancia, las cuatro posiciones de la
      tabla de direccion siguen RECHAZANDO (exit 1) cuando no hay claim que cubra las rutas para el
      actor de commit. Se acredita por el par: con claim valido pasa, sin claim rechaza. Si alguna
      vuelve a exit 0 aceptando, la tolerancia ha revertido r5 y es peor que el defecto."
    - "AC4 (el negativo sobrevive a la coordenada): el mutante de AC2 debe seguir muriendo si se
      cambia el orden de las comprobaciones o el formato del valor devuelto -- no vale un negativo
      atado a la linea exacta."
  verification_cmd:
    - "python scripts/test_precommit_hook.py"
    - "python scripts/test_commit_msg_hook.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/check_commit_trailers.py
    - scripts/test_precommit_hook.py
    - scripts/test_commit_msg_hook.py
  out_of_scope:
    - "Por COMPORTAMIENTO, no por ruta: queda fuera cualquier cambio que altere el veredicto del gate
      de claims para entradas ALCANZABLES hoy -- las 15 entradas de produccion del censo diferencial
      del checker deben seguir dando el mismo (exit, stderr). Lo que entra es unicamente el
      comportamiento en las posiciones donde hoy `instance_context()` revienta."
  risk: medium
  estimate: M
---

# TASK-0415 -- la tolerancia despierta un fragmento que hoy nadie puede falsar

## Origen

Residuo declarado por el checker en el veredicto **OK-CERRABLE de TASK-0378 r5**, seccion 6.
Lo registro como tarea propia y no como sexta vuelta de 0378 por tres razones que el checker dio y
comparto: `bb419bc0` no toca `commit_actor`, esta fuera del alcance de producto declarado de r5, y
es **la misma capa del defecto** cuya tolerancia ya se habia decidido diferir.

Evidencia completa en `Area_comun/artifacts/Analista-TASK-0378-r5-rama-muerta-verdict.md`.

## Las dos mediciones que la fundan

**M6 sobrevive.** Quitar `if inside_work_tree != "true": return None` de `commit_actor()` no mata
ninguna de las dos suites. La asercion que parece cubrirlo pasa por otro motivo: fuera de un repo
el `git rev-parse` lanza excepcion y el `except` ya devuelve `None`. Es un fragmento sin falsador,
hoy inofensivo **solo porque es inalcanzable**.

**La direccion, con el guardia levantado en ambas versiones:**

    core.bare / pre-commit    VIEJO 0 (ACEPTA)   NUEVO 1 (rechaza)
    core.bare / commit-msg    VIEJO 0 (ACEPTA)   NUEVO 1
    .git-dir  / pre-commit    VIEJO 0 (ACEPTA)   NUEVO 1
    .git-dir  / commit-msg    VIEJO 0 (ACEPTA)   NUEVO 1

La rama que r5 borro era un escape **fail-open**. La tolerancia empuja en la direccion contraria:
por eso AC2 y AC3 no son adornos, son la condicion para que pueda aterrizar.

## Por que no se puede hacer "solo la tolerancia"

Porque el orden natural es el peligroso: quien haga `instance_context()` tolerante para arreglar la
ergonomia despertara `commit_actor` sin darse cuenta, y el unico negativo que deberia protegerlo
**ya se sabe que no discrimina**. Es el patron del repo -- una senal que no puede enrojecer ninguna
puerta -- pero conocido de antemano por una vez. Aprovecharlo.
