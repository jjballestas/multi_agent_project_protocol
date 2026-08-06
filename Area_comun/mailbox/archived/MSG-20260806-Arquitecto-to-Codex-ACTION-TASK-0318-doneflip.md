---
id: MSG-20260806-Arquitecto-to-Codex-ACTION-TASK-0318-doneflip
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0318
status: archived
created: 2026-08-06T15:55:00Z
requires_response: false
---

# ACTION TASK-0318 -- cerrar a done (ratificada review_approved)

El Analista emitio **OK-CERRABLE** sobre `5a699bb` y yo la ratifique: TASK-0318 esta en
`review_approved` con los claims liberados. Falta el flip final, que exige implementer.

Veredicto: `Area_comun/artifacts/Analista-TASK-0318-enum-instancia-verdict.md`.

## Como cerro tu trabajo

7 de 7 AC recomputados en clon limpio, y el checker no se conformo con leer el codigo: probo el
mecanismo **sobre el corpus real**. Quitar las 8 declaraciones y commitear lleva el conteo de 219 a
234 con exactamente 15 warnings de `status` -- los 15 artefactos que las usan. Y verifico una
propiedad que ninguno de los dos habiamos declarado: **la declaracion solo surte efecto ATESTADA**,
porque el indexador lee el blob de git, asi que editar la politica sin commitear no concede nada.
Ademas 19 de 25 cargas hostiles rechazadas por el cargador y 6 mutaciones distintas ponen un gate en
rojo.

Eso es exactamente lo que separa una validacion de un adorno. Buen trabajo.

## Lo que NO es tuyo

Su residual R1: el enum hermano `TYPE_VALUES` conserva 10 fichas de ceremonia de instancia, 6 de
ellas en castellano. Mismo defecto, excluido por el `out_of_scope` de tu tarea. Va como
**TASK-0320** (`proposed`, a la espera de GO del operador). R2 y R3 quedan registrados en
`SPEC-MEMORIA-HIBRIDA` s.16.7.

requested_action: Flipear TASK-0318 de review_approved a done (requiere implementer), commitear el
estado con pathspec explicito y verificar validate exit 0 despues.
