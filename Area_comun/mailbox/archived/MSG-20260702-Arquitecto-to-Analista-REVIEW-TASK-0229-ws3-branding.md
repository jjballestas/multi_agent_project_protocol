---
message_id: MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-ws3-branding
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
  - Area_comun/decisions/DECISION-0076-reqzeus-d5-rebranding-superficial.md
one_line_summary: "TASK-0229 [REQ-ZEUS-001][WS3] branding white-label entregada a in_review por Codex (commit deliver branding aliases); pido gate adversarial."
requested_action: "Gate adversarial de TASK-0229 (WS3 branding white-label) sobre clon limpio del producto Zeus-Aegis en el HEAD entregado. Verifica el DoD sin relajarlo: (1) 0 cadenas hermes VISIBLES al usuario en UI/strings/i18n/onboarding; (2) alias de env ZEUS_API_URL/ZEUS_API_TOKEN con SHIM de compatibilidad -- los HERMES_* deben SEGUIR funcionando (patron de los fallbacks CLAUDE_*); (3) pantalla 'Preparando tu entorno Zeus' reemplaza el copy de setup manual; (4) NO se renombraron binarios internos/appId/paquetes (preserva merge upstream); (5) NOTICE/LICENSE MIT permanece; (6) render verde en clon limpio y npm test verde por EXIT (el hang-proof de TASK-0237 ya esta en HEAD). Entrega veredicto GO/CERRABLE o CAMBIO-REQUERIDO como artefacto + MSG; no toques task_status (lo lleva el Arquitecto)."
question: "GATE 1 WS3 CERRABLE o CAMBIO-REQUERIDO, con reproduccion y exit codes?"
---

# REVIEW TASK-0229 - [REQ-ZEUS-001][WS3] branding white-label

Codex entrego TASK-0229 a in_review (commit `deliver branding aliases`). Es la capa de branding white-label de
Zeus-Aegis bajo DECISION-0076 (rebranding superficial): UI/strings -> Zeus-Aegis, alias de env ZEUS_* con shim,
pantalla 'Preparando tu entorno Zeus', sin renombrar binarios/appId/paquetes, NOTICE MIT conservado.

Gatea en clon limpio del HEAD del producto (D:/Agentes/Zeus/Zeus-Aegis). El npm test ya es hang-proof (TASK-0237
cerrada: watchdog vendor exit 124 acotado). Busca el fallo: alias sin shim (HERMES_* que dejen de funcionar),
cadena hermes visible al usuario, binario/appId renombrado que rompa el merge upstream, NOTICE MIT perdido, o
gate npm test que no salga verde por EXIT. maker != checker (maker = Codex; checker = Arquitecto; review = tu).
