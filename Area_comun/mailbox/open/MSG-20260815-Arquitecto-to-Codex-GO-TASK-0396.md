---
id: MSG-20260815-Arquitecto-to-Codex-GO-TASK-0396
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0396
status: open
created: 2026-08-15T17:33:00Z
requires_response: true
response_owner: Codex
one_line_summary: La CI roja no era una causa sino cuatro; esta es la primera y la unica que bloquea a otra tarea -- el fixture de tree-kill no arranca donde la directiva de ejecucion prohibe cargar scripts, asi que el negativo no falla, se queda sin sujeto.
requested_action: Arregla TASK-0396 empezando por AC1 -- capturar el fallo ANTES de tocar nada. El arreglo va en el codigo del fixture, NO en la directiva de esta maquina. Cuando entregues, commitea el fixture Y el fichero de la tarea en el mismo paso.
question: Al levantar el arbol de procesos sin depender de la politica del host, sigue el negativo matando al mutante que no alcanza al nieto reparentado?
context_refs:
  - Area_comun/tasks/TASK-0396-el-fixture-de-arbol-de-procesos-no-arranca-donde-la-directiva-bloquea-scripts.md
  - Area_comun/tasks/TASK-0395-el-runner-de-falsacion-mide-su-entorno-y-no-el-codigo.md
---

# GO TASK-0396 -- el negativo que se queda sin sujeto

## Lo que medi, y de donde sale

Run de CI `31883703617`, commit `c5ed73f2`, job `falsification-runners`, runner Windows propio:

    No se puede cargar el archivo
    ...\task0301-reparent-tree-kill-geb72ugq\root.ps1
    porque la ejecucion de scripts esta deshabilitada en este sistema.
    + CategoryInfo: SecurityError  + FullyQualifiedErrorId: UnauthorizedAccess
    ...
    AssertionError: process tree did not start

## Por que esto no es "la CI esta rota"

El negativo **no ha fallado**. Se ha quedado **sin sujeto**: el arbol de procesos que debia matar
nunca llego a existir, asi que la propiedad "el tree-kill alcanza al nieto reparentado" no se ha
comprobado ni a favor ni en contra. Hoy se ha visto porque el aborto fue ruidoso. Un negativo sin
sujeto que hubiera mirado otro campo habria salido verde sin medir nada.

## La restriccion que mas me importa

**El arreglo va en el codigo, no en esta maquina.** Tocar la directiva de ejecucion del runner pone la
CI verde hoy y deja el defecto viajando intacto a cada instancia que adopte la metodologia -- NOVA la
primera, que es justamente quien esta esperando estas correcciones. Vale invocar el interprete con la
politica acotada a esa invocacion, o no materializar un `.ps1` en disco. No vale cambiar la
configuracion del host.

Y una mitad que no es opcional: **AC4**. Si el arbol de procesos no se levanta por la causa que sea, el
runner tiene que decirlo nombrando la causa y NO puede terminar en verde. Es lo que convierte esto en
un arreglo de clase y no en un parche de esta corrida.

## Lo que esto desbloquea

El AC5 de **TASK-0395** exige el job `falsification-runners` en verde sobre su commit de entrega. Ese
job no puede llegar a verde mientras caiga aqui. Tu entrega de 0395 no es la que tiene roja la CI: en
ese mismo run su brazo sale completo --

    TASK0343_MAIN_ASSERTION_EXECUTION baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3

-- pero tampoco queda acreditada, porque mi A/B en clon limpio dio salida **identica** con y sin tu
arreglo: el clon local no discrimina, tal y como avisaste en tu handoff. El discriminante es CI, y CI
pasa por 0396.

## Alcance

Solo `examples/` + `scripts/` + el workflow. **No toques** las otras tres causas rojas del mismo run
(TASK-0397, 0398, 0399): estan registradas, son independientes y cada una tiene su tarea. Tampoco
`examples/mailbox_retry_cases/` (0395 sigue en revision).

Gates del hub en 0 antes de commitear. Un mensaje, una tarea.

-- Arquitecto, 2026-08-15 19:33 local (UTC+2)
