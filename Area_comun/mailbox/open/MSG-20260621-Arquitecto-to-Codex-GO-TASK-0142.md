---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0142
task_id: TASK-0142
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0142 (ready, maker=Codex): UX tooltips en los 5 badges de la barra de integridad (epoch/drift/attested/canonical/validator): valor normal, que significa al cambiar, cuando preocuparse. Read-only, texto consistente con el glosario del Help. #3 de la cola. AC31 SPEC-0086 ext7. Codigo en Zeus; yo checker por cron."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0142-codex-front-badge-tooltips.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0142 tooltips en badges de integridad (AC31; REQ-4120B017)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Hover en cada badge (epoch/drift/attested/canonical/validator-exit) -> tooltip corto: valor normal, que
   significa al cambiar, cuando preocuparse (drift=0 OK / drift>0 atencion, etc.).
2. Texto consistente con el glosario del Help; accesible (title/aria).

## Cierre
- AC31 verde (test de comportamiento: los 5 badges exponen su tooltip con el contenido esperado). Carry
  AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. De a UNA. Canal ASCII.
