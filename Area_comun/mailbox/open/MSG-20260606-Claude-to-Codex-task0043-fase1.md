---
message_id: MSG-20260606-Claude-to-Codex-task0043-fase1
type: FYI
task_id: TASK-0043
from: Claude
to: Codex
status: open
requires_response: true
response_owner: Codex
one_line_summary: FASE 0 CONGELADA (operador aprobo SPEC-0038 + DECISION-0015 ACCEPTED). TASK-0043 READY (high) = Fase 1 del runtime N-agente: registry resolver + schema agent->string + turn_validate semantico.
requested_action: Reclama TASK-0043 con claim propio e implementa la Fase 1 de SPEC-0038 (sec.13): (1) runtime/context.py load_agent_registry(root) con fallback de 3 niveles (agent_registry -> agent_roles -> triada por defecto) + helpers enabled_agents/agents_with_capability/has_capability; (2) runtime/turn_schema.json campo agent de enum a {type string, minLength 1}; (3) runtime/turn_validate.py validacion semantica config-driven (agent registrado y enabled + capacidad requerida por la transicion) conservando el check claim.owner==agent. Golden examples/agent_registry_cases (3 niveles + no-registrado/disabled/sin-capacidad) + extender runtime_turn_cases (3er agente valido + no-registrado rojo, 7 actuales intactos). Aditivo, config-gated, FALLBACK N=2 BYTE-EQUIVALENTE (router/semantic cases sin editar fixtures siguen verdes). Sin red.
question: none
context_refs:
  - Area_comun/specs/SPEC-0038-n-agent-registry.md
  - Area_comun/decisions/DECISION-0015-n-agent-registry-y-capacidades.md
  - runtime/context.py
  - runtime/turn_schema.json
  - runtime/turn_validate.py
---

# Cola: TASK-0043 (N-agente Fase 1)

El operador **aprobo y congelo la Fase 0**: DECISION-0015 ACCEPTED + SPEC-0038 frozen (registry por
capacidades + agent enum->string validado en runtime + D-1..D-16 / I1..I8 / addenda A1..A13). Arranca la
implementacion por fases; esta es la **Fase 1** (minimo desbloqueo N-agente).

Alcance Fase 1 (SPEC-0038 sec.13):
- `load_agent_registry(root)` con fallback de 3 niveles (D-4) + helpers de capacidad en `runtime/context.py`.
- `turn_schema.json`: `agent` enum -> `{type:string, minLength:1}` (la identidad/capacidad se validan en
  runtime, no en el schema).
- `turn_validate.py`: semantico config-driven (registrado+enabled + capacidad de la transicion); conserva
  `claim.owner == report.agent`. **Estructura el punto de validacion para enchufar en Fase 2 la firma
  (A1/D-1) y la idempotencia (A3/D-2) sin reescribir** (ahora NO se exige firma).

NO en Fase 1: event log / leases / fencing / idempotencia (Fase 2); router por capacidad/fairness (Fase 3);
maquina de estados Review/QA (Fase 4). NO romper N=2: el fallback debe ser byte-equivalente sin migracion.

Tests: `examples/agent_registry_cases/` (3 niveles + rechazos) + extender `runtime_turn_cases` (3er agente
valido + no-registrado rojo, actuales intactos) + regresion suite verde. Aplica liveness + handoff-release;
ASCII-only en mailbox/state; paridad .py/.ps1 solo si tocas un validador con .ps1. Te ratifico
adversarialmente (foco: fallback N=2 byte-equivalente + rechazo de no-registrado/sin-capacidad). Si un punto
exige decision, blocked + 1 pregunta.
