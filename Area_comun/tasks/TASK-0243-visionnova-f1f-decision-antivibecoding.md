---
task_id: TASK-0243
title: "[VISION-NOVA][F1.5] Mini-DECISION identidad anti-vibecoding + clausula pin-anclado-al-tag"
type: docs
status: review_approved
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
intake:
  type: doc
  goal: Registrar DECISION-0084 (identidad anti-vibecoding + anexo Definition of Ready 10 puntos + clausula pin-anclado-al-tag) y anotar la extension intake v2 en TASK-0230/F2.1.
  acceptance:
    - DECISION-0084 registrada via submit_intent (intent decision) con el .md en Area_comun/decisions/, relates_to GOAL-VISION-NOVA-001 + DECISION-0083.
    - Clausula pin-anclado-al-tag explicita (5 pineados anclados a TFM-dataset-N500; validador vivo evoluciona; protocol.config.json intocable).
    - Anexo Definition of Ready con los 10 puntos verbatim del Operador + mapa de cobertura v1 y regla anti-vacio v2 (directiva dae40ac).
    - Cuerpo de TASK-0230 anotado con la extension del template de instancia (campos v2 para type feature/product).
    - GO adversarial del Analista sobre la DECISION.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/decisions/
    - Area_comun/tasks/TASK-0230-codex-reqzeus-ws2-new-instance-electron.md
  out_of_scope:
    - NO se reabre TASK-0238 ni se toca el validador del hub (enforcement v2 = instancia F2.1 o v1.19 futura).
    - protocol.config.json y los 5 pineados vivos permanecen intocables.
    - No implementa la interrogacion en harnesses (aterriza en la instancia, F2).
  risk: low
  estimate: S
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
