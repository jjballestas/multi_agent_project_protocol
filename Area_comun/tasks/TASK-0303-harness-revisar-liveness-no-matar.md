---
task_id: TASK-0303
file: Area_comun/tasks/TASK-0303-harness-revisar-liveness-no-matar.md
title: "Harness: al vencer el timeout REVISAR liveness antes de terminar (no matar un exec que progresa) + post-delivery gatilla en in_review no en el reclamo"
status: ready
type: infra
owner: Codex
reviewer: Analista
priority: high
depends_on: []
relates_to:
  - TASK-0300
  - TASK-0302
created_at: 2026-07-28
intake:
  type: infra
  goal: >
    Cerrar dos defectos del harness de crons (scripts/harness/peer_mailbox_cron.ps1) cazados el 2026-07-28 con
    TASK-0299, ambos instancias del mismo principio del operador ("un timeout que vence NO debe matar un proceso
    que trabaja; se revisa su estado y se decide"). DEFECTO A (post-delivery gatilla demasiado pronto): la ventana
    post-entrega arranca ante CUALQUIER escritura al ledger (Get-OwnEvidence = crecimiento de events.jsonl). Un GO
    de una tarea ready hace que el maker flipee ready->in_progress AL INICIO (escritura temprana) -> el
    post-delivery arranca a los pocos minutos, NO en la entrega, y con un timeout corto MATA al maker a mitad de
    IMPLEMENTACION. Afecta a TODA tarea GO'd desde ready. DEFECTO B (kill a ciegas): al vencer el deadline
    (ExecTimeout o post-delivery), el harness hace TREE_KILL sin revisar si el exec PROGRESA -- mato a Codex con el
    err.log creciendo (2MB) y el exec-lease heartbeat fresco (trabajando). El operador: no matar en pleno proceso;
    revisar estado y decidir.
  acceptance:
    - "AC1 POST-DELIVERY GATILLA EN LA ENTREGA: la ventana post-entrega arranca SOLO cuando el exec produce la senal de ENTREGA (transicion a in_review de una tarea que el actor posee), NO ante el reclamo ready->in_progress ni ante escrituras de claim/memoria previas a la entrega. Test: un exec que reclama+flipea a in_progress y luego trabaja 20 min NO entra en la ventana post-entrega hasta que flipea a in_review."
    - "AC2 REVISION DE LIVENESS ANTES DE TERMINAR: al vencer el deadline (ExecTimeout o post-delivery), el harness REVISA liveness (exec-lease heartbeat fresco <=Ns AND/OR run-log creciendo AND/OR crecimiento de ledger/arbol) y solo hace TREE_KILL si el exec esta GENUINAMENTE COLGADO; si PROGRESA, extiende una ventana acotada y re-evalua (con un tope duro configurable para no correr infinito), logueando la decision (EXEC_PROGRESSING/EXEC_HUNG)."
    - "AC3 (falsabilidad): tests que MUEREN ante su mutacion -- (a) un exec que reclama+trabaja-sin-entregar NO dispara el post-delivery (mutar: revertir a gatillar-en-cualquier-escritura -> el test falla); (b) un exec PROGRESANDO al vencer el deadline NO es matado (mutar: revertir a kill-incondicional -> el test falla, ve el kill); (c) un exec COLGADO (heartbeat stale + log congelado) SI es terminado."
    - "AC4 SIN REGRESION: RETRY/backoff, entrega gobernada, tree-kill de arbol completo (TASK-0300), y el flujo maker/checker intactos. El tope duro evita que un exec verdaderamente colgado corra para siempre."
    - "AC5 ALCANCE: scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/ (regresion). protocol.config.json byte-identico. Gates hub verdes."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  out_of_scope: >
    El heartbeat de logging EXEC_RUNNING (TASK-0302, complementario -- da la senal que AC2 consume). Los timeouts
    per-agente (ya en los wrappers). Producto Zeus. El punto ciego de observabilidad del text-mode (TASK-0302).
  risk: medium
  estimate: M
notes: >
  Origen: incidente TASK-0299 (2026-07-28) + DIRECTIVA del operador "no se deberia matar un proceso que este
  trabajando... revisar y determinar su estado, no matarlo en pleno proceso". Mitigacion inmediata desplegada
  mientras: Codex PostDelivery=1800 (=ExecTimeout) para que la ventana no mate temprano. Este fix quita la
  mitigacion cruda y hace el harness CORRECTO. Se apoya en el exec-lease heartbeat (ya existe) y el run-log
  freshness; TASK-0302 anade el heartbeat de logging que refuerza la senal. PRIORIDAD ALTA: afecta a toda tarea
  GO'd desde ready.
---

# TASK-0303 - El harness revisa liveness antes de terminar (no mata a ciegas) + post-delivery en la entrega

## Contexto (incidente 2026-07-28, TASK-0299)
Al hacer GO de 0299 (tarea ready), Codex flipeo ready->in_progress al inicio -> el post-delivery de 600s arranco
a los 3 min (no en la entrega) -> TREE_KILL a mitad de implementacion a las 20:07, con el err.log CRECIENDO y el
exec-lease heartbeat FRESCO (Codex trabajando, no colgado). Quedaron 3 claims huerfanos + trabajo perdido. El
operador dio la directiva: un timeout que vence NO mata a ciegas; revisa el estado (progresa vs colgado) y decide.

## Los 2 defectos
- **A (post-delivery temprano):** `Get-OwnEvidence` gatilla ante cualquier escritura al ledger. Debe gatillar
  SOLO en la senal de ENTREGA (in_review), no en el reclamo ready->in_progress.
- **B (kill a ciegas):** al vencer el deadline, `Stop-ExpiredLeaseProcess`/TREE_KILL corre sin revisar liveness.
  Debe REVISAR (heartbeat + run-log freshness + progreso) y solo matar si esta colgado; si progresa, extender
  acotado + re-evaluar (con tope duro).

## No hacer
No quitar el tree-kill de arbol completo (TASK-0300). No correr infinito (tope duro). Solo el harness + regresion.
