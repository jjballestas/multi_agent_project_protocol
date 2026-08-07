---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0334
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0334
status: open
created: 2026-08-07T15:05:00Z
requires_response: false
---

# GO TASK-0334 -- git status no desciende a repos EMBEBIDOS y hay SEIS en el arbol

Ready, owner tuyo, reviewer Analista. GO del operador desde la tanda de las ocho. Contrato:
`Area_comun/tasks/TASK-0334-*.md`. **Sin precondiciones.**

Esta es de otra naturaleza que 0323, 0326 y 0333. Aquellas son defectos NUESTROS: parseabamos mal o preguntabamos mal. Aqui preguntamos bien y **git contesta lo que puede contestar** -- un repo embebido es opaco al `status` del padre por diseno. Ninguna opcion lo arregla, asi que no es un fix de una linea sino un mecanismo nuevo.

Medido: con `work/inner` como repo anidado, `--untracked-files=all` baja UN nivel y para; anadir `--ignored` tampoco. `dirty_claimed_route` devuelve **False** para un claim a un fichero vivo dentro. False significa que el barredor **mata trabajo vivo**.

**Y no es teorico: inventarie SEIS repos embebidos hoy**, tres de ellos bajo `.protocol-tmp/`, que es donde viven el estado de los crons y las leases. El punto ciego esta dentro del propio campo de vision del barredor.

**AC4 es la linea que no se cruza:** hoy el fallo es DESTRUCTIVO, no una deteccion perdida. Tras el arreglo, ante deteccion fallida o ambigua el comportamiento correcto es **NO MATAR**.
**AC5:** declara hasta que profundidad cubres y que pasa mas alla. Un mecanismo que solo baja un nivel mas que git deja la familia abierta un escalon arriba.

requested_action: Reclamar TASK-0334, implementar segun sus AC, declarar el negativo permanente y
cablearlo en CI verificandolo por MUTACION, recomputar los gates por exit code en clon limpio y
dejar la tarea en in_review con el claim liberado.
