---
task_id: TASK-0240
title: "[VISION-NOVA][F1.3] Trailers bloqueantes Task-Id / Fixes-Task en el validador (V1-V5)"
type: build
status: in_progress
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
file: Area_comun/tasks/TASK-0240-visionnova-f1c-trailers-bloqueantes.md
intake:
  type: infra
  goal: Escaneo de trailers Task-Id / Fixes-Task en el validador (V1-V5) con trailer_start_seq registrado.
  acceptance:
    - Los 8 casos B.3 (4 negativos + 4 positivos) como tests sobre repo fixture pasan.
    - El repo valida verde con los commits historicos exentos por el arranque declarado.
    - Un commit de prueba sin trailer hace fallar validate de forma reproducible y se revierte.
  verification_cmd:
    - python scripts/test_trailers.py
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - scripts/validate_collaboration_state.py
    - scripts/validate_collaboration_state.ps1
  out_of_scope:
    - Activar el trailer_start_seq antes del despliegue de F1-E (TASK-0242) queda prohibido (auto-DoS).
    - protocol.config.json permanece pineado e intocable.
  risk: medium
  estimate: M
---

# TASK-0240 - [VISION-NOVA][F1.3] Trailers bloqueantes Task-Id / Fixes-Task

Spec: personal/operador/vision-nova/F0/SPEC-F1-exception-trailers.md PARTE B (v0.2).

## Alcance
Escaneo de rango de commits en el validador (V1-V5), `trailer_start_seq` registrado,
allowlist ops (`Task-Id: none` + `Ops-Reason`).

## CONDICION DE ACTIVACION (hallazgo F-2 del Arquitecto, ya en SPEC v0.2 y backlog v2)
La CONSTRUCCION puede avanzar antes, pero la ACTIVACION (fijar `trailer_start_seq`) es
PRECONDICION DURA de que F1-E (TASK-0242) este DESPLEGADO: los harnesses de Codex/Analista
y el flujo del Arquitecto deben emitir trailers antes de activar, o cada commit gobernado
sin trailer pone `validate` rojo (auto-DoS del pipeline). Activar antes esta PROHIBIDO.

## DoD (testable)
1. Los 8 casos B.3 (4 negativos + 4 positivos) como tests sobre repo fixture; verdes.
2. El propio repo valida verde con commits historicos exentos (arranque declarado).
3. Un commit de prueba sin trailer hace fallar validate (demo reproducible); revertido
   tras la evidencia.
4. Los 3 gates verdes en clon limpio. trailer_start_seq fijado post-despliegue de F1-E.
