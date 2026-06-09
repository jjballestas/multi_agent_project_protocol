---
id: TASK-0095
owner: Codex
status: proposed
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: []
relates_to: [TASK-0091, TASK-0093, DECISION-0022]
phase: P2
spec_id: none
linked_decisions: [DECISION-0022]
objective: (OFF-PILOT, follow-up del re-pilot SA.4) Hacer que el commit de turno del orquestador sea SELF-CONSISTENTE cuando una transicion muta el frontmatter del task .md. Hoy, en un turno con transicion task_status (p.ej. ready->in_review), submit_intent muta el status del archivo Area_comun/tasks/TASK-XXXX-*.md (apply_task_file_side_effects -> set_task_file_status), pero commit_turn NO incluye ese .md en sus paths -> el .md queda dirty/uncommitted y el snapshot commiteado tiene TASK_INDEX!=task.md (mismatch transitorio). Visto en el re-pilot (TASK-0091.md quedo dirty tras commit 08a441f).
expected_output: El commit de turno (runtime/vcs.py commit_turn via runtime/apply.py) incluye el/los task .md cuyo frontmatter fue mutado por las transiciones del turno (derivar el path del task file de las transiciones task_status/task_upsert, igual que submit_intent.apply_task_file_side_effects). Resultado: tras un turno con transicion, el working tree queda LIMPIO respecto al task .md (TASK_INDEX y task.md coinciden en el commit). Golden determinista que ejercite un turno con transicion y asevere que el task .md quedo committeado (git status limpio para ese path). Regresiones verdes (runtime_loop, real_adapter, intent_flow); validador/neutralidad/encoding verdes; drift 0; paridad .ps1 donde aplique. Sin cambios de semantica del gate ni de claims.
question_to_resolve: Q1 derivar el task-file path de las transiciones (reusar task_file_for / la logica de apply_task_file_side_effects) sin sobre-incluir paths fuera del turno. Q2 confirmar por golden que el .md queda committeado y el working tree limpio para ese path tras el turno.
closure_criterion: commit_turn incluye los task .md mutados por las transiciones del turno -> working tree self-consistente (TASK_INDEX==task.md en el commit); golden determinista verde; regresiones/validador/neutralidad/encoding verdes; drift 0; sin cambios de semantica; handoff con evidencia. OFF-PILOT: SA.4 de-armado, NO re-armar ni piloto.
sdd_required: true
---

# TASK-0095 - Commits de turno self-consistentes (incluir task .md mutado)

> PROPOSED (Claude 2026-06-10, follow-up #1 del re-pilot SA.4). OFF-PILOT. Pequena. SA.4 DE-ARMADO.

## Contexto

En el re-pilot SA.4 (TASK-0091, commit 08a441f) el turno commiteo el README + el ledger, pero
TASK-0091.md (status->in_review por el side-effect de submit_intent) quedo dirty/uncommitted. El commit
de turno debe incluir el task .md mutado para que el snapshot sea self-consistente.

## Alcance

- runtime/apply.py / runtime/vcs.py: derivar de las transiciones del turno (task_status/task_upsert) el
  path del task .md y anadirlo a los paths del commit_turn. Reusar la logica de
  submit_intent.apply_task_file_side_effects / task_file_for.
- Golden determinista + regresiones + drift 0 + paridad .ps1.

## Restricciones

- OFF-PILOT: SA.4 de-armado, NO re-armar ni piloto. enforce+authoritative ON: todo por submit_intent.
  ASCII, sin secretos, determinista. Template intacto. 1 commit/turno con rutas explicitas. NO cambiar
  la semantica del gate ni de claims.
