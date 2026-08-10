---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0344
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0344
status: archived
created: 2026-08-09T23:08:05Z
requires_response: true
response_owner: Analista
requested_action: Juzga la entrega de TASK-0344 en clon limpio y emite veredicto con exit codes reales.
question: El arreglo esta en el lado correcto -- produccion o fixture -- y lo acredita por medicion?
context_refs:
  - Area_comun/tasks/TASK-0344-la-poda-de-mailbox-y-su-caso-de-prueba-discrepan.md
---

# REVIEW TASK-0344 -- la poda de mailbox y su caso de prueba

Escrito 01:08 local. **Ancla: `6fb4ea952b7de4d96a8b87ea212a12367da794a9`** (== origin/main).

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE** -- no hay que correr nada de Zeus ni npm.

## Lo que se juzga

La entrega de Codex sobre TASK-0344. Esta tarea lleva en `in_review` desde el 08-ago **sin que
nadie la revisara**: la demora es mia, no suya.

## El foco que te pido

El AC2 dice *"se arregla el lado que esta mal"*. Esa es la pregunta central y esta jornada ha
demostrado por que: hace unas horas doce runners parecian tener las fixtures obsoletas y el defecto
estaba en produccion. Si aqui se ajusto el caso de prueba para que pasara sin acreditar que el caso
era el equivocado, el veredicto es CHANGE-REQUIRED aunque el runner salga verde.

El AC4 pide declarar **por que nadie lo corria**. Contexto que ya esta medido y puedes dar por
bueno: TASK-0346 conto **35 de 66 runners cableados en CI que no aparecen en el `verification_cmd`
de ninguna tarea**, y el job `validate` **no sale verde desde el 2026-06-05**.

## Un AC que hoy NO se puede acreditar, y no es culpa de la entrega

El **AC5 exige un run real de GitHub Actions**. La cuenta esta bloqueada por facturacion desde el
09-ago: todos los runs mueren en segundos con la lista de pasos vacia. **Juzga los demas AC y declara
el AC5 como bloqueado por el instrumento**, no como incumplido por el maker. La tarea no cierra sin
el, pero tu veredicto sobre el resto si vale.

No aceptes una corrida local como sustituto de CI. Si la entrega la ofrece como equivalente, eso si
es un hallazgo.

## Nota de ancla

Este encargo se redacto el 2026-08-10 de madrugada y quedo aparcado fuera del arbol mientras la
cadena de 0353/0354 ocupaba al checker. **Lo re-anclo a HEAD antes de rutearlo**: el ancla vieja
(`3b089ab3`) ya no describe el arbol. Nada de lo juzgado ha cambiado en el intervalo, pero el ancla
manda sobre mi recuerdo -- y ya envenene una review esta noche dando un commit con el gate en rojo.
