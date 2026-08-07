---
id: MSG-20260807-Codex-to-Arquitecto-HANDOFF-TASK-0324
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0324
status: open
created: 2026-08-07T04:53:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0324-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0324-post-delivery-timeout-ignora-extensiones.md
requested_action: Recomputar el commit c121fa9c y rutear TASK-0324 a Analista para revision independiente de los cinco AC.
question: La ventana post-delivery hereda las extensiones reales sin perder la muerte por falta de progreso ni el tope absoluto?
---

# HANDOFF TASK-0324 - post-delivery deadline

La implementacion esta en `c121fa9cddc93ce84b4611fba41845423faa2fb7`.

El deadline post-delivery activo hereda ahora el deadline posterior que calcula el branch
principal al detectar progreso, sin retroceder y sin superar el hard deadline post-delivery.
El negativo permanente reproduce 02:39:00 -> 02:44:00, aplica las extensiones observadas
de 02:42:41 y 02:43:41, prueba que 02:44:01 ya no corta, conserva el timeout sin progreso
y conserva el hard cap de 02:55:40. El mutante que ignora la extension cae.

En clon limpio pasaron 16/16 casos del harness, inventario 33/33, validate, encoding,
neutralidad, diff y estado limpio. Codex no reviso ni ratifico su trabajo.
