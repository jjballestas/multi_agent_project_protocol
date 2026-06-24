---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0174
task_id: TASK-0174
type: ACTION
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0174: quitar del modal de Intake el indicador de pasos (div.steps con span.step '1 Capturar/2 Preview/3 Confirmar/4 Resultado', ~1585-1589) + la logica/CSS huerfana (setIntakeStep/.steps/.step). El flujo gobernado RF-14 y sus botones/estados NO cambian. Actualizar/retirar el behavior-test de avance de pasos por uno que afirme que el indicador ya no se renderiza. node --test clon limpio exit 0; #4 byte-identica; sin nueva ruta de escritura. Reentregar a in_review."
one_line_summary: "GO TASK-0174: quitar el indicador de pasos del modal de Intake (decision del operador)."
context_refs:
  - Area_comun/tasks/TASK-0174-codex-front-remove-intake-steps.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# GO TASK-0174 -- quitar el indicador de pasos del modal de Intake

El operador, en prueba, decidio quitarlo (lucia como tabs clickeables pero es pasivo). Solo presentacion; el flujo
RF-14 gobernado no cambia. Detalle/DoD en el task file. Ancla: protocolo HEAD 53f0319. maker=Codex/checker=Arquitecto.
