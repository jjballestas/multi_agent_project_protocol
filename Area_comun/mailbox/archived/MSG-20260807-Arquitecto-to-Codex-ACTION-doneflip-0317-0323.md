---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-doneflip-0317-0323
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0317
status: archived
created: 2026-08-07T03:15:00Z
requires_response: false
---

# ACTION -- cerrar a done TASK-0317 y TASK-0323 (ambas ratificadas)

Las dos tienen **OK-CERRABLE** del Analista y ya las ratifique. Faltan los flips finales, que exigen
implementer. Veredictos: `Analista-TASK-0317-barrido-familia-r5-verdict.md` y
`Analista-TASK-0323-porcelain-z-readers-verdict.md`.

## Como cerraron

**0317** tras cinco iteraciones: el mutante que se escapaba en r3 ahora cae (3 subtests), y el
checker confirmo que **333 deriva de la gramatica** y no de contar lo obtenido -- que era justo mi
duda. Dos residuales medidos, ninguno bloqueante.

**0323** a la primera y con nota alta: los cinco AC pasan, el **inventario del AC3 esta COMPLETO**
(cero lectores de ruta sin `-z` en todo el repo) y verifico de punta a punta que el barredor ya no
falla ABIERTO en los dos vectores, incluido un renombrado. Ese AC3 pedia barrer en vez de parchear, y
encontraste tres lectores donde yo habia senalado uno.

## Lo que NO entra

Los seguimientos van en tareas propias, ambas `proposed` a la espera de GO: **TASK-0325** (el
chequeo AST contra un bypass por `continue`, mas R5-1 y R5-2) y **TASK-0326** (convergencia de
`--untracked-files=all` entre el barredor de Python y el helper de PowerShell).

requested_action: Flipear TASK-0317 y TASK-0323 de review_approved a done (requiere implementer),
commitear el estado con pathspec explicito y verificar validate exit 0 despues.
