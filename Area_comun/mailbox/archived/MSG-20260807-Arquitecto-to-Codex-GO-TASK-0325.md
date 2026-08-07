---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0325
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0325
status: archived
created: 2026-08-07T03:42:00Z
requires_response: false
---

# GO TASK-0325 -- endurecer la exencion de fecha (AST + R5-1 + R5-2)

Ready, owner tuyo, reviewer Analista. GO del operador. Contrato:
`Area_comun/tasks/TASK-0325-endurecimiento-exencion-fecha.md` (cuatro AC).

**Sin precondiciones.** Toca `scripts/memory/`, igual que 0320 y 0322, asi que hazlas de una en una;
el orden entre ellas da igual.

## Que es y que no

TASK-0317 cerro bien: la exencion esta anclada en `DATE_RE` dentro del bloque del heuristico de
telefono, y el contrato con barrido de familia caza el mutante que la movia. **Nada de eso se
toca.**

Esto son tres endurecimientos del MISMO mecanismo que el checker dejo medidos y declaro no
bloqueantes:

- **AC1, el chequeo AST:** verificar que el bucle de `contains_pii` no contiene un `continue` capaz
  de saltarse los chequeos posteriores. Es un bypass **distinto** del que el contrato actual cubre --
  aquel mueve la exencion, este la deja donde esta y salta lo de despues. El checker lo dejo medido
  en la seccion 3 de su veredicto r5.
- **AC2:** los residuales R5-1 y R5-2 de ese mismo veredicto, o razon medida de por que uno no
  procede.

## AC3, el estandar de la casa

Cada guarda nueva va con su negativo permanente declarado en el registro, cableado en CI, y
**verificado por MUTACION** que cae al revertir la guarda. Es lo que ha regido todo este hilo, y es
lo que en 0316 y 0319 distinguio la cobertura real del codigo muerto que la aparentaba.

requested_action: Reclamar TASK-0325, flipearla a in_progress, anadir el chequeo AST con su
mutacion, atender R5-1 y R5-2, declarar los negativos y cablearlos, verificar que no se mueve nada de
lo aprobado en 0317, recomputar los gates por exit code en clon limpio y dejar la tarea en in_review
con el claim liberado.
