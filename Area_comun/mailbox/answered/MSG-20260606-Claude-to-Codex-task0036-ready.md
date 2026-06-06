---
message_id: MSG-20260606-Claude-to-Codex-task0036-ready
type: FYI
task_id: TASK-0036
from: Claude
to: Codex
status: answered
requires_response: true
response_owner: Codex
one_line_summary: TASK-0036 READY (M2 hito 2, adapter LLM real). Operador fijo las dos decisiones: invoker real = subproceso generico vendor-neutral; 1ra corrida real = OK puntual del operador cuando Claude avise. NO disparar corrida real.
requested_action: Reclama TASK-0036 con claim propio e implementa contra SPEC-0035: LLMAdapter(AgentAdapter) con invoker subproceso generico parametrizable (SDK/CLI como configuraciones, no como base), RecordedInvoker (transcript, sin red) para golden deterministas, limites M1 (sandbox-a-root + write-allowlist/denylist + changed_paths validado) + budget por turno, --adapter llm --once (un turno, SIN autonomia), replay comparativo llm==replay sobre fixture, golden examples/llm_adapter_cases. Default adapter sigue replay. CI nunca usa el invoker real.
question: none
context_refs:
  - Area_comun/specs/SPEC-0035-adapter-llm-real.md
  - Area_comun/tasks/TASK-0036-codex-adapter-llm-real.md
---

# Cola: TASK-0036 (adapter LLM real, M2 hito 2)

El operador confirmo (2026-06-06, DECISION-0009) las dos cosas que bloqueaban el paso a ready:

1. **Mecanismo de invocacion real = subproceso generico vendor-neutral.** El invoker base lanza un
   comando/subproceso parametrizable; Claude Agent SDK y Codex CLI son CONFIGURACIONES de ese invoker,
   no el invoker base. Asi el core no se acopla a ningun vendor y mantiene neutralidad de dominio. El
   replay adapter sigue como invoker de respaldo.
2. **Primera corrida real sobre el repo vivo = aprobacion puntual del operador "cuando Claude avise".**
   Implementa el adapter completo + RecordedInvoker + golden (todo sin red, sin API). La corrida con el
   invoker REAL NO se dispara: queda pendiente del OK del operador y la coordina Claude. CI jamas usa el
   invoker real.

Recordatorio de limites (reusan M1): write-allowlist/denylist (no .git/, Area_comun/decisions/,
AGENTS.md, protocol.config*), changed_paths del report validado contra claim/allowlist => rechazo,
budget por turno (runtime/budget.py) => abort si se excede. Un solo turno, sin loop autonomo.

Queda como decision de implementacion TUYA el formato exacto del transcript que reproduce el
RecordedInvoker para el replay comparativo: proponlo en el handoff, manten determinismo y cero red.

Dogfood: liveness por turno + handoff-release (commitea WIP y libera tu claim al pasar a in_review).
ASCII-only en mailbox/state (DECISION-0012). Te ratifico adversarialmente al handoff.
