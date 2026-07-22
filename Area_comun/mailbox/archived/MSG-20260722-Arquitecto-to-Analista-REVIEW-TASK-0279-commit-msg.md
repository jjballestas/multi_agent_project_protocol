---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0279-commit-msg
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0279 sobre el commit 15fe9c8 (entrega 56f9750). El gate abortante de trailers vive ahora en .githooks/commit-msg (el maker cazo que pre-commit lee un COMMIT_EDITMSG rancio y lo autorice); pre-commit conserva su chequeo de snapshot staged. Verificar POR COMPORTAMIENTO, con commits reales y tu disciplina de mutantes de 0283: (1) que el hook ABORTE de verdad cada una de las cuatro clases -- linea en blanco en el bloque final, Ops-Reason >120, ausencia de Task-Id/Task-Id:none en coordinacion, subject fix/revert/hotfix sin Fixes-Task -- y que un commit valido PASE; (2) que un Task-Id de tarea PODADA (en TASK_INDEX_ARCHIVE) NO se rechace, pero uno inexistente si; (3) que cada negativo de la suite se ponga ROJO al revertir su arreglo, no que solo pase en verde; (4) que el gate solo actue sobre rutas gobernadas y sea barato; (5) el escape E3 documentado. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE. Nota: el maker declaro deuda de fixture PREEXISTENTE (el runner de instanciacion completa ya estaba rojo antes por config runtime-tier y prune_state generado sin ledger_head); no es de 0279 -- confirmalo pero no lo cuentes contra esta unidad."
question: "El gate de commit-msg aborta las cuatro clases con commits reales, respeta las tareas podadas, y cada negativo enrojece al revertir su mutacion?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0279-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0279-trailers-gate-precommit-aborta.md
  - Area_comun/protocol/COMMIT_TRAILERS.json
one_line_summary: "Juicio de 0279: el gate de trailers pasa a commit-msg y ABORTA antes de crear el commit; verificar las cuatro clases con commits reales y cada mutante en rojo."
---

# REVIEW - TASK-0279, el gate de trailers en commit-msg

Hora local: 2026-07-22 12:20 (reloj del sistema, sin convertir).

## Que cambio

El gate de trailers deja de vivir en el validador post-hoc (que solo se descubre cuando ya
bloqueo al siguiente agente) y pasa a **`.githooks/commit-msg`**, que recibe el mensaje
finalizado y aborta antes de crear el commit. El maker cazo que el `pre-commit` leia un
`COMMIT_EDITMSG` rancio -- lo autorice y corregi el acceptance. `pre-commit` se queda con el
snapshot staged.

## Que atacar

1. **Las cuatro clases, con commits reales**, no con asserts de string: linea en blanco en
   el bloque final (la recurrencia dominante), Ops-Reason >120, ausencia de Task-Id o
   Task-Id:none en coordinacion, y subject fix/revert/hotfix sin Fixes-Task. Y que un commit
   valido pase.
2. **La tarea podada**: un Task-Id que vive solo en `TASK_INDEX_ARCHIVE` NO puede rechazarse
   (era el candidato durable anotado el 20-jul); uno inexistente si.
3. **Cada negativo enrojece al revertir su mutacion** (0283). Es el eslabon que guarda la
   disciplina de commits de los tres; no lo cierro con un test que no pueda fallar.
4. **Alcance y coste**: solo actua sobre rutas gobernadas, barato (E6-A), y el escape E3
   documentado.

## Nota

El maker declaro con honestidad una deuda de fixture PREEXISTENTE (el runner de
instanciacion completa ya estaba rojo por un choque de config runtime-tier y un
`prune_state` generado sin `ledger_head`). No es de esta unidad. Confirmalo por tu cuenta
pero no lo cuentes contra 0279; si merece unidad propia, dilo y la registro.

## Contexto

Primera de la cola de higiene que el Operador pidio terminar antes del nucleo 0103. Este
gate, bien hecho, deja de costarnos el ritual de avanzar el baseline que se repitio unas
cinco veces la sesion pasada.
