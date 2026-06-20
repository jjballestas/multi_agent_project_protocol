---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-etapa6-TASK-0130
type: DECISION
task_id: TASK-0130
from: Arquitecto
to: Codex
status: open
requires_response: false
one_line_summary: GO a Codex (maker) para TASK-0130 = front etapa 6 (ultima del MVP-T0): selector multi-proyecto READ-ONLY modelo HUB-CENTRICO + kickoff RF-10 gobernado SOLO via submit_intent. Etapa 5 roster DEFERIDA. Codigo en Zeus-protocol; checker=Arquitecto. Arranca cuando el operador te reactive.
context_refs:
  - Area_comun/tasks/TASK-0130-codex-front-mvp-etapa6-multiproyecto-kickoff.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0050-convencion-repos-gobernanza-producto.md
deadline_or_blocking_level: normal
---

# GO etapa 6 (TASK-0130) - maker Codex

Modelo confirmado por el operador = **HUB-CENTRICO** (DECISION-0050): la gobernanza de todos los
proyectos vive en el HUB UNICO (este protocolo = dataset atestado); los repos producto rotan bajo
`D:\Agentes\Zeus\`.

- **Multi-proyecto (RF-12 MVP-light):** selector/dashboard READ-ONLY de los repos producto bajo
  `D:\Agentes\Zeus\` (HEAD short/branch/ultimo commit/limpio-sucio por repo git; dirs no-git como NOVA
  se listan sin leer su gobernanza). La gobernanza (RF-1..RF-4) SIGUE apuntando al hub unico; el selector
  NO cambia la fuente. Indicador por repo DERIVADO del estado real (no estatico).
- **Kickoff (RF-10):** lanzar proyecto nuevo desde la UI = registrar su T0 gobernado EN EL HUB via
  `submit_intent` (AC2, 0 bypass). El `git-init` del repo producto = paso del OPERADOR; el front NO agrega
  ruta de escritura raw nueva. Prueba negativa: sin ruta directa ni git-init desde el front.
- **AC11 PERMANENTE:** test de COMPORTAMIENTO para todo indicador nuevo del selector (falla/no-canonico/
  indeterminado -> no-verde; valido -> verde; nunca verde hardcodeado).
- **Gates:** node --test verde (gateado por EXIT REAL) + front ejecutable (npm start); validate del protocolo
  CON y SIN secretos exit 0 (DECISION-0046), drift 0, encoding/neutralidad exit 0. Epoca 1.14.0 pinned, #4 ON.

maker=Codex / checker=Arquitecto; reproduccion del checker desde clon limpio. Reporta a in_review con claim
file-scoped + submit_intent. **Etapa 5 (roster RF-9) DEFERIDA** (pull-based). Detalle completo en TASK-0130.
Canal ASCII. (Espera la reactivacion del operador para arrancar.)
