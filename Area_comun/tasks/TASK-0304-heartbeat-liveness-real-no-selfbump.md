---
task_id: TASK-0304
file: Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md
title: "Harness: el exec-lease heartbeat debe reflejar liveness REAL (no auto-refrescarse) + cobertura frozen-exec con ProgressFreshSeconds>0"
status: done
type: infra
owner: Codex
reviewer: Analista
priority: normal
depends_on:
  - TASK-0303
relates_to:
  - TASK-0303
  - TASK-0302
created_at: 2026-07-29
intake:
  type: infra
  goal: >
    Cerrar el residual R1 convergente de TASK-0303 (lo cazaron independientemente el recompute del Arquitecto y la
    Analista). El fix de 0303 revisa liveness al vencer el deadline via progressing = heartbeat_fresh OR run_log_growing
    OR ledger/arbol. PERO Update-ExecLeaseHeartbeat auto-refresca heartbeat_monotonic a `now` en CADA iteracion del
    loop, independiente de si el exec produce trabajo -> heartbeat_fresh es SIEMPRE true bajo defaults de produccion
    (ProgressFreshSeconds=15) -> progressing es SIEMPRE true mientras el proceso vive -> la rama de hung-detection
    temprana (EXEC_HUNG reason=no_progress) es INALCANZABLE; un exec genuinamente congelado (run-log + ledger
    congelados) solo lo cosecha el hard_cap (hasta 75 min el exec principal, 20 min post-entrega). Ambos tests de 0303
    fijan ProgressFreshSeconds=0 (neutralizan el heartbeat), asi que el comportamiento de PRODUCCION queda sin testear.
    NO es un defecto de correccion (yerra en direccion segura: hacia NO matar, que es el principio del operador; el
    hard_cap acota; el caso REAL de 0299 tenia run-log CRECIENDO, cubierto por run-log) -- por eso 0303 cerro. Pero la
    senal heartbeat es enganosa y hay un gap de cobertura. Este fix hace la senal de liveness FIEL.
  acceptance:
    - "AC1 HEARTBEAT FIEL O RETIRADO: el exec-lease heartbeat refleja liveness REAL del exec (p.ej. derivado del run-log/ledger/CPU del proceso, no auto-refrescado por el loop del harness), O se RETIRA como senal de progreso y el progressing se deriva SOLO de run_log_growing OR ledger/arbol (senales de salida real). El resultado: un exec congelado (run-log + ledger congelados) se detecta como no_progress ANTES del hard_cap bajo defaults de produccion."
    - "AC2 COBERTURA FROZEN-EXEC CON DEFAULTS DE PRODUCCION: un caso de regresion NUEVO en examples/mailbox_retry_cases/ con ProgressFreshSeconds>0 (default de produccion) donde un exec congelado (sin escribir run-log ni ledger) SI es terminado por no_progress (no solo por hard_cap). MUTAR: revertir AC1 (heartbeat vuelve a auto-refrescarse) -> el caso FALLA (el exec sobrevive hasta el hard_cap)."
    - "AC3 SIN REGRESION: los casos de 0303 (post-delivery en in_review, progressing-no-matado, hard_cap) y de 0300 (tree-kill completo) + RETRY/entrega siguen verdes. Un exec que PROGRESA (run-log creciendo, como el incidente 0299) NO es matado."
    - "AC4 ALCANCE: scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/. protocol.config.json byte-identico. Sintaxis del .ps1 valida. Gates hub verdes."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  out_of_scope: >
    El watchdog de salud del Arquitecto (arquitecto-monitor-coordina s.1b) tiene el defecto ESPEJO -- mide liveness
    por frescura del err.log, que en text-mode es 0-byte (falso "colgado", 4 falsos-positivos el 28-29 jul). Deberia
    usar la MISMA senal de liveness real (run-log/ledger/exec-lease heartbeat FIEL); pero eso es capa skills/monitor,
    no el harness -- se aborda aparte (nota en la skill). El heartbeat de logging EXEC_RUNNING (TASK-0302).
  risk: low
  estimate: S
notes: >
  Origen: residual R1 CONVERGENTE del review de 2 capas de TASK-0303 (2026-07-29). El recompute del Arquitecto y la
  Analista lo cazaron independientemente y ambos lo declararon no bloqueante (yerra seguro + hard_cap acota + caso
  real cubierto por run-log). Este fix elimina la senal enganosa. Conexion: el watchdog de salud tiene el defecto
  ESPEJO (err.log 0-byte -> falso colgado); la leccion comun = medir liveness por PROGRESO REAL, no por heartbeats
  self-bumped ni logs vacios. Prioridad normal (0303 ya cierra correcto en direccion segura).
---

# TASK-0304 - Heartbeat de exec-lease fiel a liveness real (no auto-refrescado) + cobertura frozen-exec

## Contexto (residual R1 convergente de TASK-0303, 2026-07-29)
El fix de 0303 (revisar liveness antes de matar) usa `progressing = heartbeat_fresh OR run_log_growing OR ledger`.
Pero `Update-ExecLeaseHeartbeat` auto-refresca el heartbeat a `now` cada iteracion, asi que `heartbeat_fresh` es
SIEMPRE true bajo defaults de produccion (ProgressFreshSeconds=15) y DOMINA el OR -> la deteccion temprana
`no_progress` es dead code; un exec congelado solo lo mata el hard_cap. Los 2 tests de 0303 usan FreshSeconds=0
(neutralizan el heartbeat), asi que produccion queda sin testear. No es defecto de correccion (yerra seguro, hard_cap
acota, el caso real de 0299 tenia run-log creciendo) -- por eso 0303 cerro -- pero la senal es enganosa.

## Que hacer
Hacer el heartbeat FIEL a liveness real (o retirarlo del OR y dejar run_log/ledger como senales de progreso) + un
caso de regresion frozen-exec con FreshSeconds>0 que MUERA si el heartbeat vuelve a auto-refrescarse.

## No hacer
No matar execs que PROGRESAN (run-log creciendo). No quitar el hard_cap ni el tree-kill de 0300. Solo harness + regresion.
