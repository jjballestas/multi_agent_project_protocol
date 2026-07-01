---
task_id: TASK-0230
title: "[REQ-ZEUS-001][WS2] Bootstrapper: auto-instalacion + ciclo de vida (gateway+backend+config) en Electron main"
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
linked_decisions: [DECISION-0074, DECISION-0075, DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0230-reqzeus-ws2-bootstrapper.md
---

# TASK-0230 - [REQ-ZEUS-001][WS2] Bootstrapper (auto-instalacion + lifecycle)

- **Owner build:** Codex - **Review:** Analista - **Checker:** Arquitecto
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. Dep: D3 (0074), D4 (0075). Reusa `autoStartGateway` existente.

## Alcance (modulo en Electron main; idempotente; con logs)
1. En 1er arranque: **detecta/instala el gateway** (hermes-agent, D4 vendorizado o desde fuente).
2. **Apunta/instala el backend** de modelos (D3: router empresa por defecto; Ollama local donde haya GPU).
3. Escribe **config resuelta** en `~/.zeus`.
4. Levanta el gateway en `:8642` con **health-check / reinicio / cierre limpio**.

## DoD
- Maquina limpia -> gateway `:8642` corriendo + backend conectado **sin intervencion**.
- **0 procesos huerfanos** al cerrar; re-abrir es idempotente. Logs de arranque legibles.
- Claves fuera del repo (D3). Sin PII saliente. Gate Analista: GO. maker!=checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
