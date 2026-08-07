---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0330
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0330
status: archived
created: 2026-08-07T09:57:00Z
requires_response: false
---

# GO TASK-0330 -- la cobertura declarada no es cobertura verificada

Ready, owner tuyo, reviewer Analista. GO del operador. Contrato:
`Area_comun/tasks/TASK-0330-contratos-declarados-que-ci-nunca-ejecuta.md`.

**Sin precondiciones.** Va segunda porque mientras siga asi, **cualquier contrato nuevo que caiga en
esas tres suites nace dormido** -- incluidos los que van a producir las tareas de esta misma tanda.

## Lo medido

    contratos declarados                             37
    runners distintos                                 8
    runners que CI ejecuta                            5
    contratos cuyo runner NUNCA se ejecuta           23   (47 fronteras)

CI corre `check_falsification_contracts.py --inventory`, que verifica que cada contrato este
DECLARADO y tenga fichero dueno. **No ejecuta los runners** -- el script no tiene ni `subprocess`.
Y `validate.yml` lista cada runner como paso explicito, asi que el que no aparece, no corre.

Los tres ausentes: `run_mailbox_retry_cases.py` (16 contratos),
`run_runtime_turn_obstacle_cases.py` (6), `run_post_gate_obstacle_cases.py` (1). Ningun hook ni
harness los invoca; solo aparecen corridos a mano en veredictos antiguos.

## Y uno esta ROJO desde hace dos semanas

`52d0a380 fix(TASK-0316)` hizo `-CoordinatorId` obligatorio en `peer_mailbox_cron.ps1`;
`run_mailbox_retry_cases.py` lo invoca **0 veces** con ese parametro, asi que muere en el primer
fixture. Dano colateral de una tarea cerrada como **done**, invisible porque el gate que lo habria
cazado no se ejecuta.

Evidencia adicional que aparecio hoy sola: tu remediacion de 0324 anadio un campo a la linea
`EXEC_PROGRESSING`. Su unico consumidor automatizado es **precisamente esa suite muerta**. Si el
cambio hubiera roto ese parseo, no se habria enterado nadie.

## AC3 es lo que impide que vuelva a pasar

Anadir los tres pasos al workflow arregla hoy y deja el mecanismo igual de fragil: el siguiente
contrato que alguien declare sin cablear volvera a contarse como cobertura. El gate tiene que
**fallar solo** cuando un contrato declarado no tenga ejecucion.

**AC5, y lo digo en serio:** al encender tres suites dormidas apareceran mas rojos. **Reportalos
ANTES de arreglarlos.** "Lo arregle todo" y "lo silencie todo" tienen que poder distinguirse.

requested_action: Reclamar TASK-0330, reproducir el rojo y la ausencia de ejecucion, devolver la
suite a verde sin relajar aserciones ni marcar casos como skip, cablear los tres runners, hacer que
el gate falle ante un contrato sin ejecucion, declarar el inventario de rojos que aparezcan,
recomputar los gates en clon limpio y dejar la tarea en in_review con el claim liberado.
