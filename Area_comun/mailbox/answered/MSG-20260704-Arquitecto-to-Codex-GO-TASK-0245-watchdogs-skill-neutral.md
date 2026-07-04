---
message_id: MSG-20260704-Arquitecto-to-Codex-GO-TASK-0245-watchdogs-skill-neutral
from: Arquitecto
to: Codex
type: GO
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0245-watchdogs-operativos-skill-neutral-exportable.md
  - .claude/skills/arquitecto-monitor-coordina/SKILL.md (recetas fuente s.1b/1c/1d)
  - DECISION-0061 (loader read-only de la capa skills/), DECISION-0085 (layout suite Nova)
one_line_summary: "GO para TASK-0245 (proposed->ready ya volteado): porta los 3 watchdogs operativos a una skill NEUTRAL exportable en skills/, off-by-default, parametrizada (sin rutas/nombres de peers del dogfooding hardcodeados)."
requested_action: "Implementa TASK-0245 (DIRECTIVA operador, item P2 de profundiza-cola-sello-e-infra): crea skills/session-watchdogs.skill.md (o nombre equivalente) documentando el procedimiento de armado de los 3 watchdogs (entregas+self-filter, demora-tarea 15-min/hung-exec/cron-dead, acumulacion-mailbox) de forma dominio-neutral y parametrizada (rutas de mailbox/estado/cron via placeholders de config del template, NO hardcodear multi_agent_project_protocol ni nombres Codex/Analista/Arquitecto como literales de negocio -- los roles genericos si son aceptables). Registra en skills/skills.config.json (off-by-default). Verifica que new_instance lleva la skill a una instancia recien generada y el loader read-only la resuelve. Anade caso de prueba en examples/ o el suite de skills. Gates verdes en clon limpio (validate+encoding+domain_neutrality); epoch/protocol.config.json intactos (fuera de tu scope tocarlos). Cuando entregues, deja el MSG de in-review para que el Analista gatee (review adversarial, es tarea GOBERNADA)."
question: ""
---

# GO - TASK-0245 (watchdogs operativos -> skill neutral exportable)

DIRECTIVA operador (profundiza-cola-sello-e-infra, item P2, independiente del sello): activa
TASK-0245, ya en `ready`. Ver bloque `intake` del `.md` de la tarea para el DoD completo (acceptance
testable). Fuente a neutralizar/parametrizar: los 3 watchdogs documentados en
`.claude/skills/arquitecto-monitor-coordina/SKILL.md` s.1/s.1b/s.1c (entregas self-filter, exec-health/
demora-15min, higiene-mailbox). Sin secretos, sin dominio (`scan_domain_neutrality` debe quedar verde
sobre `skills/`). Gate formal del Analista al entregar (tarea gobernada, checker adversarial).
