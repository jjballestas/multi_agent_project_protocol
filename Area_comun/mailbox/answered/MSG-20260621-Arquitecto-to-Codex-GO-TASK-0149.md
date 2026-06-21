---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0149
task_id: TASK-0149
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0149 (ready, maker=Codex): Intake honesto (RF-14) - el EXECUTE RECHAZA server-side requerimientos fantasma (narrativa/aceptacion vacias o == placeholder, sin preview-as-green) + exige PROYECTO DESTINO EXPLICITO (no default a Zeus-protocol). Remedia el fantasma REQ-984A85C6. Tightening del execute ya gobernado (no abre superficie). AC39 SPEC-0086 ext9. Codigo en Zeus; yo checker DESDE CLON LIMPIO."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0149-codex-intake-no-phantom.md
  - Area_comun/tasks/req-643b160a-requirement-seed.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0149 Intake honesto (no fantasmas + proyecto explicito) (AC39; REQ-643B160A)

maker=Codex / checker=Arquitecto. Codigo en Zeus. Remedia el defecto del fantasma (REQ-984A85C6 cancelado).

## Alcance
1. **Server-side:** EXECUTE rechaza (sin preview-as-green) si narrativa o intencion de aceptacion estan vacias
   o == placeholder/ejemplo conocido. Validacion en el server, no solo cliente.
2. **Proyecto explicito:** EXECUTE exige proyecto elegido por el operador; NO defaultea a Zeus-protocol; sin
   proyecto -> rechazo.
3. **Front:** error real (no verde) al rechazar; el wizard no avanza con placeholder/vacio.

## Cierre
- AC39 verde (test de comportamiento: vacio/placeholder -> RECHAZADO no-REQ no-verde; sin proyecto -> RECHAZADO;
  contenido real + proyecto explicito -> requirement real id+seq). Carry AC11/AC14/AC22.
- npm test verde **EN CLON LIMPIO** (gate eol=lf; reproducir clonando, no in-place); #4 byte-identica; validate
  con/sin secretos exit 0; drift 0; neutralidad/encoding 0.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. Canal ASCII.
