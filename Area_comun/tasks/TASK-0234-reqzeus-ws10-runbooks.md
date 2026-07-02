---
task_id: TASK-0234
title: "[VISION-NOVA][F2.5] Runbook de onboarding remoto de empleados (objetivo <=1 dia, medido; alimenta HP6) [re-alcance: pivote Vision Nova, DECISION-0083]"
type: docs
status: proposed
owner: Arquitecto
phase: P2
priority: low
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0077, DECISION-0083]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0234-reqzeus-ws10-runbooks.md
---

# TASK-0234 - [VISION-NOVA][F2.5] Runbook onboarding remoto (re-alcance DECISION-0083)

- **Owner:** Arquitecto (Docs) - **Review:** Analista
- Dep: WS3.5 (0232). Entregable doc-only.

## Alcance
1. Runbook de **instalacion** (doble clic -> entorno listo) para empleados.
2. Runbook de **operacion** (arranque/stop del gateway, backend, cambio de modelos, resolucion de problemas) para soporte.

## DoD
- Runbooks autocontenidos; cubren instalacion + operacion + troubleshooting.
- Gate doc-only (checks de doc, no npm test). Gate Analista: GO.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
