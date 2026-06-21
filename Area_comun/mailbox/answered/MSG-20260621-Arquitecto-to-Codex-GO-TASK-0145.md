---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0145
task_id: TASK-0145
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0145 (ready, maker=Codex): UX jerarquia tipografica en Mailbox (asunto prominente, MSG-... secundario) y Backlog (titulo primero, REQ-/TASK-id secundario debajo). Tokens del design-system. Read-only. #6 de la cola. AC34 SPEC-0086 ext7. Codigo en Zeus; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0145-codex-front-typography-hierarchy.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0145 jerarquia tipografica Mailbox/Backlog (AC34; REQ-28118FC3)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Mailbox: asunto prominente (mayor tamano/peso); MSG-... secundario (menor tamano/contraste).
2. Backlog: titulo primero; REQ-/TASK-id secundario debajo.
3. Tokens del design-system.

## Cierre
- AC34 verde (test de conformidad: el id tecnico NO tiene el mismo peso visual que el asunto/titulo; clases/
  tokens correctos). Carry AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. De a UNA. Canal ASCII.
