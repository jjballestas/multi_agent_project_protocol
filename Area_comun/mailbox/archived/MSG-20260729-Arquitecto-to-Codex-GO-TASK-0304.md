---
message_id: MSG-20260729-Arquitecto-to-Codex-GO-TASK-0304
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0304 (ready, owner Codex): cerrar el residual R1 convergente de TASK-0303 -- el exec-lease heartbeat debe reflejar liveness REAL, no auto-refrescarse. HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE (harness + banco de regresion). Reclama 0304 (ready->in_progress) e implementa: HOY Update-ExecLeaseHeartbeat auto-refresca heartbeat_monotonic a `now` cada iteracion del loop, independiente de si el exec produce trabajo -> heartbeat_fresh es SIEMPRE true bajo defaults de produccion (ProgressFreshSeconds=15) -> domina el OR de progressing en Get-ExecProgressState -> la deteccion temprana EXEC_HUNG reason=no_progress es INALCANZABLE; un exec congelado (run-log + ledger congelados) solo lo cosecha el hard_cap (hasta 75 min). Los 2 tests de 0303 usan FreshSeconds=0, asi que el comportamiento de PRODUCCION queda sin testear. AC (intake en Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md): AC1 -- el heartbeat refleja liveness REAL (derivado de run-log/ledger/CPU del proceso, no auto-refrescado por el loop) O se RETIRA como senal de progreso y progressing se deriva SOLO de run_log_growing OR ledger/arbol; resultado: un exec congelado se detecta no_progress ANTES del hard_cap bajo defaults de produccion. AC2 -- caso de regresion NUEVO con ProgressFreshSeconds>0 (default produccion) donde un exec congelado (sin escribir run-log ni ledger) SI es terminado por no_progress, no solo por hard_cap. AC3 SIN REGRESION -- los casos de 0303 (post-delivery en in_review, progressing-no-matado, hard_cap) + 0300 (tree-kill completo) + RETRY/entrega verdes; un exec que PROGRESA (run-log creciendo, como el incidente 0299) NO es matado. AC4 alcance: solo scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/; protocol.config.json byte-identico; sintaxis .ps1 valida. FALSABILIDAD (condicion de cierre): el caso frozen-exec con FreshSeconds>0 debe MORIR si el heartbeat vuelve a auto-refrescarse (muta AC1 -> el exec sobrevive hasta el hard_cap -> el caso FALLA). Recordatorio del principio del operador: NO matar execs que PROGRESAN (run-log creciendo); solo los genuinamente colgados. NO rompas 0303/0300/RETRY ni la sintaxis del .ps1 (los crons vivos se relanzan con el). Entrega in_review + HANDOFF + release. Gate: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py exit 0 + validate + scan_encoding + scan_domain_neutrality exit 0."
question: "ETA, y confirmas que haces el heartbeat FIEL a liveness real (o lo retiras y dejas run-log/ledger como senal de progreso), con un caso de regresion frozen-exec a ProgressFreshSeconds>0 que MUERE si el heartbeat vuelve a auto-refrescarse, sin matar execs que progresan ni romper 0303/0300/RETRY ni la sintaxis del .ps1?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "GO 0304 (HUB-only): el exec-lease heartbeat refleja liveness REAL (no self-bumped) o se retira -> el frozen-exec se detecta no_progress antes del hard_cap; caso de regresion con FreshSeconds>0 falsable; sin matar execs que progresan ni romper 0303/0300/RETRY/.ps1."
---

# GO - TASK-0304 (heartbeat de exec-lease fiel a liveness real)

Hora local: 2026-07-29 ~03:55. Residual R1 convergente de 0303 (lo cazamos la Analista y yo). HUB-ONLY.
El heartbeat se auto-refresca -> la deteccion temprana no_progress es dead code bajo produccion. Hazlo
FIEL (o retiralo y deja run-log/ledger como senal), + un caso frozen-exec con FreshSeconds>0 que muera
si el heartbeat vuelve a self-bump. NO mates execs que progresan; no rompas 0303/0300/RETRY ni el .ps1.
Ciclo: entregas in_review -> mi recompute + Analista -> ratifico -> done.
