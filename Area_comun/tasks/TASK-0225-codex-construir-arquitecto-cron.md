---
task_id: TASK-0225
title: "Construir Arquitecto-cron (mailbox processor) analogo a los existentes; lanzamiento real lo hace el operador"
type: build
status: ready
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-29
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0057, DECISION-0038]
file: Area_comun/tasks/TASK-0225-codex-construir-arquitecto-cron.md
---

# TASK-0225 — Construir + dejar listo el Arquitecto-cron

- **Owner:** Codex (build) · **Review:** Analista (gate)
- **Linked:** DECISION-0057 (activar/stand-down runtimes), DECISION-0038 (narración mínima)

## Contexto
Existen `personal/Analista/analista_mailbox_cron.ps1` y `personal/Codex/codex_mailbox_cron.ps1`,
pero NO hay cron del Arquitecto. Falta construir `personal/Arquitecto/arquitecto_mailbox_cron.ps1`
análogo (procesa mailbox→Arquitecto, heartbeat, seen.json, pid/log).

## Alcance
1. Crear `personal/Arquitecto/arquitecto_mailbox_cron.ps1` espejo de los existentes.
2. Runbook breve de arranque/stop. **El lanzamiento real del .ps1 lo ejecuta el operador**
   (deny-rule del harness sobre PowerShell; el agente no lo lanza).

## DoD
- Script presente y consistente con los otros crons; runbook incluido.
- Gate Analista: GO.

## Handoff
Autocontenida. Ambigüedad → `blocked` + 1 pregunta concreta.
