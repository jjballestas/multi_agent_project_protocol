---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0147
task_id: TASK-0147
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0147 (ready, maker=Codex): UX filtros del Ledger #4 por actor y por tipo de evento + paginacion/carga progresiva (no renderizar 900+); el texto libre sigue REDACTADO (no afloja PII). Read-only. #8 (ultimo UX) de la cola. AC36 SPEC-0086 ext7. Codigo en Zeus; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0147-codex-front-ledger-filters.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0147 filtros + paginacion del Ledger #4 (AC36; REQ-9AF54A75)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Filtro por actor (Arquitecto/Codex/Operador) y por tipo de evento en la cabecera del Ledger.
2. La lista se reduce a los coincidentes al seleccionar.
3. Paginacion/carga progresiva (no renderizar 900+ a la vez).

## Cierre
- AC36 verde (test de comportamiento: filtrar reduce la lista; paginacion limita el render; sin filtro pagina por
  defecto). El texto libre sigue REDACTADO (no afloja PII). Carry AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. Tras este queda solo el #9 (carga por archivo). Canal ASCII.
