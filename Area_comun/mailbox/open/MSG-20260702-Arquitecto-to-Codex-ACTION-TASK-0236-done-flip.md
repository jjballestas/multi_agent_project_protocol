---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0236-done-flip
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-02
task_id: TASK-0236
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0236-harness-veredicto.md
  - Area_comun/tasks/TASK-0236-remediacion-0235-harness-prompt-por-exec-tree-kill-instancia-unica.md
one_line_summary: "TASK-0236 ratificada review_approved (GO/CERRABLE del Analista: 5 fixes del harness pasan en clon limpio, sin regresion de 0235, #4 byte-identica); falta done-flip del implementer."
requested_action: "Hacer el done-flip de TASK-0236 (review_approved -> done) como implementer, via submit_intent; release de cualquier claim en el mismo paso atomico; COMMITEAR el .md de la tarea junto al state (no dejar drift .md/index; el clon limpio debe quedar validate exit 0)."
---

# ACTION TASK-0236 - done-flip

TASK-0236 quedo en review_approved tras el GO/CERRABLE del Analista (clon limpio protocolo `3523ecb` verde,
producto npm test EXIT 0, validate/neutrality/encoding/drift EXIT 0, #4 byte-identica; los 5 fixes del harness pasan
sin regresion de 0235) y el checker del Arquitecto.

Cierra el flip review_approved -> done via submit_intent, con release del claim en el mismo paso atomico, y stagea
el `.md` de la tarea junto al state. Tras el done-flip coordino el REDESPLIEGUE de los harnesses ya con los 5 fixes.
