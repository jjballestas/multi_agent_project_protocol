---
task_id: TASK-0242
title: "[VISION-NOVA][F1.5-harness] Envelope de handoff 7 campos + fix-loop pre-commit (cosecha gentle-ai nivel A)"
type: build
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0083]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0242-visionnova-f1e-envelope-fixloop.md
intake:
  type: infra
  goal: Envelope de handoff 7 campos + fix-loop pre-commit en TASK_PROTOCOL + prompts de cron; habilita la activacion de trailers de F1-C.
  acceptance:
    - Schema del envelope (status/executive_summary/artifacts/next_recommended/risks + task_id + gates) y la regla "texto final nunca tool call" en TASK_PROTOCOL.md y template.
    - Prompts de cron de Codex y Analista actualizados con envelope + fix-loop + emision de trailers Task-Id.
    - Un handoff real conforme al envelope como evidencia (cita commit o mensaje).
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - Area_comun/protocol/TASK_PROTOCOL.md
    - personal/Codex/codex_mailbox_cron.ps1
    - personal/Analista/analista_mailbox_cron.ps1
  out_of_scope:
    - Activar el trailer_start_seq de F1-C/TASK-0240 no es parte de esta tarea (aqui solo se habilita la precondicion).
    - protocol.config.json permanece pineado e intocable.
  risk: medium
  estimate: M
---

# TASK-0242 - [VISION-NOVA][F1.5-harness] Envelope de handoff + fix-loop

Owner: Codex (harness de peers) + Arquitecto (doctrina). Cosecha gentle-ai nivel A.
Parte doctrinal avanza en paralelo; el despliegue de harnesses es PRECONDICION de activar F1-C (TASK-0240).

## Alcance
Schema de envelope (status / executive_summary / artifacts / next_recommended / risks +
task_id + gates) en TASK_PROTOCOL + regla dura "el envelope es TEXTO FINAL del turno, nunca
un tool call"; fix-loop: tras NO-GO del checker, remediacion + RE-JUICIO obligatorio antes
del commit de cierre, tope 2 iteraciones + escalada al operador; opcional workload-guard
N-lineas con size:exception (via exception.recorded kind=scope_change, F1-B).

## DoD (testable)
1. Schema y reglas en TASK_PROTOCOL.md (y template) commiteados.
2. Prompts de cron de Codex y Analista actualizados con envelope + fix-loop + emision de
   trailers (habilita la activacion de F1-C).
3. 1 handoff real conforme al envelope como evidencia (cita commit/mensaje).
4. Los 3 gates verdes en clon limpio.
