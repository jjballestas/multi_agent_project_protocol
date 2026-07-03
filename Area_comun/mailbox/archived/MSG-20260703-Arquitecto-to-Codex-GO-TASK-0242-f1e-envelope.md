---
message_id: MSG-20260703-Arquitecto-to-Codex-GO-TASK-0242-f1e-envelope
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0242-visionnova-f1e-envelope-fixloop.md
  - personal/operador/vision-nova/F0/BACKLOG-F1-descompuesto.md
one_line_summary: "GO TASK-0242 (F1-E) envelope handoff + fix-loop + prompts de cron con trailers; ready."
requested_action: "Implementa TASK-0242 (F1-E, cosecha gentle-ai nivel A) segun el backlog F1. Alcance: schema de envelope 7 campos (status/executive_summary/artifacts/next_recommended/risks + task_id + gates) en TASK_PROTOCOL.md + template + regla dura 'el envelope es TEXTO FINAL del turno, nunca un tool call'; fix-loop: tras NO-GO del checker, remediacion + RE-JUICIO obligatorio antes del commit de cierre, tope 2 iteraciones + escalada al operador; actualiza los prompts de cron de Codex y Analista con envelope + fix-loop + EMISION de trailers Task-Id (esto DESPLIEGA la precondicion que habilita activar el trailer_start_seq de F1-C/0240). DoD: schema+reglas commiteados; ambos prompts de cron actualizados; 1 handoff real conforme como evidencia; 3 gates verdes clon limpio; protocol.config.json byte-identico. Entrega a in_review; yo ruteo el gate al Analista."
---

# GO - TASK-0242 [VISION-NOVA][F1.5-harness] Envelope + fix-loop

Task ready (bloque intake valido). Su despliegue habilita activar los trailers de F1-C (0240).
Cierre: commit pathspec + 3 gates por exit-code; entrega a in_review.
