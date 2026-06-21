---
message_id: MSG-20260622-Arquitecto-to-Operador-CLOSE-REQ-643B160A
task_id: TASK-0149
type: FYI
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "CERRADO el defecto del Intake REQ-643B160A (fantasma) -> done via TASK-0149 (AC39). El EXECUTE ahora rechaza server-side narrativa/aceptacion vacias o == placeholder (sin preview-as-green) y exige proyecto destino EXPLICITO (no default a Zeus-protocol); el TASK_INDEX no crece en los rechazos (no se crea fantasma). Zeus 03991cd; npm 41/41 EN CLON LIMPIO; validate con/sin secretos exit 0; #4 byte-identica; drift 0. Cola VACIA."
context_refs:
  - Area_comun/tasks/TASK-0149-codex-intake-no-phantom.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
deadline_or_blocking_level: normal
---

# CIERRE REQ-643B160A - Intake honesto (no fantasmas + proyecto explicito)

Cerrado a `done` (checker=Arquitecto **DESDE CLON LIMPIO**, maker=Codex). AC39 verde behavior-tested:
- **narrativa o aceptacion VACIAS** -> 400 "narrative is required" (no se crea REQ, no verde).
- **texto == PLACEHOLDER** conocido -> 400 "placeholder text" (incluso en dry_run; no preview-as-green).
- **proyecto vacio/no elegido** -> 400 "explicit project" (NO defaultea a Zeus-protocol).
- los rechazos NO incrementan `TASK_INDEX.tasks` -> no se persiste fantasma.
Validacion **server-side** (no solo cliente); remedia el fantasma REQ-984A85C6 (cancelado).

Gates: Zeus `npm test` 41/41 en CLON LIMPIO determinista; validate con/sin secretos exit 0; #4 epoca 1.14.0
byte-identica; drift 0. Tightening del execute ya gobernado -- no abrio superficie de escritura.

## Estado
Cola de trabajo VACIA. Zeus-protocol acumula commits LOCALES (TASK-0140..0149) -> el push de Zeus al remote
sigue gateado a tu accion. Codex sigue activo (lo reactivaste); si quieres lo mando a stand-down, dime. Canal ASCII.
