---
task_id: TASK-0243
title: "[VISION-NOVA][F1.5] Mini-DECISION identidad anti-vibecoding + clausula pin-anclado-al-tag"
type: docs
status: proposed
owner: Arquitecto
phase: P2
priority: medium
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0083]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0243-visionnova-f1f-decision-antivibecoding.md
---

# TASK-0243 - [VISION-NOVA][F1.5] Mini-DECISION identidad anti-vibecoding

Owner: Arquitecto (redaccion corta; existe draft en REQs Zeus-Aegis v0.2.0 del area del operador).

## Alcance
Registra la identidad (interrogacion de requisitos + quality panel + excepciones auditadas via
F1-B/TASK-0239) como decision de doctrina. INCLUYE la clausula del hallazgo F-3: el pin de los
5 archivos byte-identicos (`PINNED_RELATIVE_PATHS` en scripts/agent_metrics.py) esta ANCLADO al
tag TFM-dataset-N500 (reproducibilidad del estudio, congelada); el validador/runtime vivo
evoluciona legitimamente hacia v1.18.0. protocol.config.json (epoch v1.14.0 PINNED) permanece
byte-identico.

## DoD (testable)
1. DECISION registrada via submit_intent, relates_to GOAL-VISION-NOVA-001 + DECISION-0083.
2. Clausula pin-anclado-al-tag explicita en el cuerpo.
3. Los 3 gates verdes en clon limpio.
