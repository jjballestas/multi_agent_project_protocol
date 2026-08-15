---
id: TASK-0396
title: El fixture de arbol de procesos no arranca donde la directiva de ejecucion bloquea scripts -- el negativo de tree-kill no falla, se queda sin sujeto
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0396-el-fixture-de-arbol-de-procesos-no-arranca-donde-la-directiva-bloquea-scripts.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Medido por el Arquitecto el 2026-08-15 sobre el commit de entrega `c5ed73f2`, en el job de CI
    `falsification-runners` del runner Windows propio. El fixture de TASK-0301 escribe un `root.ps1`
    en un directorio temporal y lo invoca para levantar un arbol de procesos que el negativo de
    tree-kill debe matar. El host responde:

        No se puede cargar el archivo
        C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Temp\task0301-reparent-tree-kill-geb72ugq\root.ps1
        porque la ejecucion de scripts esta deshabilitada en este sistema.
        + CategoryInfo: SecurityError ... + FullyQualifiedErrorId: UnauthorizedAccess

    y acto seguido el runner aborta en `assert all((fixture / name).exists() for name in pid_files),
    "process tree did not start"`.

    Lo que importa no es que la CI este roja, sino QUE CLASE de rotura es. El negativo no ha fallado:
    se ha quedado SIN SUJETO. Nunca llego a existir el arbol de procesos que debia matar, asi que la
    propiedad "el tree-kill alcanza a los nietos reparentados" no se ha comprobado ni a favor ni en
    contra. Un negativo sin sujeto es indistinguible, desde fuera, de un negativo que no encuentra
    nada que objetar -- y aqui solo se ha visto porque el aborto fue ruidoso.

    El fallo es de PORTABILIDAD, no de este equipo. La directiva de ejecucion de PowerShell es
    politica de host: una instancia adoptante (NOVA la primera) hereda un fixture que solo arranca si
    el administrador de su maquina resulta permitir la carga de scripts desde el directorio temporal.
    Arreglarlo tocando la politica del runner deja el defecto intacto para todo el que adopte; por eso
    la reparacion tiene que estar en el codigo del fixture, no en la configuracion de esta maquina.
  acceptance:
    - "AC1 (reproducir primero): dejar constancia del fallo ANTES de tocar nada -- correr el fixture
      en un host con la carga de scripts deshabilitada y capturar el `SecurityError`/`UnauthorizedAccess`
      mas el `process tree did not start`. Sin esa captura no se sabe que el arreglo arregla ESTO."
    - "AC2 (el fixture arranca sin depender de la politica del host): el arbol de procesos se levanta
      igual con la carga de scripts deshabilitada. Vale invocar el interprete con la politica acotada
      a esa invocacion, o no materializar un `.ps1` en disco. Lo que NO vale es cambiar la directiva
      de la maquina: eso repara este runner y deja el defecto viajando a cada adoptante."
    - "AC3 (el negativo SIGUE matando): tras el cambio, el mutante que el negativo debe cazar -- el
      tree-kill que no alcanza al nieto reparentado -- sigue saliendo en exit 1, y el control en 0. Un
      fixture que arranca pero ya no discrimina es peor que el aborto de hoy, porque calla."
    - "AC4 (distinguir sin-sujeto de sin-hallazgo): si el arbol de procesos no llega a levantarse por
      cualquier causa, el runner lo dice con un mensaje que nombra la causa, y NO puede terminar en
      verde. Hoy el `assert` desnudo no distingue una cosa de la otra; esa es la propiedad que hace
      que este defecto sea generico y no anecdotico."
    - "AC5 (CI): el job `falsification-runners` deja de caer por esta causa sobre el commit de
      entrega. Se acredita con el run de CI. Si tras el arreglo cae por OTRA causa, se reporta esa
      causa y no se declara cerrado el AC."
  verification_cmd:
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/
    - scripts/
    - .github/workflows/validate.yml
  out_of_scope: >
    ENMIENDA 2026-08-15 20:03 local (Arquitecto): la redaccion original excluia
    `examples/mailbox_retry_cases/` entera, y eso era una CONTRADICCION -- el fixture de TASK-0301
    vive exactamente ahi (`run_mailbox_retry_cases.py`, lineas 1776-1797), asi que la tarea pedia
    reparar algo en el unico fichero que prohibia tocar. Lo detecto Codex y bloqueo en vez de
    interpretar, que es lo correcto. Alcance corregido: SI se puede modificar el bloque del fixture
    de TASK-0301 dentro de `run_mailbox_retry_cases.py` -- su montaje de `root.ps1`/`child.ps1`/
    `grand.ps1`, su invocacion y sus aserciones. NO se toca ninguna otra ruta ni comportamiento de
    TASK-0395 en ese mismo fichero, que sigue en revision.
    Ademas: NO se toca la directiva de ejecucion del runner ni ninguna configuracion de esta
    maquina -- el arreglo es de codigo y debe viajar. NO se tocan las otras tres causas rojas del
    mismo run (TASK-0397, TASK-0398, TASK-0399): son independientes y cada una tiene su tarea.
  risk: high
  estimate: M
---

# TASK-0396 -- el fixture de arbol de procesos no arranca donde la directiva bloquea scripts

## Evidencia

Run de CI `31883703617`, job `falsification-runners`, commit `c5ed73f2`, runner Windows propio.

    No se puede cargar el archivo ...\task0301-reparent-tree-kill-geb72ugq\root.ps1
    porque la ejecucion de scripts esta deshabilitada en este sistema.
    + CategoryInfo          : SecurityError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : UnauthorizedAccess
    ...
    assert all((fixture / name).exists() for name in pid_files), "process tree did not start"
    AssertionError: process tree did not start

## Por que bloquea a otra tarea

El AC5 de **TASK-0395** exige el job `falsification-runners` en verde sobre su commit de entrega. Ese
job no puede llegar a verde mientras caiga aqui, asi que 0395 no puede acreditarse por mucho que su
propio arreglo sea correcto. En el mismo run, y sobre el commit de entrega de 0395, la linea de su
brazo ya sale completa:

    TASK0343_MAIN_ASSERTION_EXECUTION baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3

-- Arquitecto, 2026-08-15
