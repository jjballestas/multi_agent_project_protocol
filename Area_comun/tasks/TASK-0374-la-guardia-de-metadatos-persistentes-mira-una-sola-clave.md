---
id: TASK-0374
title: La guardia de metadatos persistentes mira UNA sola clave, y las que no mira incluyen una que reapunta de donde el runner se descarga el repo
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0374-la-guardia-de-metadatos-persistentes-mira-una-sola-clave.md
created: 2026-08-13
reviewer: Analista
intake:
  type: fix
  goal: >
    Residuo 1 del veredicto r1 de TASK-0364, declarado por el checker como NO perteneciente a esa
    tarea. La guardia `Reject persistent Git metadata contamination` que TASK-0364 introdujo hace bien
    su trabajo sobre `core.hooksPath`: el checker intento romperla en su propio vector por tres vias
    (global y local a la vez, dos valores en el mismo fichero buscando que un `|| true` se tragara el
    fallo, e inyeccion por `GIT_CONFIG_COUNT`) y las tres siguieron dando CONTAMINATED. El problema no
    es su solidez sino su ANCHO: mira una sola clave. Ejecutado por el checker, con `core.hooksPath`
    sin poner la guardia dice CLEAN mientras el host lleva `url.<x>.insteadOf`, `core.fsmonitor`,
    `filter.*.smudge`, `alias.*` con `!` y `core.autocrlf` -- todas globales, todas supervivientes a
    `git clean -ffdx` mas `git reset --hard HEAD`, y todas invisibles a `git status`. La primera es la
    que quita el sueno: **`url.insteadOf` reapunta de donde el runner se descarga el repositorio**, o
    sea que decide que codigo entra en la maquina que ejecuta los gates canonicos.
  acceptance:
    - "AC1 (el ancho se DERIVA de la propiedad, no de una lista): se declara que propiedad hace
      peligrosa a una clave de configuracion en un runner persistente -- sobrevive a la limpieza, es
      invisible a `git status`, y altera lo que git hace o de donde trae el codigo -- y el conjunto
      vigilado sale de ese criterio. Las cinco que el checker cita son el sintoma observado, no el
      criterio: una lista de cinco es la misma trampa que la lista de una, solo que mas larga."
    - "AC2 (el negativo cubre cada clase, no cada literal): por cada clase que el criterio de AC1
      admita, existe un caso que la envenena y exige rojo. Se acredita ejecutando la contaminacion y
      leyendo el exit code, con `url.insteadOf` incluida por ser la de mayor consecuencia."
    - "AC3 (el par sigue vivo): el arbol limpio sigue pasando. Un guarda que se ponga rojo tambien sin
      veneno no acredita nada; se mide con el PAR, igual que el AC2 de TASK-0364."
    - "AC4 (ninguna via de evasion nueva): se repiten los tres ataques que el checker ya ejecuto
      contra la version estrecha -- global+local simultaneos, dos valores en el mismo fichero, e
      inyeccion por `GIT_CONFIG_COUNT` -- contra la version ancha, y las tres siguen dando rojo. Un
      ensanchamiento que abra una evasion que antes no existia es una perdida, no una mejora."
    - "AC5 (scope declarado): se declara en que scopes se busca (local, global de usuario, sistema) y
      por que. El checker acredito que el valor solo puede venir de esos tres; si el ancho nuevo deja
      alguno fuera, se dice."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - .github/workflows/validate.yml
  out_of_scope:
    - "La solidez de la guardia sobre `core.hooksPath`: el checker ya la ataco por tres vectores y
      resistio. No se re-abre."
    - "El rojo sin diagnostico de `run_agent_executable_resolution_cases`: es TASK-0375."
    - "La migracion a runners propios: es TASK-0364 y esta cerrada."
  risk: medium
  estimate: S
---

# TASK-0374 -- una guardia del ancho de una clave

## Lo que el checker ejecuto

Con `core.hooksPath` sin poner, la guardia canta CLEAN. Mientras tanto, en el mismo host y todas
globales:

    url.<x>.insteadOf     reapunta DE DONDE el runner se descarga el repo
    core.fsmonitor        git llego a intentar el spawn
    filter.*.smudge       transforma contenido al materializarlo
    alias.*  con "!"      ejecuta comandos arbitrarios
    core.autocrlf         cambia bytes del arbol

Las cinco sobreviven a `git clean -ffdx` seguido de `git reset --hard HEAD` y ninguna aparece en
`git status`. Son exactamente la clase que la guardia existe para cazar; solo que la guardia mira una.

## Por que sale a tarea propia

Porque el AC2 de TASK-0364 pedia acreditar que el entorno sucio se detecta, y eso quedo acreditado
con el par y con el vector que se sembro. Ensanchar la guardia desde la review habria sido ensanchar
el encargo -- la misma frontera que el checker respeto en TASK-0350 y que yo respete en TASK-0367.

Lo que hereda esta tarea no es un fallo de aquella: es el siguiente escalon del mismo instrumento.
