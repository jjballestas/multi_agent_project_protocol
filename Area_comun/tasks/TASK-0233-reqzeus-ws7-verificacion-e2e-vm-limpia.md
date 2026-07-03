---
task_id: TASK-0233
title: "[VISION-NOVA][F2.2] Verificacion e2e distribuida: un clon limpio opera 1 tarea completa solo via Git [re-alcance: pivote Vision Nova, DECISION-0083]"
type: build
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0075, DECISION-0076, DECISION-0077, DECISION-0083, DECISION-0085]
linked_reqs: [REQ-ZEUS-001]
depends_on: [TASK-0230, TASK-0232]
file: Area_comun/tasks/TASK-0233-reqzeus-ws7-verificacion-e2e-vm-limpia.md
intake:
  type: research
  goal: Verificacion e2e distribuida de la instancia Aegis - un clon LIMPIO opera 1 tarea completa de principio a fin usando SOLO Git (pull/push via el harness F2.3), demostrando transferibilidad de la metodologia.
  acceptance:
    - Un clon limpio de la instancia Aegis (sin residual de dev) opera 1 tarea completa (claim -> trabajo -> entrega -> cierre) coordinando SOLO via Git (pull/push), usando el harness distribuido de TASK-0232.
    - La coordinacion es visible entre clones: el claim/estado escrito por el clon aparece en el origin/otro clon tras pull, sin colision ni perdida.
    - Evidencia reproducible (logs/comandos/hashes) adjunta en un artefacto ANALISTA-TASK-0233-* en el hub.
    - El ciclo mantiene validate/encoding/neutralidad verdes en el clon; sin drift.
    - Opera sobre la instancia Aegis (NOVA/Aegis); NO toca el hub (epoch pineado byte-identico) ni crea repos de producto.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/artifacts/
  out_of_scope:
    - NO toca el core del protocolo ni los pineados (epoch 1.14.0 byte-identico).
    - NO crea repos de producto (Nova-X lazy); la e2e es sobre la operacion distribuida de la instancia.
    - NO instala Engram ni gentle-ai install.
  risk: medium
  estimate: M
---

# TASK-0233 - [VISION-NOVA][F2.2] Verificacion e2e distribuida (re-alcance DECISION-0083/0085)

- **Owner (maker):** Codex - **Review:** Analista - **Checker:** Arquitecto. maker != checker.
- **RE-ASIGNACION 2026-07-03 (owner Analista -> Codex):** el backlog asignaba owner=Analista, pero el Analista
  es CHECKER-ONLY por identidad (maker != checker, directiva del operador reforzada); se nego correctamente a
  ser maker. Resolucion: **Codex construye la demostracion e2e (maker)**, el **Analista la verifica
  adversarialmente (checker)**. Ver FYI al operador. La e2e sigue siendo la prueba de transferibilidad.
- **Instancia:** `D:/Agentes/Zeus/NOVA/Aegis` (DECISION-0085). **Deps:** F2.1 (0230, done) + F2.3 (0232, harness distribuido).

## Alcance (re-alcance DECISION-0083; body viejo de e2e Zeus-Aegis SUPERADO)
Verificacion e2e DISTRIBUIDA de la instancia Aegis: un CLON LIMPIO (como lo veria un empleado/agente que
se une por primera vez via Git) opera 1 TAREA COMPLETA de principio a fin (claim -> trabajo -> entrega ->
cierre) coordinando SOLO via Git (pull/push con el harness distribuido de TASK-0232), sin pasos manuales
ocultos ni servidor central de estado. Es la prueba de TRANSFERIBILIDAD de la metodologia: un agente en un
clon limpio puede operar el protocolo end-to-end.

## DoD (testable)
Ver bloque intake (acceptance). Cierre: los AC pasan con evidencia reproducible en un artefacto
ANALISTA-TASK-0233-*; coordinacion visible entre clones; gates verdes en el clon; hub intacto.

## Handoff
Autocontenida. maker (Analista) != checker (Arquitecto). Ambiguedad -> blocked + 1 pregunta concreta.
