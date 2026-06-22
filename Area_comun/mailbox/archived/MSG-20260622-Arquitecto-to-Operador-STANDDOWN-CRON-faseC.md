---
message_id: MSG-20260622-Arquitecto-to-Operador-STANDDOWN-CRON-faseC
task_id: TASK-0152
type: FYI
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "Detengo el cron de monitoreo (9954b818) tras 7 rondas sin que Codex tome el rework. Fase C (TASK-0152) queda BLOQUEADA en CAMBIO-REQUERIDO: el guard AC45 SLIPS en await import('openai')/import('undici')/net.connect-bare/axios-got (probado por el Analista; los must-catch que nombraste). El directivo de cambio esta en open/ esperando a Codex. Para avanzar: reactiva a Codex para que endurezca el guard (o re-arma el cron). Sin breach vivo (extractor deterministic-local); canonico verde HEAD aeac725."
context_refs:
  - Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0152-guard-AC45.md
  - Area_comun/artifacts/ANALISTA-TASK-0152-v2-faseC-veredicto.md
  - Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
deadline_or_blocking_level: normal
---

# STAND-DOWN del cron de monitoreo (9954b818) - Fase C esperando rework de Codex

Tras **7 rondas seguidas** sin que Codex re-reclamara la Fase C, detengo el cron de monitoreo (CronDelete
9954b818) segun la regla de auto-drive. Resumen de donde quedo todo:

## Estado de la carga por archivo v2
- **Fase A (TASK-0150): DONE.** Fase B (TASK-0151): **DONE** (checker Arquitecto + Analista OK 6/6).
- **Fase C (TASK-0152): in_review, BLOQUEADA en CAMBIO-REQUERIDO.** El Analista probo por comportamiento que el
  guard de egress AC45 (aunque ampliado a todo `src/**`) **SLIPS** en:
  - `await import("openai")` (SDK de modelo dinamico), `await import("undici")` (tu ejemplo explicito),
    `net.connect` por import bare, `axios`/`got`.
  - El control positivo solo ejercita `fetch`. Vectores 2-6 (purga/TTL, loop off+consent+cero-egress,
    fuera-del-ledger, carry AC40/43/44, #4 byte-identica) PASAN.
  - **No hay breach vivo** (el extractor es `deterministic-local`, cero egress), pero la teeth de AC45 no cierra
    la ruta `await import(...)`, la mas realista de la ventana de modelo.
- El **directivo de cambio para Codex** esta en `open/`
  (`MSG-...-Arquitecto-to-Codex-CAMBIO-TASK-0152-guard-AC45.md`): ampliar `sourceEgressViolations` (import
  dinamico + bare net/tls/dgram/http/https/dns + clientes undici/axios/got/node-fetch) o **flip a allowlist**,
  con control positivo POR patron. Falsable: `await import("openai")` debe dar violacion.

## Para retomar
- **Reactiva a Codex** para que tome el rework del guard (su cron ejecutor o un disparo manual); cuando re-entregue
  in_review, yo reproduzco como checker desde clon limpio y el **Analista re-verifica** el guard antes de cerrar
  (DECISION-0056). Puedo **re-armar el cron de monitoreo** cuando me lo indiques.
- **Uso vivo del extractor contra archivos reales = GO aparte tuyo** (sigue OFF-by-default, env-gated).

Canonico verde: HEAD==origin **aeac725**, validate con/sin secretos exit 0, drift 0, #4 byte-identica. Canal ASCII.
