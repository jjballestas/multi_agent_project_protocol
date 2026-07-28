---
task_id: TASK-0302
file: Area_comun/tasks/TASK-0302-observabilidad-exec-heartbeat-harness.md
title: "Heartbeat de exec en el harness de crons (EXEC_RUNNING elapsed) para acabar con la muerte muda 0/0-byte"
status: proposed
type: feature
owner: unassigned
reviewer: Analista
priority: normal
depends_on: []
relates_to:
  - TASK-0300
created_at: 2026-07-28
goal: >
  Cerrar el punto ciego de observabilidad que hizo el diagnostico del hang de la Analista (2026-07-28) lento y
  manual. Con `--output-format text` claude buffea el stdout hasta el final y no streamea stderr, asi que un exec
  lento o matado deja `.out.log` Y `.err.log` en 0 bytes: un exec killed es indistinguible de un crash, y el
  watchdog de "err.log congelado" no puede medir liveness (0-byte nunca tiene mtime fresco). El root cause real
  (ExecTimeout demasiado corto para las reviews de 12-37min) hubo que reconstruirlo de las DURACIONES del cron log,
  no de los run logs. Anadir un heartbeat periodico al loop de espera del exec en el harness da liveness + tiempo
  transcurrido en tiempo real, sin tocar la clasificacion de outcome ni el parseo del OUTCOME.
acceptance: >
  AC1: el loop de espera del exec en scripts/harness/peer_mailbox_cron.ps1 emite al cron log una linea
  `EXEC_RUNNING pid=<pid> elapsed=<N>s message=<msg>` a cadencia configurable (default ~60s) mientras el exec
  vive, ademas del EXEC_START/EXEC_EXIT ya existentes.
  AC2 (falsabilidad): un caso de regresion en examples/mailbox_retry_cases/ que, para un exec simulado de larga
  duracion, asevera que aparecen >=K lineas EXEC_RUNNING a la cadencia esperada; MUTAR el harness (quitar la
  emision del heartbeat) hace FALLAR el caso (no vacuo).
  AC3: CERO cambio de comportamiento en la clasificacion de outcome, retry/backoff, ventana post-entrega, o el
  TREE_KILL; el heartbeat es SOLO logging. Regresion previa (run_mailbox_retry_cases.py) PASS.
  AC4 alcance: scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/ (+ helper de fixture si hace
  falta). protocol.config.json byte-identico (git diff --exit-code). Gates hub verdes (validate + scan_encoding +
  scan_domain_neutrality exit 0).
verification_cmd: "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
scope_routes:
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
out_of_scope: >
  Cambiar --output-format text a stream-json+verbose (alternativa considerada pero mas invasiva: exige re-parsear
  la salida JSON-lines y podria romper Get-ExecOutcomeClass; se puede evaluar como iteracion SEPARADA si el
  heartbeat no basta). El ExecTimeout per-agente (ya arreglado en los wrappers, TASK aparte). Hangs de proveedor
  del LLM. Cualquier producto Zeus/Nova.
risk: low
estimate: S
notes: >
  Origen: diagnostico del review-task-hang de la Analista (2026-07-28). El heartbeat en el CRON log tambien
  permitiria que el watchdog de salud (arquitecto-monitor-coordina s.1b) mida liveness por la frescura de
  EXEC_RUNNING en vez del err.log (que en text-mode es 0-byte). Prioridad normal -- encolar cuando el operador
  priorice el backlog de endurecimiento.
---

# TASK-0302 - Heartbeat de exec en el harness (acabar con la muerte muda 0/0-byte)

## Contexto
El 2026-07-28 el review headless de la Analista "colgaba" (0 bytes). El root cause era ExecTimeout=600 matando
reviews de 12-37min, PERO costo diagnosticarlo porque `--output-format text` deja los run logs en 0/0 bytes al
matar el exec: no hay senal de progreso ni de liveness. El diagnostico hubo que sacarlo de las duraciones
EXEC_START->TREE_KILL del cron log.

## Que hacer
Anadir al loop `while (-not $process.WaitForExit(1000))` de `Invoke-...` (scripts/harness/peer_mailbox_cron.ps1)
una emision periodica `Write-Log "EXEC_RUNNING pid=$($process.Id) elapsed=<N>s message=$($Message.Name)"` cada
~60s (parametro configurable, p.ej. `$HeartbeatSeconds=60`; 0 = off). Es SOLO logging -- no toca outcome, retry,
post-delivery ni tree-kill.

## No hacer
No cambiar el output-format (eso es una iteracion aparte, mas invasiva). No tocar la clasificacion de outcome.
Fondo intocable byte-identico. Solo el harness + un caso de regresion falsable.
