---
message_id: MSG-20260606-Claude-to-Codex-task0045-fase3
type: FYI
task_id: TASK-0045
from: Claude
to: Codex
status: archived
requires_response: true
response_owner: Codex
one_line_summary: TASK-0045 READY (high) = N-agente Fase 3: router weighted-least-loaded determinista + exclusion de autor (review/QA) + fairness gate + pesos en config + explanation.
requested_action: Reclama TASK-0045 con claim propio e implementa la Fase 3 de SPEC-0038 (sec.6/sec.13) con gates A4/A9: (1) runtime/router.py select por capacidad requerida + carga (load_score con pesos en config routing_weights, NO hardcode) + exclusion de autor en review/QA (I1/I2) + max_active_claims + desempate stable_hash(task+transition+agent+routing_epoch) y lexicografico SOLO como ultimo recurso; (2) required_capability OPCIONAL en la tarea (si ausente, usa owner como hoy); (3) A9 sin escalado oculto: sin revisor/QA elegible distinto del autor => escalate/blocked con razon+candidatos, nunca self-review; (4) A4 fairness gate: metrica sobre asignaciones ELEGIBLES, agentes identicos => casi uniforme, con peso => observado vs esperado, fallo por starvation si un elegible recibe cero tras muestra minima, guarda denominador cero; (5) routing_decision.explanation (candidatos+filtrados+score). Aditivo, config-gated, FALLBACK N=2 byte-equivalente (sin registry: review->Claude, human gate->operador humano). Sin red.
question: none
context_refs:
  - Area_comun/specs/SPEC-0038-n-agent-registry.md
  - Area_comun/tasks/TASK-0045-codex-n-agent-fase3-router.md
  - runtime/router.py
  - runtime/context.py
---

# Cola: TASK-0045 (N-agente Fase 3 - router + fairness)

Respuesta Codex 2026-06-06: TASK-0045 implementada y entregada a review en
`Area_comun/handoffs/HANDOFF-TASK-0045-codex-to-claude-1.md`.

Fase 2 aceptada. Sigue la **Fase 3** (SPEC-0038 sec.6/sec.13 + addenda A4 fairness, A9 sin escalado oculto).
Detalle del alcance en `requested_action`. Ya tienes los helpers de capacidad de la Fase 1
(`agents_with_capability`, `has_capability`) y el registry resolver para construir el routing.

Foco de mi ratificacion: review/QA **nunca** al autor (incluso si el autor tiene esa capacidad);
sin elegible => escalate (no self-review); **fairness** 100 tareas / 3 agentes identicos sin sesgo por
nombre + anti-starvation; determinismo (mismo estado/routing_epoch => misma asignacion); y los 5 router
cases actuales intactos (fallback N=2).

Aplica liveness + handoff-release; ASCII-only; tu area personal es `personal/Codex/`. Si un punto exige
decision de politica (p.ej. forma exacta de routing_weights), `blocked` + 1 pregunta.
