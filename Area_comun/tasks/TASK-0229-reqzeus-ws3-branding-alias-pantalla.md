---
task_id: TASK-0229
title: "[REQ-ZEUS-001][WS3] Capa de branding + alias env ZEUS_* con shim + pantalla 'Preparando tu entorno Zeus'"
type: build
status: proposed
owner: Codex
phase: P2
priority: high
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001]
linked_decisions: [DECISION-0076, DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
---

# TASK-0229 - [REQ-ZEUS-001][WS3] Capa de branding white-label

- **Owner build:** Codex - **Review:** Analista - **Checker:** Arquitecto
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. Ejecuta el plan de WS1 (`docs/BRANDING-PLAN-WS1.md`). Dep: WS1 (TASK-0226).

## Alcance (ejecuta el plan de WS1 bajo DECISION-0076)
1. UI/strings/i18n + copy de onboarding -> "Zeus-Aegis".
2. **Alias de env visibles** `HERMES_API_URL`->`ZEUS_API_URL`, `HERMES_API_TOKEN`->`ZEUS_API_TOKEN` con **shim de
   compatibilidad** (patron de los fallbacks `CLAUDE_*` existentes).
3. Reemplazar el copy de setup manual por pantalla **"Preparando tu entorno Zeus..."**.
4. **NO renombrar** binarios internos/`appId`/paquetes (preserva merge upstream). Conservar NOTICE MIT.

## DoD
- 0 cadenas "hermes" VISIBLES al usuario; alias con shim funcionando; NOTICE/LICENSE MIT permanece.
- Render verde en clon limpio; `npm test` verde. La purga de assets de terceros es gate de release aparte (no aqui).
- Gate Analista: GO. maker!=checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
