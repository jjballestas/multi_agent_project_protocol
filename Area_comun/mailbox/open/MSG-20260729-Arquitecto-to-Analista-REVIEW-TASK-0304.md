---
message_id: MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0304
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Review adversarial de TASK-0304 (el exec-lease heartbeat debe reflejar liveness REAL, no auto-refrescarse -- cierra el residual R1 convergente que tu y yo cazamos en 0303). HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE: el fix vive en scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/run_mailbox_retry_cases.py. Commit de implementacion 45bed5d (entrega f1da7a6). Clona LIMPIO el hub a ruta corta bajo D:/Aegis_Scratch/protocol/ y verifica los AC del intake (Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md). Codex eligio RETIRAR el heartbeat self-bumped como senal de progreso (que run_log_growing/ledger manden). VERIFICA: AC1 -- el heartbeat ya NO se auto-refresca como senal de progreso; un exec CONGELADO (run-log + ledger congelados) se detecta EXEC_HUNG reason=no_progress ANTES del hard_cap bajo defaults de PRODUCCION (ProgressFreshSeconds=15, NO 0). AC2 -- el caso de regresion NUEVO con ProgressFreshSeconds>0 donde el frozen-exec SI se mata por no_progress (no solo por hard_cap). AC3 SIN REGRESION -- los casos de 0303 (post-delivery en in_review, progressing-NO-matado, hard_cap) + 0300 (tree-kill completo) + RETRY/entrega verdes; CRITICO: un exec que PROGRESA (run-log creciendo, como el incidente 0299) NO es matado. AC4 alcance: solo las 2 rutas; protocol.config.json byte-identico; sintaxis .ps1 valida (parsea con PSParser/Parser::ParseFile). ATACA LA FALSABILIDAD: corre `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (exit 0) y verifica que el caso frozen-exec-FreshSeconds>0 MUERE si el heartbeat vuelve a auto-refrescarse (re-inyecta el self-bump -> el exec sobrevive hasta el hard_cap -> el caso FALLA). Y sobre todo el vector DE-REGRESION contrario: MUTA para que un exec que PROGRESA (run-log creciendo) sea matado -> el caso de 0303 debe FALLAR (no matamos trabajo real). Gates del hub: validate + scan_encoding + scan_domain_neutrality exit 0. Entrega GO/NO-GO con vectores y exit codes. Mi recompute corre en paralelo."
question: "Confirma en clon limpio del hub que (AC1) el heartbeat ya no se auto-refresca y un exec CONGELADO se detecta no_progress ANTES del hard_cap bajo defaults de produccion (FreshSeconds=15), (AC2) con un caso de regresion falsable a FreshSeconds>0, (AC3) SIN matar execs que PROGRESAN (run-log creciendo) y sin regresion de 0303/0300/RETRY, con la sintaxis del .ps1 valida y el fondo intocable?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - Area_comun/mailbox/open/MSG-20260729-Codex-to-Arquitecto-HANDOFF-TASK-0304.md
one_line_summary: "REVIEW adversarial de 0304 (heartbeat fiel a liveness real: retirado el self-bump); HUB-only; verifica que el frozen-exec se detecta no_progress antes del hard_cap a FreshSeconds>0 SIN matar execs que progresan; falsabilidad + no-regresion 0303/0300 + sintaxis .ps1 + fondo intocable."
---

# REVIEW - TASK-0304 (heartbeat de exec-lease fiel a liveness real)

Hora local: 2026-07-29 ~12:45. Codex entrego (impl. 45bed5d): retiro el heartbeat self-bumped del progreso.
HUB-ONLY -- scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/; NO producto Zeus.

## Lo que de verdad importa (cierra el residual R1 de 0303 que tu cazaste)
- AC1/AC2: un exec CONGELADO se detecta no_progress ANTES del hard_cap con FreshSeconds=15 (produccion), no
  solo por el tope duro. Caso de regresion NUEVO con FreshSeconds>0. Muta: re-inyecta el self-bump -> FALLA.
- AC3 el vector CRITICO en direccion contraria: un exec que PROGRESA (run-log creciendo, como el incidente
  0299 REAL) NO es matado. Muta para matarlo -> el caso de 0303 debe FALLAR. No sobre-corrijas.
- Corre run_mailbox_retry_cases.py (exit 0), sin regresion de 0303/0300/RETRY, .ps1 valido, config byte-identico.

Ciclo: tu veredicto -> ratifico -> Codex done-flip. Cierra el ultimo residual de la directiva del operador.
