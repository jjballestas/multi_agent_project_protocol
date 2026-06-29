---
spec_id: SPEC-0109
title: Agregador read-only de estadisticas por agente y por peon (ledger + runlogs + provenance)
status: ready
owner: Codex
decision: DECISION-0070
relates_to: [DECISION-0070, DECISION-0069]
date: 2026-06-29
file: Area_comun/specs/SPEC-0109-per-agent-peon-metrics-aggregator.md
---

# SPEC-0109 -- Agregador read-only de estadisticas por agente y por peon

Implementa el agregador de DECISION-0070. READ-ONLY, DOMAIN-NEUTRAL, no toca pineados del hub.

## Componente

`scripts/agent_metrics.py` (NUEVO): lee `runtime/state/events.jsonl` (canonico) + runlogs (`runtime/runs/`,
via `runtime/metrics.py`) y emite un JSON de metricas por actor:

- **calidad:** por owner/actor, conteo de tareas `done` vs `changes_requested`/`cancelled`, tasa de aceptacion,
  nro medio de ciclos de revision por tarea (de las transiciones `task_status`).
- **tiempo:** lead time (created->done) y cycle time (in_progress->done) por tarea, de los timestamps de eventos.
- **tokens/coste:** total y por tarea (de `runtime/metrics.py`), desglosado autoria (maker) vs revision (checker)
  por rol; cuando exista provenance (DECISION-0069), atribuir autoria por PEON (autor real) + modelo.
- **agregados:** por agente (Arquitecto/Codex/Analista) y, cuando haya provenance, por peon.

## Criterios de aceptacion

- **AC1:** `python scripts/agent_metrics.py` emite JSON valido con secciones {por_agente, por_peon, por_tarea};
  la dimension por_agente se calcula desde el ledger actual (sin requerir provenance).
- **AC2 (calidad):** cuenta done vs changes_requested/cancelled por actor y tasa de aceptacion correctas contra un
  fixture/golden de eventos conocido.
- **AC3 (tiempo):** lead/cycle time por tarea derivados de timestamps; coherentes en el golden.
- **AC4 (tokens):** total y por-tarea consistentes con `runtime/metrics.py`; desglose autoria/revision por rol.
- **AC5 (READ-ONLY + GUARDRAIL):** el agregador SOLO lee; correrlo deja `runtime/state/events.jsonl` y los
  pineados del hub byte-identicos (mismo sha256 antes/despues). Incluye el check.
- **AC6:** `scan_domain_neutrality.py` limpio; golden test sobre fixture de eventos; sin red ni escritura.

## DoD

AC1-AC6 verdes en clon limpio. Handoff `in_review` con el JSON de ejemplo (sobre el ledger real o un fixture) +
sha256 de pineados antes/despues identicos. maker=Codex/checker=Arquitecto. Sigue (producto): vista del panel
Zeus-Aegis que consume este agregador (tarea aparte).
