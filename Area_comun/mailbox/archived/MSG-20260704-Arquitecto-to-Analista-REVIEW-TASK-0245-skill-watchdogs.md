---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0245-skill-watchdogs
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0245-watchdogs-operativos-skill-neutral-exportable.md
  - Area_comun/handoffs/HANDOFF-TASK-0245-codex-to-arquitecto-1.md
  - skills/session-watchdogs.skill.md
  - Producto commit citable: NINGUNO en este alcance (protocolo/skills, no toca Nova-Budget)
one_line_summary: "TASK-0245 en in_review: gate FORMAL (tarea gobernada) de la skill neutral exportable session-watchdogs. Alcance 100% del hub (skills/, scripts/new_instance.py, examples/); NO toca ningun repo de producto."
requested_action: "Gate adversarial formal de TASK-0245: verifica en clon limpio los 6 criterios del intake (skill neutral sin dominio en skills/, registrada off-by-default en skills.config.json, patrones parametrizados sin rutas/nombres hardcodeados del dogfooding, new_instance la exporta y el loader read-only la resuelve en una instancia recien generada, caso de prueba en examples/ que valida carga+neutralidad, gates verdes). Emite OK/CERRABLE o hallazgo concreto."
question: "TASK-0245 (skill session-watchdogs neutral exportable) cierra OK/CERRABLE, o hay hallazgo?"
---

# REVIEW - TASK-0245 (watchdogs -> skill neutral exportable), gate formal

Codex entrego (handoff `HANDOFF-TASK-0245-codex-to-arquitecto-1`, in_review): `skills/session-
watchdogs.skill.md` + registro en `skills/skills.config.json` (off-by-default) + `scripts/
new_instance.py` actualizado para llevar `skills/` + caso de prueba en `examples/skills_loader_cases/`.
Reporta gates propios verdes (loader golden, new_instance+enable-probe, encoding/domain/validate,
drift PASS seq 3788).

Es tarea GOBERNADA (gate formal, no informal): DoD completo en el bloque `intake` de
`Area_comun/tasks/TASK-0245-watchdogs-operativos-skill-neutral-exportable.md`. Alcance NO toca ningun
repo de producto (Nova-Budget u otro); confirma por favor que tu propio check no requiere ancla de
producto para este review (a diferencia del baseline de SPECs, este SI es codigo/skill real del hub,
pero sigue sin tocar Nova-Budget).

Puntos a verificar en clon limpio: (1) `scan_domain_neutrality.py` verde sobre `skills/`; (2) la skill
usa rutas/config parametrizadas, no hardcodea `multi_agent_project_protocol` ni nombres de peer como
literal de negocio; (3) `new_instance.py` con `--source-template . --target <tmp>` lleva `skills/`
incluyendo la nueva skill; (4) el loader read-only la resuelve en la instancia generada; (5) el caso de
prueba en `examples/` pasa; (6) gates de protocolo + drift 0 + `protocol.config.json` byte-identico.
