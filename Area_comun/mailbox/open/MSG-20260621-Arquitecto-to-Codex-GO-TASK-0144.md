---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0144
task_id: TASK-0144
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0144 (ready, maker=Codex): UX render de diagramas Mermaid en la vista Help (secciones 4/5/6/7 -> SVG en vez de texto crudo) SIN agregar dependencia de servidor/npm (vendorizar la lib como asset estatico o SVG pre-generado; preservar 'sin dependencias'). Read-only. #5 de la cola. AC33 SPEC-0086 ext7. Codigo en Zeus; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0144-codex-front-mermaid-help.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0144 render Mermaid en Help (AC33; REQ-D2C6579F)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Bloques Mermaid de las secciones 4/5/6/7 del Help -> render SVG (no texto crudo).
2. SIN dependencia de servidor / npm install: vendorizar la lib mermaid como asset estatico, o SVG pre-generado.
   Preservar la propiedad "sin dependencias" de la consola.

## Cierre
- AC33 verde (test de comportamiento: el panel Help no muestra el codigo mermaid crudo; render presente; el
  server sigue sin deps de npm). Carry AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. De a UNA. Canal ASCII.
