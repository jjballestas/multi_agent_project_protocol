---
task_id: TASK-0258
title: "[DECISION-0103][C3] Bloque obstacles[] en runtime/turn_schema.json (what / root_cause / resolution / recurrence_risk)"
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
file: Area_comun/tasks/TASK-0258-d0103-c3-turn-schema-obstacles.md
intake:
  type: feature
  goal: Anadir a runtime/turn_schema.json el bloque obstacles[] (DECISION-0103 C3, carril runtime), lista de objetos con what, root_cause, resolution y recurrence_risk, para que el reporte de turno capture contra que se peleo el agente y como lo resolvio. Hoy el schema tiene cero campos para obstaculos y additionalProperties false, asi que un emisor que lo anada sin cambiar el schema falla la validacion.
  acceptance:
    - turn_schema.json admite campo opcional obstacles, array de objetos con required [what, root_cause, resolution, recurrence_risk], recurrence_risk con enum [low, medium, high], additionalProperties false en el item.
    - Version del turn schema bumpeada segun su contrato SemVer (TASK-0053); cambio aditivo = minor.
    - Suites del runtime que consumen el schema actualizadas y verdes (runtime_turn_cases y cualquier otra afectada).
    - Casos cubren turno con obstacles poblado (valido), con lista vacia (valido) y con item mal formado (invalido).
    - El MISMO bloque (4 campos + enum) es la forma canonica que el carril sesion replica (TASK-0261/0262); no se inventa una variante.
  verification_cmd:
    - python examples/runtime_turn_cases/run_runtime_turn_cases.py
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - runtime/turn_schema.json
    - examples/runtime_turn_cases/
  out_of_scope:
    - Validacion condicional por friccion - FUERA (es TASK-0259).
    - Carril sesion (mailbox) - FUERA (TASK-0261/0262).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA; esta tanda va por flujo gobernado normal.
  risk: low
  estimate: S
---

# TASK-0258 - [DECISION-0103][C3] obstacles[] en turn_schema

Origen: DECISION-0103 clausula 3, unidad 2 de la tabla. OK del plan recibido
2026-07-19. Orden (enmienda E2 de la 0103): esta unidad arranca SOLO despues de que
TASK-0257 pase su gate propio de revision (no basta con que 0257 este entregada).
