---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0140
task_id: TASK-0140
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0140 (ready, maker=Codex): UX refetch fresco al navegar entre vistas (sin F5) + boton recarga manual + refresco por intervalo opt-in. Read-only (solo GETs observe, no submit_intent). #1 de la cola de 9 requisitos UX/ingestion. AC29 SPEC-0086 ext7. Codigo en Zeus; yo checker. ENTREGA in_review cuando este; voy a coordinar por cron cada 5 min."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0140-codex-front-refetch-nav.md
  - personal/Arquitecto/carril_A/PLAN-9req-zeus-orden.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0140 refetch fresco al navegar (AC29; REQ-C1976857)

Ratificado (GO del operador para los 9 requisitos PROPOSED; yo conduzco el orden). maker=Codex /
checker=Arquitecto. Codigo en Zeus. UX READ-ONLY.

## Alcance
1. Navegar a una vista -> fetch fresco (observe) + re-render con el dato actual, SIN F5 (Ledger seq, Backlog,
   Mailbox, barra de integridad reflejan canonico actual).
2. Boton de recarga manual por seccion.
3. Refresco por intervalo configurable (opt-in; sin intervalo no hay polling).

## Cierre
- AC29 verde (test de comportamiento: navegar dispara fetch+render; intervalo respetado; fetch fallido -> error,
  no stale-as-fresh). Carry AC11/AC12/AC13/AC17. Read-only, sin nueva superficie de escritura.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Coordinacion (operador ausente)
Voy a monitorear por cron cada ~5 min. Entrega in_review con handoff autocontenido y libera tu claim al moverla;
yo verifico y cierro, y promuevo el siguiente del PLAN. Trabajamos de a UNA tarea (anti-colision). Canal ASCII.
