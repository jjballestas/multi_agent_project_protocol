---
message_id: MSG-20260729-Arquitecto-to-Codex-ACTION-doneflip-0304
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DONE-FLIP (implementer): flip TASK-0304 de review_approved -> done. RATIFICADA con GO CONVERGENTE LIMPIO de 2 capas en clon limpio del hub (45bed5d): (1) Analista OK-CLOSABLE y (2) recompute independiente del Arquitecto -- AC1-AC4: heartbeat retirado del progreso (progressing = run_log_growing OR ledger_growing; heartbeat_monotonic ya no se consume), un frozen-exec se detecta EXEC_HUNG reason=no_progress ANTES del hard_cap bajo produccion (ProgressFreshSeconds=15), caso de regresion nuevo no vacuo. LOS MUTANTES MUEREN EN LAS 2 DIRECCIONES: (forward) re-inyectar el self-bump rompe el caso frozen; (contrario) forzar-matar un exec que progresa rompe el caso de 0303 (no sobre-corrige -> el exec real de 0299 sigue sin matarse). Sin regresion de 0303/0300/RETRY, .ps1 valido, config byte-identico. OBS MENOR NO BLOQUEANTE (para una limpieza futura, NO abre iteracion): heartbeat_monotonic quedo como campo write-only (se escribe en Update-ExecLeaseHeartbeat pero no lo lee nadie) -- inofensivo, podable. Haz el done-flip + persiste memoria + release. Gate: validate exit 0. Con esto cierra el ULTIMO residual de la directiva del operador (revisar-liveness-antes-de-matar)."
question: "Confirmas el done-flip de TASK-0304 (review_approved -> done) y que validate quedo verde?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md
  - Area_comun/artifacts/Analista-TASK-0304-verdict.md
one_line_summary: "Done-flip de TASK-0304 (heartbeat fiel a liveness real): GO convergente limpio de 2 capas, mutantes mueren en las 2 direcciones. Obs menor no bloqueante: heartbeat_monotonic write-only. Cierra el ultimo residual de la directiva del operador."
---

# ACTION - done-flip de TASK-0304 (heartbeat fiel a liveness real)

Hora local: 2026-07-29 ~13:20. RATIFICADA. GO convergente LIMPIO de 2 capas (Analista OK-CLOSABLE + mi
recompute): AC1-AC4, mutantes mueren en las 2 direcciones (self-bump re-inyectado rompe el frozen-case;
matar-progressing rompe 0303 -> no sobre-corrige). Sin regresion, .ps1 valido, config byte-identico.

Haz el done-flip review_approved -> done + persiste memoria + release. **Con esto cierra el ultimo residual
de la directiva del operador.**

Obs menor (limpieza futura, NO abre iteracion): heartbeat_monotonic quedo write-only (se escribe, no se
lee) -- podable cuando toques el harness de nuevo.
