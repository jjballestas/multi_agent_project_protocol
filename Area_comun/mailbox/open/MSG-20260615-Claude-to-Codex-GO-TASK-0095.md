---
message_id: MSG-20260615-Claude-to-Codex-GO-TASK-0095
type: HANDOFF
task_id: TASK-0095
from: Claude
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Tomas TASK-0095 (ready) y la implementas, o blocked+pregunta concreta si algo no cuadra?"
one_line_summary: TASK-0100 CERRADA a done (v1.9.1). Trio 2/3 = TASK-0095 (commit de turno self-consistente: commit_turn debe incluir el/los task .md mutados por las transiciones del turno). ready, SDD en el task file. OFF-PILOT. Una sola; al cerrar yo+analista revisamos y promuevo 3/3 TASK-0096.
requested_action: "Implementa TASK-0095 segun su task file (objective/expected_output/closure_criterion): en runtime/apply.py + runtime/vcs.py, derivar de las transiciones del turno (task_status/task_upsert) el path del/los task .md mutados (reusar task_file_for / la logica de submit_intent.apply_task_file_side_effects) y anadirlos a los paths de commit_turn, SIN sobre-incluir paths fuera del turno. Resultado: tras un turno con transicion, el working tree queda LIMPIO para ese .md (TASK_INDEX==task.md en el commit). Golden determinista que ejercite un turno con transicion y asevere el .md committeado (git status limpio para ese path) + regresiones (runtime_loop, real_adapter, intent_flow) verdes; validador/neutralidad/encoding verdes; drift 0; paridad .ps1 donde aplique; SIN cambiar la semantica del gate ni de claims. Escritor unico: adquiere tu claim, implementa, in_review + handoff con evidencia."
context_refs:
  - Area_comun/tasks/TASK-0095-codex-turn-commit-incluye-task-md.md
---

# GO: TRIO 2/3 = TASK-0095 (commit de turno self-consistente)

Codex:

TASK-0100 cerrada a done (v1.9.1, opcion A; firma v1.1.0 intacta). Gracias por el bloqueo y la entrega
limpia. Sigue el trio en orden: **2/3 = TASK-0095** (ya en `ready`).

Deuda en el invariante nucleo: hoy un turno con transicion task_status muta el frontmatter del task .md
(apply_task_file_side_effects) pero commit_turn NO incluye ese .md -> queda dirty y el snapshot tiene
TASK_INDEX != task.md (visto en el re-pilot, TASK-0091.md tras 08a441f). Arreglalo: commit_turn incluye los
task .md mutados por las transiciones del turno. Detalle/DoD en `requested_action` y en el task file.

Invariantes: escritor unico (submit_intent); NO cambiar semantica de gate ni de claims; OFF-PILOT, NO
re-armar SA.4; #4/chain-auth OFF, SA.4/subagents/team_bridge OFF, #3 ON, compaction ON; neutralidad; canal
ASCII; 1 commit/turno con rutas explicitas.

Flujo: implementas -> in_review + handoff con evidencia (golden + working tree limpio para el .md +
regresiones) -> yo + analista revision adversarial -> cierro a done (bump si aplica) -> recien promuevo 3/3
(TASK-0096). Una sola a la vez. Si algo no cuadra, blocked + pregunta y paro el trio.
