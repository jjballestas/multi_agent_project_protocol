---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-GO-TASK-0279-trailers-precommit
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0279: llevar el chequeo de trailers al pre-commit CON ABORTO, en vez del validador post-hoc que solo se descubre cuando ya bloquea al siguiente agente. El hook (.githooks/pre-commit, ya armado en 0257 y con avisos no bloqueantes desde 0273) debe RECHAZAR el commit cuando el mensaje incumple el contrato de trailers, con un mensaje que diga que falta y como se escribe. Cubrir las cuatro clases que han mordido de verdad esta semana: (1) linea en blanco dentro del bloque final de trailers (F-0240-01, la recurrencia dominante); (2) Ops-Reason de mas de 120 caracteres; (3) ausencia de Task-Id o de Task-Id: none en commits de coordinacion; (4) subject fix/revert/hotfix sin Fixes-Task. Un Task-Id que referencia tarea inexistente se rechaza, pero una tarea PODADA NO cuenta como inexistente: consultar tambien TASK_INDEX_ARCHIVE. Chequeo acotado y barato (coherente con E6-A, sin segundos perceptibles). Salida de escape documentada coherente con el desarme E3. Suite con un commit valido y uno por clase invalida, cada negativo con su mutacion demostrada (disciplina de 0283). Espejo born-operational. Entregar in_review + handoff + release."
question: "ETA, y confirmas que el chequeo consulta TASK_INDEX_ARCHIVE para no rechazar commits historicos que referencian una tarea ya podada?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0279-trailers-gate-precommit-aborta.md
  - Area_comun/protocol/COMMIT_TRAILERS.json
one_line_summary: "GO a 0279: el gate de trailers pasa al pre-commit con aborto. Es el que corrige el fallo de fondo -- hoy se valida donde no se puede corregir, y el que se estrella es el siguiente agente."
---

# ACTION - GO a TASK-0279, el gate de trailers en el sitio correcto

Hora local: 2026-07-22 08:45. Arranca el frente de higiene, y empiezo por esta porque es
la que mas friccion quita: el baseline de trailers se avanzo unas cinco veces en la ultima
sesion, cada vez porque un commit con el bloque de trailers mal formado se descubrio DESPUES
de existir, y el que se estrellaba era el pre-gate del siguiente agente.

El intake esta completo; subrayo lo que no puedes saltarte:

- **Aborta de verdad**, no avisa. El hook rechaza el commit incumplidor con un mensaje que
  diga exactamente que falta.
- **Las cuatro clases reales**, no una lista generica: linea en blanco en el bloque final,
  Ops-Reason > 120, ausencia de Task-Id/Task-Id: none, y subject fix/revert/hotfix sin
  Fixes-Task.
- **Tarea podada != inexistente**: consulta TASK_INDEX_ARCHIVE. Este es el candidato durable
  que quedo anotado en el propio registro del gate el 20-jul; sin el, un commit historico
  legitimo que cita una tarea ya archivada se rechazaria.
- **Barato**: coherente con E6-A, sin segundos perceptibles en el commit.
- **Escape documentado** coherente con el desarme E3 del hook.
- **Cada negativo con su mutacion demostrada** (0283): un commit valido pasa, uno por clase
  invalida se rechaza, y al revertir el chequeo el negativo correspondiente se pone rojo.

## Contexto

La maquinaria de integridad esta cerrada y desplegada (rollback no destructivo, pre-gate
sano). El Operador pidio terminar toda la higiene antes de reabrir el nucleo 0103, y esta va
primera. El harness vivo ya lleva el codigo bueno; esto toca .githooks/, no el cron.

Trailers en bloque final sin linea en blanco -- que la unidad que arregla eso no nazca
incumpliendolo. Fondo intocable intacto.
