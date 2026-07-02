---
task_id: TASK-0238
title: "[VISION-NOVA][F1.1] Gate de intake determinista (validador pre-ready ps1+python + runtime hard-gate + templates)"
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
file: Area_comun/tasks/TASK-0238-visionnova-f1a-gate-intake.md
---

# TASK-0238 - [VISION-NOVA][F1.1] Gate de intake determinista

Spec: personal/operador/vision-nova/F0/SPEC-F1-gate-intake.md (v0.2).

## Alcance
Reglas R0-R6 en el validador (ps1 + python) y runtime (task_status hard-gate en la
transicion proposed->ready); bloque `intake` en los templates; examples/minimal_instance
actualizado. Neutral de dominio.

## CONDICION DE PROMOCION (hallazgo F-1 del Arquitecto, ya en SPEC v0.2)
R0/`intake_start` (anti-retroactividad) es OBLIGATORIO: las 177 tareas pre-existentes en
ready/claimed/in_progress/in_review/done NO tienen bloque intake; sin el boundary R0, R1
pondria `validate` rojo sobre HEAD y el DoD punto 3 seria inalcanzable. R1 solo aplica a
tareas POSTERIORES a `intake_start`. No promover a ready sin R0 implementado y verde en
clon limpio.

## DoD (testable)
1. Los 6 casos negativos (N1-N6) y 5 positivos (P1-P5, incluye exencion historica R0 y
   HEAD real) del SPEC s.4 implementados como tests; verdes.
2. Transicion proposed->ready via submit_intent con intake invalido = rechazo atomico
   (exit != 0, sin drift).
3. Los 3 gates (validate + scan_encoding + neutralidad) verdes en CLON LIMPIO de HEAD
   (con R0 activo: las pre-existentes exentas).
4. Cero terminos de dominio en core/templates (neutralidad exit 0).
