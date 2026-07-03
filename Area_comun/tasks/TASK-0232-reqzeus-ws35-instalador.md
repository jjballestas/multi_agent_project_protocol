---
task_id: TASK-0232
title: "[VISION-NOVA][F2.3] Harness distribuido pull -> escribir -> push inmediato (claims visibles entre clones) + hosting privado de la instancia [re-alcance: pivote Vision Nova, DECISION-0083]"
type: build
status: ready
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0075, DECISION-0076, DECISION-0077, DECISION-0083, DECISION-0085]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0232-reqzeus-ws35-instalador.md
intake:
  type: infra
  goal: Harness distribuido de la instancia Aegis (NOVA/Aegis) que hace pull -> escribir estado/claim -> push inmediato, de modo que los claims sean visibles entre clones; con hosting privado de la instancia.
  acceptance:
    - El harness ejecuta el ciclo pull -> escribir (claim/estado via submit_intent) -> push inmediato sobre el repo de la instancia Aegis, sin dejar el push diferido.
    - Dos clones de la instancia (o clon + origin) demuestran que un claim escrito por un clon es VISIBLE en el otro tras pull (evidencia reproducible: claim aparece, no colision).
    - Hosting privado de la instancia configurado (repo remoto privado propio de la instancia; NO hereda remoto del hub).
    - Anti-colision respetado: ventana segura + push inmediato (no medio-escribir sin push); el ciclo no rompe validate en el clon.
    - Gates verdes en clon limpio (validate/encoding/neutralidad) sobre la instancia y el hub intacto.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - scripts/
    - runtime/
  out_of_scope:
    - NO toca el epoch pineado ni protocol.config.json del hub (1.14.0 byte-identico).
    - NO crea repos de producto (Nova-X son lazy; esta tarea es sobre la operacion distribuida de la instancia Aegis).
    - NO instala Engram ni gentle-ai install.
  risk: medium
  estimate: M
---

# TASK-0232 - [VISION-NOVA][F2.3] Harness distribuido (re-alcance DECISION-0083/0085)

- **Owner build:** Codex (DevOps) - **Review:** Analista - **Checker:** Arquitecto
- **Instancia:** `D:/Agentes/Zeus/NOVA/Aegis` (repo propio de la instancia, DECISION-0085). Dep: F2.1 (0230, done).

## Alcance (re-alcance DECISION-0083; body viejo de instalador electron SUPERADO)
Harness de operacion DISTRIBUIDA de la instancia Aegis: un agente en un clon hace **pull -> escribir
(claim/estado via submit_intent) -> push INMEDIATO**, para que los claims sean visibles entre clones
(coordinacion via Git puro, sin servidor central de estado). Incluye **hosting privado** de la
instancia (remoto propio, no el del hub).

1. Ciclo pull -> write -> push inmediato (sin push diferido) sobre el repo de la instancia Aegis.
2. Demostrar visibilidad de claims entre clones: un claim de un clon aparece en otro tras pull, sin colision.
3. Hosting privado de la instancia (remoto privado propio; no hereda el remoto del hub).
4. Respetar anti-colision (ventana segura + push inmediato); el ciclo mantiene validate verde en el clon.

## DoD (testable)
Ver bloque intake (acceptance). Cierre: GO adversarial del Analista + evidencia reproducible de claim
visible entre clones + gates verdes en clon limpio. maker != checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
