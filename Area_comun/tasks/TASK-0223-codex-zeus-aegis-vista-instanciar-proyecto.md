---
task_id: TASK-0223
title: "Zeus-Aegis: vista Instanciar-proyecto (read-only, prepara comando atestado, NO ejecuta)"
type: build
status: in_review
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-29
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0064, DECISION-0069, DECISION-0050]
file: Area_comun/tasks/TASK-0223-codex-zeus-aegis-vista-instanciar-proyecto.md
---

# TASK-0223 — Zeus-Aegis: vista "Instanciar proyecto" (read-only)

- **Owner:** Codex (build) · **Review:** Analista (gate)
- **Linked:** DECISION-0064 (F1 read-only), DECISION-0069 (ceremonia instanciación atestada), DECISION-0050 (hub + repos producto)

## Contexto
El hub es permanente; los repos de producto rotan bajo `D:\Agentes\Zeus\` (DECISION-0050). La
instanciación atestada está definida en DECISION-0069. Falta una vista en el panel.

## Alcance
1. Vista que muestre el flujo de instanciación atestada en **modo preparar-comando**:
   genera el JSON/cmd de `scripts/new_instance.py` + ceremonia, lo presenta para copiar.
2. **NO ejecuta** (F2 write-through sigue gateado). Read-only puro.

## DoD
- Read-only; respeta waiver F1; no toca el ledger.
- Render verde en clon limpio; evidencia de checker.
- Gate Analista: GO.

## Handoff
Autocontenida. Ambigüedad → `blocked` + 1 pregunta concreta.
