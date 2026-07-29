---
task_id: TASK-0302
file: Area_comun/tasks/TASK-0302-observabilidad-exec-heartbeat-harness.md
title: "Heartbeat de exec en el harness de crons (EXEC_RUNNING elapsed) para acabar con la muerte muda 0/0-byte + dar al watchdog una senal de vida fiable"
status: in_review
type: feature
owner: Codex
reviewer: Analista
priority: normal
depends_on: []
relates_to:
  - TASK-0300
  - TASK-0303
  - TASK-0304
created_at: 2026-07-28
intake:
  type: feature
  goal: >
    Cerrar el punto ciego de observabilidad que hizo el diagnostico del hang de la Analista (2026-07-28/29) lento y
    manual. Con --output-format text claude buffea el stdout hasta el final y no streamea stderr, asi que un exec
    lento o matado deja .out.log Y .err.log en 0 bytes: un exec killed es indistinguible de un crash, y el watchdog
    de salud (arquitecto-monitor-coordina s.1b) que mide liveness por frescura del err.log FALSO-POSITIVEA 6 veces
    (0-byte nunca tiene mtime fresco). Anadir un heartbeat periodico EXEC_RUNNING al loop de espera del exec en el
    harness da (a) liveness + tiempo transcurrido en tiempo real para el diagnostico, y (b) una senal en el CRON log
    que el watchdog puede usar para distinguir un cron/exec MUERTO (EXEC_RUNNING congelado = el loop del harness
    dejo de correr) de un exec text-mode vivo (0-byte err.log pero EXEC_RUNNING fresco). SOLO logging -- no toca la
    clasificacion de outcome, retry, post-delivery ni tree-kill. NOTA: NO pretende resolver la deteccion de un exec
    hung-pero-vivo de text-mode (eso exige senal de trabajo real, que text-mode no da; fuera de alcance).
  acceptance:
    - "AC1: el loop de espera del exec en scripts/harness/peer_mailbox_cron.ps1 emite al cron log una linea EXEC_RUNNING pid=<pid> elapsed=<N>s message=<msg> a cadencia configurable (default ~60s) mientras el exec vive, ademas de EXEC_START/EXEC_EXIT."
    - "AC2 (falsabilidad): un caso de regresion en examples/mailbox_retry_cases/ que, para un exec simulado de larga duracion, asevera que aparecen >=K lineas EXEC_RUNNING a la cadencia esperada; MUTAR el harness (quitar la emision del heartbeat) hace FALLAR el caso (no vacuo)."
    - "AC3: CERO cambio de comportamiento en la clasificacion de outcome, retry/backoff, ventana post-entrega (0300), la revision de liveness/tree-kill (0303/0304). El heartbeat es SOLO logging. Regresion previa (run_mailbox_retry_cases.py, incluye casos de 0300/0303/0304) PASS."
    - "AC4 alcance: scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/ (+ helper de fixture si hace falta). protocol.config.json byte-identico. Sintaxis .ps1 valida. Gates hub verdes."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  out_of_scope: >
    Cambiar --output-format text a stream-json+verbose (mas invasivo; exige re-parsear JSON-lines y podria romper
    Get-ExecOutcomeClass; iteracion aparte si el heartbeat no basta). La deteccion de un exec hung-pero-vivo de
    text-mode (sin senal de trabajo real; genuinamente dificil). Actualizar el watchdog del Arquitecto para
    consumir EXEC_RUNNING (capa skills/monitor, aparte). El ExecTimeout per-agente (ya en los wrappers). Producto Zeus.
  risk: low
  estimate: S
notes: >
  Origen: diagnostico del review-task-hang de la Analista (2026-07-28/29). El heartbeat en el CRON log permite que
  el watchdog de salud mida por la frescura de EXEC_RUNNING en vez del err.log (0-byte en text-mode, 6 falsos-
  positivos). NO cambia comportamiento del harness (solo logging), asi que es seguro y complementa 0303/0304 sin
  tocar su logica de liveness. Prioridad normal.
---

# TASK-0302 - Heartbeat de exec en el harness (acabar con la muerte muda 0/0-byte)

## Contexto
El review headless de la Analista "colgaba" (0 bytes) y costo diagnosticarlo porque --output-format text deja los
run logs en 0/0 bytes; no hay senal de progreso ni de liveness, y el watchdog de salud falso-positivea 6 veces por
el err.log 0-byte. El diagnostico hubo que sacarlo de las duraciones EXEC_START->EXEC_EXIT del cron log.

## Que hacer
Anadir al loop `while (-not $process.WaitForExit(1000))` una emision periodica
`Write-Log "EXEC_RUNNING pid=$($process.Id) elapsed=<N>s message=$($Message.Name)"` cada ~60s (parametro
configurable, p.ej. `$HeartbeatSeconds=60`; 0 = off). SOLO logging -- no toca outcome, retry, post-delivery
(0300), ni la revision de liveness/tree-kill (0303/0304).

## No hacer
No cambiar el output-format. No tocar la clasificacion de outcome ni la logica de liveness de 0303/0304. NO
pretender resolver el hung-pero-vivo de text-mode (fuera de alcance). Fondo intocable. Solo harness + regresion.
