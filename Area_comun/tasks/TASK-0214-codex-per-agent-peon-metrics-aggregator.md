---
task_id: TASK-0214
title: "Agregador read-only de estadisticas por agente y por peon (ledger + runlogs + provenance) (DECISION-0070, SPEC-0109)"
type: protocol
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
maker: Codex
checker: Arquitecto
linked_decisions: [DECISION-0070]
spec: SPEC-0109
file: Area_comun/tasks/TASK-0214-codex-per-agent-peon-metrics-aggregator.md
---

# TASK-0214 -- Agregador read-only de estadisticas por agente y por peon (DECISION-0070 / SPEC-0109)

## Objetivo
Agregador READ-ONLY (`scripts/agent_metrics.py` NUEVO) que deriva metricas por agente/peon del ledger + runlogs:
calidad (done vs rechazada, tasa aceptacion, ciclos de revision), tiempo (lead/cycle), tokens/coste (autoria vs
revision). DOMAIN-NEUTRAL, no toca pineados del hub. Spec autocontenido en SPEC-0109; rationale en DECISION-0070.

## Alcance (SOLO archivo NUEVO; no tocar pineados)
- `scripts/agent_metrics.py`: lee `runtime/state/events.jsonl` + runlogs (via `runtime/metrics.py`); emite JSON
  {por_agente, por_peon, por_tarea}. La dimension por_peon usa la provenance de DECISION-0069 cuando exista; la
  dimension por_agente funciona ya desde el ledger.
- Golden test sobre fixture de eventos conocido.

## Criterios de aceptacion
AC1-AC6 de SPEC-0109. CRITICOS:
- **AC5 (READ-ONLY/GUARDRAIL):** correr el agregador deja `events.jsonl` + pineados del hub byte-identicos (sha256
  antes/despues). Incluye el check.
- **AC2/AC3/AC4:** calidad/tiempo/tokens correctos contra el golden.

## DoD
AC1-AC6 verdes en clon limpio. Handoff `in_review` con JSON de ejemplo + sha256 pineados antes/despues identicos.
Commit como Arquitecto + Co-Authored-By Codex. checker=Arquitecto. NOTA: depende parcialmente de TASK-0213 (la
atribucion por-peon necesita su provenance); la dimension por-agente no. Sigue: vista panel Zeus-Aegis (producto).
