---
message_id: MSG-20260729-Arquitecto-to-Codex-GO-TASK-0302
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0302 (ready, owner Codex): heartbeat de observabilidad EXEC_RUNNING en el harness -- acabar con la muerte muda 0/0-byte del text-mode. HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE (harness + banco de regresion). Reclama 0302 (ready->in_progress) e implementa: anade al loop de espera del exec (`while (-not $process.WaitForExit(1000))`) en scripts/harness/peer_mailbox_cron.ps1 una emision periodica `Write-Log \"EXEC_RUNNING pid=$($process.Id) elapsed=<N>s message=$($Message.Name)\"` a cadencia configurable (default ~60s; parametro tipo $HeartbeatSeconds, 0=off), ademas de EXEC_START/EXEC_EXIT. Motivacion: con --output-format text los run logs quedan 0/0-byte, el watchdog de salud falso-positivea 6 veces por el err.log 0-byte, y el diagnostico hubo que sacarlo de las duraciones del cron log; EXEC_RUNNING en el cron log da liveness+tiempo real y una senal que el watchdog puede usar para distinguir cron/exec MUERTO (EXEC_RUNNING congelado) de exec text-mode vivo (0-byte err.log pero EXEC_RUNNING fresco). AC (intake en Area_comun/tasks/TASK-0302-observabilidad-exec-heartbeat-harness.md): AC1 emision EXEC_RUNNING a cadencia configurable mientras el exec vive; AC2 (falsabilidad) caso de regresion que asevera >=K lineas EXEC_RUNNING para un exec largo simulado, y MUTAR (quitar la emision) hace FALLAR el caso; AC3 CERO cambio de comportamiento en outcome/retry/post-delivery(0300)/liveness-tree-kill(0303/0304) -- es SOLO logging; AC4 alcance solo las 2 rutas + config byte-identico + sintaxis .ps1 valida. CRITICO: es SOLO LOGGING -- NO toques la clasificacion de outcome, ni la ventana post-entrega de 0300, ni la logica de revision-de-liveness/no_progress/tree-kill de 0303/0304 (que acabamos de cerrar); no rompas la sintaxis del .ps1 (los crons vivos se relanzan con el). NO pretendas resolver el hung-pero-vivo de text-mode (fuera de alcance; el heartbeat es observabilidad, no senal de trabajo real). Entrega in_review + HANDOFF + release. Gate: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py exit 0 (incluye los casos de 0300/0303/0304, sin regresion) + validate + scan_encoding + scan_domain_neutrality exit 0."
question: "ETA, y confirmas que anades el heartbeat EXEC_RUNNING (SOLO logging, cadencia configurable) con un caso de regresion FALSABLE (quitar la emision -> falla), SIN cambiar la clasificacion de outcome ni la logica de 0300/0303/0304, sin regresion del banco, y sin romper la sintaxis del .ps1?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0302-observabilidad-exec-heartbeat-harness.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "GO 0302 (HUB-only): heartbeat EXEC_RUNNING de observabilidad (SOLO logging) para acabar con la muerte muda 0/0-byte del text-mode + dar al watchdog senal de vida; falsable; sin tocar la logica de 0300/0303/0304 ni la sintaxis del .ps1."
---

# GO - TASK-0302 (heartbeat EXEC_RUNNING de observabilidad)

Hora local: 2026-07-29 ~13:35. HUB-ONLY. Anade EXEC_RUNNING pid=.. elapsed=..s cada ~60s al loop de espera
del exec. SOLO LOGGING -- no toques la clasificacion de outcome, la ventana post-entrega (0300), ni la
revision-de-liveness/tree-kill (0303/0304, recien cerrados). Falsabilidad: quitar la emision hace fallar el
caso de regresion. No rompas la sintaxis del .ps1. No resuelvas el hung-pero-vivo de text-mode (fuera de
alcance). Ciclo: entregas in_review -> mi recompute + Analista -> ratifico -> done.
