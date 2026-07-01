---
task_id: TASK-0231
title: "[REQ-ZEUS-001][WS4] Backend de modelos por defecto (D3) + bloqueo PII + spike peones (repo sandbox aparte)"
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
linked_decisions: [DECISION-0074, DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0231-reqzeus-ws4-backend-modelos-peones.md
---

# TASK-0231 - [REQ-ZEUS-001][WS4] Backend de modelos + peones

- **Owner build:** Codex - **Review:** Analista (seguridad/PII) - **Checker:** Arquitecto - Decision de backend: Operador.
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. **Spike de peones en repo SANDBOX aparte** `D:/Agentes/Zeus/piloto-peones`. Dep: D3 (0074).

## Alcance
1. Backend por defecto (router empresa OpenAI-compat u Ollama local) que expone **modelos frontera** (firmantes) +
   **peon** (drafter boilerplate). Punto unico de claves/costo.
2. **Bloqueo PII (cero-egress):** prueba negativa de que datos reales NO salen a modelos externos.
3. **Spike de peones (opcional, en sandbox aparte):** experimento A/B/C de la guia (DECISION-0074); metrica que decide
   = tokens del firmante; peon = maker keyless fuera del ledger, firmante distinto firma (maker!=checker).

## DoD
- Chat de prueba responde; claves fuera del repo; **prueba negativa PII no sale**.
- Si se corre el spike: va en `D:/Agentes/Zeus/piloto-peones`, cero escritura al repo medido; reporte de medicion.
- Gate Analista (seguridad): GO. maker!=checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
