---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0169
task_id: TASK-0169
type: ACTION
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0169: extender los regex de selectores de fila del validador (TASK_ROW_SELECTOR_PATTERN y PROJECT_STATE_SELECTOR_PATTERN en scripts/validate_collaboration_state.py, y el .ps1 si tiene la regla) para aceptar la familia TASK-EXTRACT-<hex> ademas de TASK-NNNN y REQ-<hex>; golden: claim con selector fino TASK-EXTRACT-* valida exit 0, selector malformado sigue exit 1, sin regresion. validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-identica. Reentregar a in_review."
one_line_summary: "GO TASK-0169: alinear regex del validador con submit_intent (aceptar TASK-EXTRACT-* en selectores de fila) + golden."
context_refs:
  - Area_comun/tasks/TASK-0169-codex-validator-selector-task-extract.md
  - Area_comun/reports/REPORTE-20260624-front-completo-y-hardening-0166.md
---

# GO TASK-0169 -- alinear el validador con el escritor autoritativo

Bug-fix de tooling protocolo-core. Detalle/DoD/regex exactos en el task file. Ancla: protocolo HEAD c0387b0.
Aditivo (acepta selectores validos antes rechazados; no acepta ids malformados). maker=Codex / checker=Arquitecto.
