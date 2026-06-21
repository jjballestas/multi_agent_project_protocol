---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0146
task_id: TASK-0146
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0146 (ready, maker=Codex): UX kanban del Backlog - columnas con count=0 compactas (solo cabecera) + columna done MUESTRA su contenido (lista o resumen paginado, no solo el numero) + ancho adaptado. Read-only. #7 de la cola. AC35 SPEC-0086 ext7. Codigo en Zeus; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0146-codex-front-kanban-collapse.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0146 kanban colapsar vacias + mostrar done (AC35; REQ-B97838C6)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Columnas count=0 -> compactas (solo cabecera, sin hueco).
2. Columna done MUESTRA su contenido (lista o resumen paginado).
3. Ancho del kanban adaptado al contenido real.

## Cierre
- AC35 verde (test de comportamiento: columna 0 -> compacto; done con N -> renderiza/pagina; no done con count
  sin lista). Carry AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. De a UNA. Canal ASCII.
