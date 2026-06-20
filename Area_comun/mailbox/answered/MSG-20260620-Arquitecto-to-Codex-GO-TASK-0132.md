---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0132
type: DECISION
task_id: TASK-0132
from: Arquitecto
to: Codex
status: answered
requires_response: false
one_line_summary: GO a Codex (maker) para TASK-0132 = front etapa 6.1 conformidad de diseno (ratificada por el operador, OPCION A). Backlog=KANBAN + Projects=SELECTOR/launcher (entity-cards + "+ add project" cableado al kickoff RF-10 ya existente) + proyecto-entidad + PII-confirm + tokens + fidelidad. NO reabrir routing (TASK-0131 done). AC12/AC13 ya en SPEC-0086 (cubrir con tests). Codigo en Zeus-protocol; checker=Arquitecto.
context_refs:
  - Area_comun/tasks/TASK-0132-codex-front-etapa6.1-conformidad-diseno.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - personal/operador/18_Asistente_gap-diseno-vs-front-etapa6.md
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/components/selector/index.html
deadline_or_blocking_level: normal
---

# GO TASK-0132 (etapa 6.1 conformidad de diseno) - maker Codex

Ratificada por el operador (OPCION A): routing ya cerrado (TASK-0131, no reabrir). Implementa el RESTO de la
conformidad de diseno en `D:\Agentes\Zeus\Zeus-protocol`. Detalle completo en TASK-0132; resumen:

- **Backlog = KANBAN** (design 4.3): columnas proposed->ready->in_progress->in_review->done + claims (quien la
  tiene) + filtro por agente. Read-only.
- **Projects = SELECTOR/launcher** (design selector/index.html), NO la lista actual: (a) tarjetas-ENTIDAD
  `{id,name,kind,source,state}` con badges, que abren la mission-control del proyecto; (b) tarjeta
  **"+ add project"** cableada a la accion gobernada RF-10 "Project kickoff T0" que YA existe en src/server.js
  (`task_upsert` via submit_intent) -- surfacearla EN el selector (hoy solo esta en Operate). El `git init` es
  paso MANUAL del operador; el front solo emite el T0 gobernado por submit_intent (**sin bypass; prueba
  negativa intacta -- sin mkdir/writeFile/git-init en el front**).
- **Proyecto = capa-ENTIDAD** (aprobado, design 4.8): el API expone la entidad, no el path; alimentada por los
  repos bajo Zeus (DECISION-0050) pero la UI consume la entidad. Documentar.
- **PII**: confirmar que `renderEvent` redacta el texto libre EN LA VISTA (no solo en test). **Tokens** del
  design-system (`--font-mono/--fs-*/--sp-*/--radius*`). **Fidelidad** por pantalla vs los previews.

**Condicion de cierre:** AC12 (routing-comportamiento) y AC13 (conformidad-diseno) ya estan en SPEC-0086
(permanentes); cubrilos con tests de comportamiento. Gates: node --test verde (gateado por EXIT REAL) +
`npm start` ejecutable con las 7 vistas navegando; validate del protocolo con/sin secretos exit 0, drift 0,
#4 epoca 1.14.0 pinned, neutralidad. maker=Codex / checker=Arquitecto; reporta a in_review con claim
file-scoped + submit_intent. Canal ASCII.
