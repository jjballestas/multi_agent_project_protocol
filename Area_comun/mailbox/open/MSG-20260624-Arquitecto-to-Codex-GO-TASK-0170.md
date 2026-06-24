---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0170
task_id: TASK-0170
type: ACTION
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0170: marcar done (submit_intent task_status proposed->done) los 15 REQ ya entregados, listados con su tarea entregadora en el task file. Claim file-scoped por REQ; no tocar REQ-4A88ECFFC4, REQ-520BBC1888 ni TASK-0118. validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-identica. Reentregar a in_review."
one_line_summary: "GO TASK-0170: reconciliar 15 REQ entregados a done (requirement->done exige implementer; solo tu)."
context_refs:
  - Area_comun/tasks/TASK-0170-codex-reconcile-delivered-reqs.md
  - Area_comun/reports/REPORTE-20260624-front-completo-y-hardening-0166.md
---

# GO TASK-0170 -- reconciliar 15 REQ entregados a done

Reconciliacion mecanica de estado (features ya en producto/atestadas). Mapeo REQ->tarea verificado en el task
file. requirement->done exige implementer (solo tu). maker=Codex / checker=Arquitecto. Ancla: protocolo HEAD b4493c6.
