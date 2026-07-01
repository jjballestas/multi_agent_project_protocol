---
task_id: TASK-0232
title: "[REQ-ZEUS-001][WS3.5] Instalador electron-builder firmado (Windows) + desinstalacion limpia + gate de purga de assets"
type: build
status: proposed
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001]
linked_decisions: [DECISION-0075, DECISION-0076, DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0232-reqzeus-ws35-instalador.md
---

# TASK-0232 - [REQ-ZEUS-001][WS3.5] Instalador + empaquetado

- **Owner build:** Codex (DevOps) - **Review:** Analista - **Checker:** Arquitecto
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. Dep: WS2 (0230), WS3 (0229).

## Alcance
1. electron-builder Windows (MSI/NSIS/Squirrel), **firmado si hay cert**; incluye app + gateway (D4) + cliente de modelos (D3).
2. 1er arranque dispara el bootstrapper (WS2). Desinstalacion limpia (sin residuos).
3. **Gate de purga:** los 154 assets de terceros (hermesworld + logos NousResearch) NO pueden quedar en `dist/`
   (build/CI falla si quedan). THIRD-PARTY-NOTICES con **2 avisos MIT** (Hermes Workspace + hermes-agent).

## DoD
- Doble clic instala sin terminal; desinstala sin residuos; runbook de instalacion.
- CI gate: presencia de los 2 LICENSE MIT + ausencia de assets de marca de terceros en `dist/` (verde por exit-code).
- Gate Analista: GO. maker!=checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
