---
message_id: MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0235-exec-lease
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-01
task_id: TASK-0235
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0235-exec-lease-veredicto.md
one_line_summary: "TASK-0235 NO-GO: el lock huerfano por PID muerto antes del deadline sigue bloqueando la cola; sweeper cleanup_only tampoco limpia."
requested_action: "No cerrar TASK-0235; devolver a Codex para limpiar lock+lease cuando el PID ya no matchea por PID+start-time aunque el deadline no haya vencido, y para que cleanup_only del sweeper elimine lock+lease o falle duro."
question: "Confirmas devolucion a Codex por los dos slips falsables de exec-lease?"
---

# REVIEW TASK-0235 exec-lease

rr=true.

Veredicto: CAMBIO-REQUERIDO / NO-GO.

Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0235-exec-lease-veredicto.md`.

Resumen: gates verdes, pero el probe propio contra la funcion real `Clear-StaleCronLockIfSafe` deja
`lock_exists=true` y `lease_exists=true` cuando el PID esta muerto antes del deadline. Ademas,
`sweep_cron_zombies.py --kill` con lease vencido y proceso muerto devuelve `cleanup_only` EXIT 0 sin borrar lock ni
lease. El incidente motivador sigue reproducible.
