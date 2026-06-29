---
task_id: TASK-0222
title: "Zeus-Aegis: vista Estadisticas (stats) completa: costo tokens por agente + chip progreso dataset X/500, read-only F1"
type: build
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0064, DECISION-0070, DECISION-0040]
file: Area_comun/tasks/TASK-0222-codex-zeus-aegis-vista-stats.md
---

# TASK-0222 — Zeus-Aegis: vista Estadísticas (stats) completa

- **Owner:** Codex (build) · **Review:** Analista (gate adversarial)
- **Linked:** DECISION-0064 (UI sobre metodología, F1 read-only), DECISION-0070 (stats costo tokens), DECISION-0040 (dataset/PII)

## Contexto
El panel Zeus-Aegis (`D:\Agentes\Zeus\Zeus-Aegis`) expone `/api/governance/agent-metrics`
(fusiona `scripts/agent_token_usage.py` + `scripts/session_token_usage.py`). Falta consolidar
la **vista de Estadísticas** del panel.

## Alcance
1. Vista Estadísticas read-only (F1, sin escritura al ledger) que muestre:
   - Costo de tokens real por agente (Arquitecto / Codex / Analista) y total.
   - **Chip de progreso del dataset: X/500** (eventos elegibles `seq>=2221 ∧ intent.applied ∧ ed25519`).
2. Render estable en clon limpio (cuidado con flaky vite-dev: pre-warm + reload + poll).

## DoD
- Render verde verificado en clon limpio (no working tree caliente con dist/ residual).
- Sin escritura al ledger; respeta waiver F1.
- Reporte de checker con evidencia (screenshot + endpoint OK).
- Gate Analista: GO.

## Handoff
Autocontenida. Ambigüedad → `blocked` + 1 pregunta concreta.
