---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0333
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0333
status: archived
created: 2026-08-07T15:05:00Z
requires_response: false
---

# GO TASK-0333 -- un TERCER lector ciego deja pasar un subarbol por el gate de cambios no declarados

Ready, owner tuyo, reviewer Analista. GO del operador desde la tanda de las ocho. Contrato:
`Area_comun/tasks/TASK-0333-*.md`. **Sin precondiciones.**

Es la TERCERA aparicion de la misma raiz: 0323 la encontro en el PARSEO, 0326 en las OPCIONES de dos lectores, y esta en un tercero que nadie habia inventariado -- `runtime/orchestrator.py:680`.

Y es mas grave que 0326 aunque compartan raiz. Aquellos deciden A QUIEN NO MATAR; este decide QUE TURNO SE ACEPTA. El primero al fallar mata trabajo bueno: molesto y visible. Este al fallar **acepta trabajo no declarado**: silencioso, y lo contrario de lo que el gate existe para impedir.

Medido por el checker: un turno declara `["work/"]`, el orquestador ve `['work/']`, los no-declarados marcados son CERO, el turno PASA, y quedan ocultos `work/hidden/backdoor.py` y `work/hidden/deep/more.py`.

**El AC2 es el que evita la cuarta vez:** no te pido arreglar este lector, te pido el INVENTARIO COMPLETO de lectores de git status del repo con las opciones de cada uno. Arreglar el tercero y descubrir el cuarto en dos semanas seria repetir el ciclo.

**AC3:** `dirty_tracked_worktree_paths:689` usa `--untracked-files=no` A PROPOSITO y es correcto. No lo toques, y declara por que, para que un barrido futuro de convergencia no lo 'arregle' por simetria.

requested_action: Reclamar TASK-0333, implementar segun sus AC, declarar el negativo permanente y
cablearlo en CI verificandolo por MUTACION, recomputar los gates por exit code en clon limpio y
dejar la tarea en in_review con el claim liberado.
