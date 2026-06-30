---
task_id: TASK-0226
title: "REQ-ZEUS WS1: inventario de 'hermes' en Zeus-Aegis + plan de branding white-label"
type: build
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0050]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0226-codex-reqzeus-ws1-inventario-hermes-branding.md
---

# TASK-0226 — REQ-ZEUS WS1: inventario "hermes" + plan de branding

- **Owner build:** Codex · **Review:** Analista · **Gobierna:** Arquitecto
- **Repo de PRODUCTO (donde va el deliverable):** `D:\Agentes\Zeus\Zeus-Aegis` (NO el hub del protocolo).
- **Gobernanza (esta tarea):** hub `multi_agent_project_protocol`.
- **Decisiones que aplican:** D1 tiered, D5 rebrand SUPERFICIAL (alias HERMES->ZEUS con shim, sin renombrar
  binarios/appId, mergeable upstream), D4 (hermes-agent = MIT; conservar avisos; logo NousResearch = purga aparte).

## Alcance (entregable = un documento + matriz, NO codigo todavia)
1. **Inventario** de donde aparece "hermes" visible al usuario en el fork: strings/i18n, copy de onboarding
   ("Looking for hermes-agent", "Detecting...", "Run the installer", "hermes setup", "hermes gateway run"),
   logica de deteccion del gateway, variables de entorno (`HERMES_API_URL`/`HERMES_API_TOKEN`/`HERMES_DASHBOARD_*`),
   URLs de instalacion, `electron-builder.config.cjs` (appId/productName/copyright/auto-updater), assets de marca.
2. **Plan de branding** (mapa de cambios, sin ejecutarlos aun): textos/i18n "Zeus-Aegis"; alias de env con shim de
   compatibilidad (mismo patron que los fallbacks `CLAUDE_*` existentes); reemplazo del copy de setup manual por
   "Preparando tu entorno Zeus..."; lista de assets de terceros a PURGAR (hermesworld + logos NousResearch) con
   gate de release; preservacion de NOTICE/LICENSE MIT (Hermes Workspace + hermes-agent).
3. Identificar que NO se renombra (binarios internos, appId) para preservar el merge con upstream.

## DoD
- Documento de inventario + plan en `D:\Agentes\Zeus\Zeus-Aegis\docs\` (p.ej. `BRANDING-PLAN-WS1.md`), autocontenido.
- Cubre los 3 puntos de alcance con rutas concretas del fork.
- NO modifica codigo del fork todavia (WS1 = inventario+plan; la capa de branding es WS3).
- Gate Analista: GO/NO-GO.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta. maker!=checker.
