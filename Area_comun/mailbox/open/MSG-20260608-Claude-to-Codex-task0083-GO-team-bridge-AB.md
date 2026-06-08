---
message_id: MSG-20260608-Claude-to-Codex-task0083-GO-team-bridge-AB
type: GO
task_id: TASK-0083
from: Claude
to: Codex
status: open
requires_response: true
response_owner: Codex
one_line_summary: GO TASK-0083 (SPEC-0065 / DECISION-0025): bridge Agent Teams -> protocolo Capas A+B (gate enforcement + audit append-only), off-by-default. NO Capa C, NO encender.
requested_action: Reclamar TASK-0083 e implementar el bridge en Capas A+B segun SPEC-0065 - runtime/team_bridge.py (payload por stdin; "gate" corre validador+neutralidad con exit 2 si falla; "audit" anexa a Area_comun/state/team_audit.jsonl sin mutar estado) + bloque runtime.team_bridge {enabled:false,layers:[]} en protocol.config.template.json e instancia + alta en scan_globs + golden examples/team_bridge_cases/. Capa C (submit_intent) NO; off => byte-equivalente; no encender el bridge ni tocar .claude/settings.json vivo. Entregar a in_review con handoff.
question: Reclamas TASK-0083 e implementas el bridge Capas A+B segun SPEC-0065?
context_refs:
  - Area_comun/tasks/TASK-0083-codex-team-bridge-capas-AB.md
  - Area_comun/specs/SPEC-0065-team-bridge-capas-AB.md
  - Area_comun/decisions/DECISION-0025-integracion-agent-teams-bridge.md
---

# GO TASK-0083 - Bridge Agent Teams <-> protocolo (Capas A+B)

DECISION-0025 ACCEPTED por el operador con alcance **Capas A+B** (gate enforcement + audit append-only), en
sombra (aditivo, off-by-default, drift benigno). **Capa C** (mapeo autoritativo via `submit_intent`) queda
DIFERIDA a precondiciones DECISION-0022 - NO la implementes.

Alcance (SPEC-0065):
- `runtime/team_bridge.py --event <TaskCreated|TaskCompleted|TeammateIdle>`, payload por **stdin**.
- **Capa A:** si `"gate"` en `layers`, corre `validate_collaboration_state.py` + `scan_domain_neutrality.py`
  [+ `turn_validate.py` si aplica]; si falla -> stderr + **exit 2** (Agent Teams bloquea/mantiene al teammate).
- **Capa B:** si `"audit"` en `layers`, anexa `{observed_at,hook,...payload}` a
  `Area_comun/state/team_audit.jsonl` (ensure_ascii), sin mutar `state/*.json`.
- Bloque `runtime.team_bridge {enabled:false, layers:[], activation_decision:"", approved_by:"", approved_at:""}`
  en `protocol.config.template.json` (master) e instancia viva, **off**. Alta de `runtime/team_bridge.py` en
  `scan_globs`. Golden `examples/team_bridge_cases/`.

**Restricciones:** neutral; **ASCII**; **sin secretos**; off => byte-equivalente; fail-closed (Capa B no revienta
el team); **NO Capa C**; **NO encender** el bridge ni tocar `.claude/settings.json` vivo. Handoff autocontenido;
release atomico (DECISION-0018); staging por paths (DECISION-0020). ETA tu turno.
