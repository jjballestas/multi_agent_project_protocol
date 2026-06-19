---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-etapa6
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: GO a front etapa 6 (multi-proyecto + kickoff RF-10) para dejar el front totalmente funcional. De a una pieza, SDD, maker=Codex/checker=Arquitecto. Badge-honesto (test de COMPORTAMIENTO) sigue como AC PERMANENTE. Etapa 5 roster DEFERIDA (sin Disenador). #4 epoca 1.14.0 intacta, sin re-genesis. NOTA: queda encolado; el cron se detiene (fin de sesion del operador) -> recoger al reanudar.
requested_action: "Autorar el SDD de etapa 6: (1) selector/dashboard multi-proyecto sobre D:\\Agentes\\Zeus\\ (read-only del estado de cada proyecto); (2) RF-10 kickoff: lanzar un proyecto nuevo desde la UI (su primer handoff gobernado = T0 del nuevo proyecto, via submit_intent, sin bypass). Codigo en Zeus-protocol; gobernanza en Area_comun. AC: badge-honesto con test de comportamiento; validate con/sin secretos exit 0; drift 0; #4 intacto. Al cerrar, front ejecutable (npm start). Esto queda ENCOLADO: recogerlo al reanudar (cron detenido)."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/mailbox/open/MSG-20260620-Operador-to-Arquitecto-retira-onboard-disenador.md
deadline_or_blocking_level: normal
---

# GO etapa 6 - multi-proyecto + kickoff (RF-10)

Completar el front a totalmente funcional con la **etapa 6**, de a una pieza (SDD; maker=Codex /
checker=Arquitecto; reproduccion desde clon limpio):
- **Multi-proyecto:** selector/dashboard de los proyectos bajo `D:\Agentes\Zeus\` (este front, y futuros),
  read-only sobre el estado de cada uno.
- **Kickoff (RF-10):** lanzar un proyecto nuevo desde la UI -> su primer handoff gobernado = T0 del nuevo
  proyecto, via `submit_intent` (sin bypass de gates/#4).

AC: **badge-honesto con test de COMPORTAMIENTO** (AC permanente), validate con/sin secretos exit 0, drift 0,
#4 intacto. Codigo en Zeus-protocol; gobernanza en Area_comun (dataset). Al cerrar, front ejecutable
(`npm start`).

**Etapa 5 roster: DEFERIDA** (sin agente que agregar; pull-based). **#4 epoca 1.14.0 intacta, SIN
re-genesis.** Esto queda **ENCOLADO**: el operador cierra sesion y el cron se detiene; recoger al reanudar.
Canal ASCII.
