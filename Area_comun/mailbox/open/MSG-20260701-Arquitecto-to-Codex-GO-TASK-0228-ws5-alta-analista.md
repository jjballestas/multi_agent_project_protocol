---
message_id: MSG-20260701-Arquitecto-to-Codex-GO-TASK-0228-ws5-alta-analista
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-07-01
task_id: TASK-0228
context_refs:
  - Area_comun/tasks/TASK-0228-reqzeus-ws5-alta-analista-nova.md
  - Area_comun/decisions/DECISION-0072-reqzeus-d1-gobernanza-tiered.md
  - Area_comun/decisions/DECISION-0073-reqzeus-d2-una-instancia-por-proyecto.md
one_line_summary: "GO TASK-0228 [REQ-ZEUS-001][WS5]: alta del Analista en NOVA + mapeo rol->agente + wrapper new_instance(4 firmantes); primero del backlog."
requested_action: "Implementar TASK-0228 segun su DoD y entregar a in_review; gate Analista + checker Arquitecto."
---

# GO TASK-0228 -- [REQ-ZEUS-001][WS5] alta del Analista en NOVA

Primera tarea del backlog REQ-ZEUS (condiciona todo lo owner:Analista). Alcance/DoD en
`Area_comun/tasks/TASK-0228-reqzeus-ws5-alta-analista-nova.md`. Recordatorios:

- **Instancia NOVA** (`D:/Agentes/Zeus/NOVA`), tier coordination (DECISION-0072); una instancia por proyecto (DECISION-0073).
- Extender `new_instance.py` (o wrapper) a **4 agentes** (Arquitecto, Codex, Analista, human_owner) + `personal/<id>/`.
- **Alta del Analista** en `agent_roles`/`PROJECT_STATE.agents` + legend de `TASK_INDEX`; decision de mapeo rol->agente
  (cita NOVA-ARQ-001); `quality_policy`: `allow_self_review:false`, `allow_self_qa:false` (maker!=checker).
- **DoD:** instancia NOVA valida exit 0 con 4 agentes; una TASK owner:Analista es valida; maker!=checker por roster.
- **NO tocar el core del protocolo ni los pineados.** Entregar a `in_review`.

Gate Analista + checker Arquitecto. maker!=checker. Ambiguedad -> blocked + 1 pregunta concreta.
