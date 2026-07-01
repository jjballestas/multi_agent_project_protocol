---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0235-remediacion
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-01
task_id: TASK-0235
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0235-exec-lease-veredicto.md
  - Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md
one_line_summary: "TASK-0235 NO-GO: el self-heal deja lock+lease cuando el PID muere ANTES del deadline; y sweep --kill cleanup_only sale EXIT 0 sin borrar. Dos slips falsables."
requested_action: "Remediar TASK-0235 (dos slips del veredicto Analista, ambos confirmados por probe contra la funcion real): (1) Clear-StaleCronLockIfSafe debe ELIMINAR lock+lease cuando el proceso ya no matchea por PID+start-time, AUNQUE el deadline no haya vencido (hoy solo limpia con lease vencido -> un exec muerto pre-deadline bloquea la cola hasta 1h; es el incidente motivador, sigue reproducible); (2) sweep_cron_zombies.py --kill, con lease vencido y proceso muerto, debe BORRAR lock+lease de verdad (hoy devuelve cleanup_only EXIT 0 sin borrar) o fallar duro. Anadir tests reproducibles de ambos: PID-muerto-pre-deadline se auto-limpia; cleanup_only borra o falla. Redelivery a in_review."
---

# ACTION TASK-0235 - remediacion (self-heal por PID-muerto + cleanup_only real)

Veredicto Analista (`ANALISTA-TASK-0235-exec-lease-veredicto.md`): CAMBIO-REQUERIDO / NO-GO. Confirma con probe
contra la funcion real los dos slips (uno lo levante yo como checker en vivo hoy):

1. `Clear-StaleCronLockIfSafe` deja `lock_exists=true` y `lease_exists=true` cuando el PID esta muerto ANTES del
   deadline. Debe auto-limpiar en cuanto el proceso ya no matchea por PID + start-time, sin esperar el deadline.
   (Hoy tres execs de review murieron pre-deadline y bloquearon la cola horas -- lo destrabe a mano 3 veces.)
2. `sweep_cron_zombies.py --kill` con lease vencido + proceso muerto devuelve `cleanup_only` EXIT 0 pero NO borra
   lock ni lease. Debe borrarlos de verdad, o fallar duro con codigo != 0.

Pedido: arreglar ambos, con tests reproducibles (PID-muerto-pre-deadline -> auto-limpia; cleanup_only -> borra o
falla). Conservar el resto de gates verdes. Redelivery a in_review; luego re-ruteo al Analista.
