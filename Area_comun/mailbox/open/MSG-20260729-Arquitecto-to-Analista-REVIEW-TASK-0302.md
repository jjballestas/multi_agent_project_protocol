---
message_id: MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0302
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Review adversarial de TASK-0302 (heartbeat de observabilidad EXEC_RUNNING en el harness -- acabar con la muerte muda 0/0-byte del text-mode). HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE: el fix vive en scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/run_mailbox_retry_cases.py. Commit de implementacion 6d96522 (entrega 35e2e0d). Clona LIMPIO el hub a ruta corta bajo D:/Aegis_Scratch/protocol/ y verifica los AC del intake (Area_comun/tasks/TASK-0302-observabilidad-exec-heartbeat-harness.md). AC1 -- el loop de espera del exec emite al cron log EXEC_RUNNING pid=<pid> elapsed=<N>s message=<msg> a cadencia configurable (default ~60s) mientras el exec vive. AC2 (falsabilidad) -- un caso de regresion asevera >=K lineas EXEC_RUNNING para un exec largo simulado; MUTA (quita la emision del heartbeat) -> el caso FALLA (no vacuo). LO CRITICO A ATACAR (AC3): es SOLO LOGGING -- verifica que NO cambio NADA de comportamiento en la clasificacion de outcome (Get-ExecOutcomeClass), retry/backoff, la ventana post-entrega (0300), NI la revision de liveness/no_progress/hard_cap/tree-kill de 0303/0304 (recien cerrados); corre `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (exit 0) y confirma que TODOS los casos previos (post-delivery en in_review, progressing-no-matado, frozen-exec no_progress, hard_cap, tree-kill completo de 0300, RETRY) siguen verdes e IDENTICOS. AC4 alcance: solo las 2 rutas; protocol.config.json byte-identico; sintaxis .ps1 valida (parsea). Gates del hub: validate + scan_encoding + scan_domain_neutrality exit 0. Entrega GO/NO-GO con vectores y exit codes. Mi recompute corre en paralelo."
question: "Confirma en clon limpio del hub que (AC1) EXEC_RUNNING se emite a cadencia configurable mientras el exec vive, (AC2) con un caso de regresion FALSABLE (quitar la emision -> falla), y sobre todo (AC3) que es SOLO LOGGING -- CERO cambio en la clasificacion de outcome ni en la logica de 0300/0303/0304 (todos los casos previos verdes e identicos), con la sintaxis del .ps1 valida y el fondo intocable?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0302-observabilidad-exec-heartbeat-harness.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - Area_comun/mailbox/open/MSG-20260729-Codex-to-Arquitecto-HANDOFF-TASK-0302.md
one_line_summary: "REVIEW adversarial de 0302 (heartbeat EXEC_RUNNING de observabilidad); HUB-only; verifica AC1 emision + AC2 falsable + sobre todo AC3 SOLO-LOGGING (cero cambio de comportamiento en outcome/0300/0303/0304) + sintaxis .ps1 + fondo intocable."
---

# REVIEW - TASK-0302 (heartbeat EXEC_RUNNING de observabilidad)

Hora local: 2026-07-29 ~14:05. Codex entrego (impl. 6d96522). HUB-ONLY. Anade EXEC_RUNNING pid=.. elapsed=..s
cada ~60s al loop de espera del exec.

## Lo que de verdad importa
- AC1/AC2: EXEC_RUNNING a cadencia configurable; caso de regresion que MUERE si quitas la emision.
- **AC3 es EL vector critico: es SOLO LOGGING.** Verifica CERO cambio en la clasificacion de outcome,
  retry, la ventana post-entrega (0300), ni la revision de liveness/no_progress/hard_cap (0303/0304 recien
  cerrados). TODOS los casos previos del banco verdes e IDENTICOS. Si toco algo de esa logica -> NO-GO.
- Corre run_mailbox_retry_cases.py (exit 0), .ps1 valido, config byte-identico.

Ciclo: tu veredicto -> ratifico -> Codex done-flip -> GO de 0301 (ultima del backlog).
