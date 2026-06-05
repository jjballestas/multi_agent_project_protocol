---
spec_id: SPEC-0009-sdd-templates
task_id: TASK-0009
type: implementation
status: ready
linked_decisions: [DECISION-0004, DECISION-0002, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0009 — Actualizar plantillas del protocolo para SDD

## Contexto
Las plantillas del protocolo aún no contemplan `type` ni los campos SDD. Ver
[DISENO-SDD.md](../artifacts/DISENO-SDD.md) §2.

## Alcance
`TASK_PROTOCOL.md`, `TASK_TEMPLATE.md`, `HANDOFF_TEMPLATE.md`, `HUMAN_REPORT_TEMPLATE.md`.

## No-alcance
Validador (TASK-0011), carpeta specs/ (TASK-0010), ejemplo (TASK-0012), README (TASK-0013).

## execution_pipeline
1. `TASK_PROTOCOL.md`: añadir gate SDD al ciclo de vida + regla discovery-antes-de-implementar + revisión contra spec/criterios (DISENO §2.1).
2. `TASK_TEMPLATE.md`: añadir `type` y los 6 campos SDD / 4 mínimos con guía por tipo (DISENO §1, §2.2).
3. `HANDOFF_TEMPLATE.md`: añadir "Criterios cumplidos" y "Pruebas ejecutadas" (DISENO §2.3).
4. `HUMAN_REPORT_TEMPLATE.md`: referenciar spec/criterios/pruebas (DISENO §2.4).
5. Validar y handoff.

## acceptance_criteria
- Las 4 plantillas incluyen los elementos de DISENO §2, redactadas **neutrales de dominio**.
- `TASK_TEMPLATE.md` distingue campos por `type`.
- No se rompe ninguna instancia/ejemplo existente.

## test_plan
- Barrido de neutralidad sobre las 4 plantillas (sin trading/.NET/SQL/Azure).
- `validate_collaboration_state.py` y `.ps1` verdes en raíz + `examples/minimal_instance` + `examples/dotnet_enterprise_instance`.

## closure_criteria
- acceptance_criteria cumplidos y demostrados en el handoff (criterios + pruebas).
- Revisión cruzada del arquitecto OK; validadores verdes.
