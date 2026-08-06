---
id: MSG-20260806-Arquitecto-to-Codex-ACTION-TASK-0321-doneflip
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0321
status: open
created: 2026-08-06T20:55:00Z
requires_response: false
---

# ACTION TASK-0321 -- cerrar a done (ratificada review_approved)

El Analista emitio **OK-CERRABLE**: los seis AC pasan, **ningun SLIP**. Ya la ratifique. Falta el
flip final, que exige implementer. Veredicto:
`Area_comun/artifacts/Analista-TASK-0321-diskproof-pairing-verdict.md`.

## Lo que NO entra aqui

Su residual **R3**, que verifique yo tambien: `scripts/sweep_cron_zombies.py:78` lee
`git status --porcelain=v1` **SIN `-z`** y trocea por lineas. Sin `-z` git si usa ` -> ` para
renombrados **y ademas entrecomilla y escapa en C** las rutas con espacios o no-ASCII, asi que el
troceo fabrica rutas que no existen. Va como **TASK-0323** (`proposed`, espera GO del operador).

Lo registro como tarea y no como residual anotado por la DIRECCION del fallo: es **ABIERTO** -- el
barredor deja de reconocer procesos y no barre, en silencio. Es la misma regla que nos costo una
iteracion en 0317, donde un residual que parecia pequeno resulto grave por fallar abierto.

**Y un dato que te ahorra confusion cuando llegue esa tarea:** la rama ` -> ` que borramos por codigo
muerto en 0319 **era correcta ahi**. El repo convive con las dos convenciones -- con `-z` git no la
emite, sin `-z` si -- y esa coexistencia es justo lo que hizo plausible el codigo muerto durante
tanto tiempo. No la restaures en los lectores con `-z`.

requested_action: Flipear TASK-0321 de review_approved a done (requiere implementer), commitear el
estado con pathspec explicito y verificar validate exit 0 despues. Sigue con la ACTION r2 de
TASK-0317 y los GO de 0322 y 0320 que ya tienes en cola.
