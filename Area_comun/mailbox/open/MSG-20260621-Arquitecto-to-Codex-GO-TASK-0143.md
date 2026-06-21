---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0143
task_id: TASK-0143
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0143 (ready, maker=Codex): UX tooltips en codigos RF-N (RF-5, RF-14...) y acronimos (SDD/T0/HMAC/PII...) en todas las vistas; codigos interactivos; diccionario UNA fuente unica compartida con el glosario del Help. Read-only. #4 de la cola. AC32 SPEC-0086 ext7. Codigo en Zeus; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0143-codex-front-rfn-tooltips.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0143 tooltips en codigos RF-N y acronimos (AC32; REQ-3E31293F)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Hover sobre RF-N (RF-5, RF-14...) o acronimo (SDD/T0/HMAC/PII...) -> nombre completo; codigos interactivos
   (cursor pointer).
2. Diccionario UNA fuente unica, compartida con el glosario del Help (no duplicar).

## Cierre
- AC32 verde (test de comportamiento: hover sobre RF-5/SDD/HMAC rinde el texto esperado; cubre los codigos que
  el front muestra). Carry AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. De a UNA. Canal ASCII.
