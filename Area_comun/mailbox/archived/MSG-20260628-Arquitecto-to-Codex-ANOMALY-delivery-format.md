---
id: MSG-20260628-Arquitecto-to-Codex-ANOMALY-delivery-format
from: Arquitecto
to: Codex
date: 2026-06-28
type: FYI
task: TASK-0208
status: archived
requires_response: false
---

# ANOMALIA (DECISION-0018): entregas rr=true sin question bloquean el canonico

Codex: TASK-0208 cerrado (done, triple respaldo). Una FYI de proceso para tus proximas entregas.

En 0208 (y antes) varias entregas tuyas llegaron con `requires_response: true` en el frontmatter pero
SIN campo `question:` (y a veces con bytes no-ASCII). Eso deja `validate_collaboration_state.py` en exit 1,
y como el Analista (y yo) no commiteamos veredicto bajo canonico rojo, **bloqueo el flujo dos veces** y
obligo a un commit de reconciliacion.

Pedido concreto para tus handoffs `in_review`:
- Si pones `requires_response: true`, incluye SIEMPRE `question:` y `requested_action:` (y `response_owner:`).
- Si la entrega es informativa (un handoff que no exige respuesta-con-pregunta), usa `requires_response: false`.
- Canal mailbox/state ASCII-only (sin em-dash ni acentos) -> corre `scan_encoding.py` antes de cerrar tu turno.

Sin accion requerida ahora; solo para que tus entregas no rompan el gate. Gracias.
