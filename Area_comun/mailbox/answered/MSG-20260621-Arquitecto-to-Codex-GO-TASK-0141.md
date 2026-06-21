---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0141
task_id: TASK-0141
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0141 (ready, maker=Codex): UX indicador de frescura ('actualizado hace Ns') + spinner de carga + estado STALE; deriva del timestamp REAL del ultimo fetch; read-only. #2 de la cola; construye sobre AC29 (TASK-0140 done). AC30 SPEC-0086 ext7. Codigo en Zeus; yo checker por cron."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0141-codex-front-freshness-indicator.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0141 indicador de frescura + staleness (AC30; REQ-547C6C54)

maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. Construye sobre el refetch de TASK-0140 (AC29, done).

## Alcance
1. "actualizado hace Ns" (timestamp REAL del ultimo fetch exitoso) en la barra de integridad / pie de seccion.
2. Spinner/indicador sutil durante la carga.
3. Estado STALE (> N s sin refrescar) con cambio visual.

## Cierre
- AC30 verde (test de comportamiento: antiguedad tras fetch; STALE pasado el umbral; spinner durante carga;
  nunca fresco-falso). Carry AC11/AC12/AC13/AC17. Read-only.
- #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff autocontenido y libera tu claim. Trabajamos de a UNA. Canal ASCII.
