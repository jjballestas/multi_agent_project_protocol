---
task_id: TASK-0262
title: "[DECISION-0103][C2/C4] Plantillas de mailbox: REPORTE de entrega con bloque obstacles + friction_count, y reporte de ASIGNACION (unidad, agente, por que)"
type: doc
status: done
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0262-d0103-c2c4-plantilla-reporte-asignacion-mailbox.md
intake:
  type: doc
  goal: Redactar las plantillas gobernadas del carril sesion de DECISION-0103, (a) mensaje type REPORTE de entrega con el bloque obstacles (identico en forma al del turn_schema de TASK-0258, 4 campos + enum) y el friction_count de C4; (b) reporte de ASIGNACION de C2 (unidad, agente elegido y POR QUE, usando los datos que ya emite el routing, required_capability, candidatos y racional, sin inventar campos nuevos del runtime). Ambos carriles usan EL MISMO bloque; la plantilla es la referencia canonica para humanos y agentes en sesion.
  acceptance:
    - Plantillas en Area_comun/protocol/ (junto a los docs de mailbox existentes) con frontmatter completo y valido, ASCII puro, y coherentes con las reglas vivas del canal (response_owner cuando aplique).
    - El bloque obstacles de la plantilla es identico en campos y enum al del turn_schema (TASK-0258); cero variantes.
    - La plantilla de asignacion presenta required_capability y el racional de eleccion con los datos existentes del routing_decision; coste marginal ~0 como declara C2.
    - Ejemplo completo incluido de cada mensaje, asignacion, entrega con obstacles poblado y entrega sin friccion (obstacles vacio + friction_count 0).
    - Neutralidad de dominio, sin terminos de negocio en las plantillas.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/protocol/
  out_of_scope:
    - Enforcement en el validador (TASK-0261; esta unidad redacta, no valida).
    - Cambios de runtime - FUERA.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
  risk: low
  estimate: S
---

# TASK-0262 - [DECISION-0103][C2/C4] Plantillas REPORTE + asignacion

Origen: DECISION-0103 clausulas 2 y 4, unidad 6 de la tabla. Coordinar con TASK-0258
(forma del bloque) y TASK-0261 (lo que el validador exigira). Depende del OK del plan.
