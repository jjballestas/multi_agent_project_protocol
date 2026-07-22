---
task_id: TASK-0259
title: "[DECISION-0103][C3] Validacion condicional en turn_validate: obstacles obligatorio si hubo friccion (gate_green false / attempt>1 / revert)"
type: feature
status: done
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0259-d0103-c3-turn-validate-obstacles-condicional.md
intake:
  type: feature
  goal: Implementar en runtime/turn_validate.py la regla anti-teatro de DECISION-0103 C3 (carril runtime), si el turno tuvo friccion mecanicamente detectable (gate_green false, attempt mayor que 1 / bounce, revert), el bloque obstacles NO puede ir vacio ni ausente; sin friccion, lista vacia es respuesta legitima y no se fuerza prosa.
  acceptance:
    - turn_validate falla con mensaje accionable (que sensor disparo y que falta) si detecta friccion Y obstacles esta vacio o ausente.
    - Sin friccion detectada, obstacles vacio o ausente PASA.
    - Los sensores de friccion quedan documentados en el codigo, que campo del reporte de turno dispara cada uno (gate.green false, attempt_id mayor que 1, revert en transitions/actions segun exista en el schema real).
    - Suite cubre los 3 sensores x (con/sin obstacles) + el caso sin friccion, todos verdes.
    - Si algun sensor no es derivable del reporte actual (p.ej. revert), la unidad lo declara en el handoff y lo implementa sobre el campo real disponible, sin inventar campos fuera de TASK-0258.
  verification_cmd:
    - python examples/runtime_turn_cases/run_runtime_turn_cases.py
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - runtime/turn_validate.py
    - examples/runtime_turn_cases/
  out_of_scope:
    - Cambiar el schema (es TASK-0258, dependencia previa).
    - Carril sesion - FUERA (TASK-0261).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA.
  risk: low
  estimate: S
---

# TASK-0259 - [DECISION-0103][C3] turn_validate condicional por friccion

Origen: DECISION-0103 clausula 3, unidad 3 de la tabla. Depende de TASK-0258 (el campo
debe existir en el schema antes de validarlo condicionalmente) y del OK del plan.
