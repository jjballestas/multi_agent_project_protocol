---
task_id: TASK-0239
title: "[VISION-NOVA][F1.2] Evento firmado exception.recorded (intent nuevo en submit_intent + doctrina U1-U3)"
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
file: Area_comun/tasks/TASK-0239-visionnova-f1b-exception-recorded.md
intake:
  type: infra
  goal: Anadir el intent firmado exception.recorded a submit_intent (schema A.1) + doctrina U1-U3.
  acceptance:
    - submit_intent rechaza kind fuera de enum, summary no-ASCII, exception_id duplicado y task_id inexistente.
    - Round-trip de 2 eventos reales (assist + arbitration) con replay drift cero y listables por task_id.
    - Regla U2 (listado publicable) documentada en TASK_PROTOCOL con scan_encoding verde.
  verification_cmd:
    - python scripts/test_exception_recorded.py
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - runtime/submit_intent.py
    - Area_comun/protocol/TASK_PROTOCOL.md
  out_of_scope:
    - budget_overrun auto-pause queda en Carril B, fuera de F1.
    - protocol.config.json permanece pineado e intocable.
  risk: medium
  estimate: M
---

# TASK-0239 - [VISION-NOVA][F1.2] Evento firmado exception.recorded

Spec: personal/operador/vision-nova/F0/SPEC-F1-exception-trailers.md PARTE A (v0.2).

## Alcance
Intent `exception` en submit_intent + schema A.1 (enums cerrados, ASCII, sin PII) + doctrina
U1-U3 en TASK_PROTOCOL.md (y template). Firmado ed25519, entra a la cadena #4.
`budget_overrun` queda SOLO como kind/evento (el auto-pause es Carril B, fuera de F1 - F-5).

## NOTA (hallazgo F-3, se formaliza en F1-F/TASK-0243)
Si toca runtime/eventlog.py (pineado), la clausula pin-anclado-al-tag se registra en F1-F;
el pin es de reproducibilidad del TFM (congelado en tag TFM-dataset-N500), el validador/runtime
vivo evoluciona hacia v1.18.0. protocol.config.json (epoch) permanece intocable.

## DoD (testable)
1. submit_intent acepta el intent y rechaza: kind fuera de enum, summary no-ASCII,
   exception_id duplicado, task_id inexistente (4 tests negativos).
2. Round-trip: 2 eventos reales (assist + arbitration) emitidos, replay drift=0, listables
   por task_id.
3. Regla U2 (listado publicable) documentada en TASK_PROTOCOL; scan_encoding verde.
4. Los 3 gates verdes en clon limpio.
