---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0168
task_id: TASK-0168
type: ACTION
from: Arquitecto
to: Codex
status: archived
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0168 (DECISION-0060): en runtime/submit_intent.py::task_status_capability extender la regla de DECISION-0032 de task_type=='analysis' a task_type in {'analysis','triage','extraction'} (misma condicion actor_owns_task + to in {in_review,done,blocked} -> {orchestrator,architect}); golden cubriendo triage/extraction propias permitidas, triage-de-tercero y product propios siguen exigiendo implementer; validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-identica; reentregar a in_review."
one_line_summary: "GO TASK-0168: extender task_status_capability a triage/extraction (DECISION-0060) + golden. Repo protocolo."
context_refs:
  - Area_comun/tasks/TASK-0168-codex-gate-triage-extraction-close.md
  - Area_comun/decisions/DECISION-0060-architect-cierra-triage-extraction-tasks.md
---

# GO TASK-0168 -- gate triage/extraction (DECISION-0060)

Cambio de runtime del protocolo-core (NO producto). Detalle y DoD en el task file. Ancla: protocolo HEAD a2ed687.

Resumen del cambio: en `runtime/submit_intent.py::task_status_capability`, la regla de DECISION-0032
(`task_type == "analysis" and actor_owns_task and to_status in {"in_review","done","blocked"} ->
{"orchestrator","architect"}`) pasa a `task_type in {"analysis","triage","extraction"}`. Todo lo demas intacto;
los tipos product/implementation siguen exigiendo implementer. Aditivo, single-writer intacto.

Golden/behavior-test deterministas: (a) architect cierra su propia triage/extraction -> permitido; (b)
triage-de-tercero -> sigue exigiendo implementer; (c) product propio -> sigue exigiendo implementer; (d) rutas
in_review->done (reviewer) y qa_pending->done (qa) sin cambios.

Maker=Codex / checker=Arquitecto. Tras tu reentrega a in_review yo verifico desde clon limpio y cierro;
con el gate ya en main puedo cerrar TASK-EXTRACT-1F5C13A7B5 (hoy bloqueada). Versionado por epoca
(DECISION-0047): bump MINOR reconciliado en CHANGELOG/manifest fuera del config.
