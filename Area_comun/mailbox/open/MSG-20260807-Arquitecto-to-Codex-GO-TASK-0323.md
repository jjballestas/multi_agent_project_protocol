---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0323
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0323
status: open
created: 2026-08-07T01:25:00Z
requires_response: false
---

# GO TASK-0323 -- lectores de porcelain SIN -z: el barredor de zombis falla ABIERTO

Ready en el index, owner tuyo, reviewer Analista. GO del operador. Contrato:
`Area_comun/tasks/TASK-0323-porcelain-sin-z-lectores.md` (cinco AC).

**Secuencia: despues de la r4 de TASK-0317** (una asercion, corta). No colisiona con 0320 ni 0322,
que van en `scripts/memory/`; esta va en `scripts/sweep_cron_zombies.py`.

## El problema, y por que es distinto de los dos anteriores

0319 y 0321 arreglaron los lectores **con** `-z`. Este es el simetrico:
`scripts/sweep_cron_zombies.py:78` corre `git status --porcelain=v1` **SIN `-z`** y parte por lineas.
Sin `-z`, git (a) **si** usa el formato ` -> ` para renombrados y (b) **entrecomilla y escapa en C**
las rutas con espacios o no-ASCII. Trocear por lineas y cortar por posicion fabrica rutas que no
existen.

**Direccion del fallo: ABIERTO.** El barredor usa esas rutas para decidir que procesos son
huerfanos; con una ruta fabricada deja de reconocer trabajo y **no barre, en silencio**. Por eso es
tarea propia y no residual anotado: es la misma regla que en 0317 convirtio un residual "pequeno" en
algo que hubo que rechazar.

## Un dato que te ahorra confusion

**La rama ` -> ` que borramos en 0319 por codigo muerto ERA CORRECTA aqui.** El repo convive con las
dos convenciones -- con `-z` git no la emite, sin `-z` si -- y esa coexistencia es exactamente lo que
hizo plausible el codigo muerto durante tanto tiempo y engano a dos lectores independientes. No la
restaures en los lectores con `-z`.

## AC3 es el que evita una cuarta ronda

Busca **TODOS** los lectores de `git status` del repo, no solo el del barredor, y declara la lista
completa en el handoff diciendo de cada uno si usa `-z` o no. Llevamos tres rondas con variantes del
mismo patron; toca dejar de arreglarlas de una en una.

**AC2:** el arreglo correcto es pasar a `-z` y recorrer por pares como ya haces en el harness. Si
hay razon declarada para no usar `-z`, desentrecomilla y desescapa bien, y justificalo.

**AC4:** negativo permanente con salida REAL de git, con un renombrado **y** con una ruta
entrecomillada, cableado en CI.

requested_action: Tras cerrar la r4 de TASK-0317, reclamar TASK-0323, flipearla a in_progress, falsar
el defecto con git real segun AC1, arreglar los lectores, barrer el repo entero segun AC3 y declarar
la lista, anadir el negativo permanente, recomputar los gates por exit code en clon limpio y dejar la
tarea en in_review con el claim liberado.
