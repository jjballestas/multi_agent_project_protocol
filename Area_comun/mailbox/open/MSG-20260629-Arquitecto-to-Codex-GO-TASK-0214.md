---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0214
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0214
status: open
requires_response: false
---

# GO - TASK-0214 (agregador de estadisticas por agente y por peon)

Codex: arranca **TASK-0214** (maker). DECISION-0070 ratificada. Spec en
`Area_comun/specs/SPEC-0109-per-agent-peon-metrics-aggregator.md`.

Encargo (READ-ONLY, DOMAIN-NEUTRAL, no contamina TFM):
- **`scripts/agent_metrics.py` (NUEVO):** lee `runtime/state/events.jsonl` + runlogs (via `runtime/metrics.py`);
  emite JSON `{por_agente, por_peon, por_tarea}`:
  - calidad: done vs changes_requested/cancelled por actor, tasa de aceptacion, ciclos de revision.
  - tiempo: lead time (created->done) y cycle time (in_progress->done) de los timestamps.
  - tokens/coste: total y por-tarea (de runtime/metrics.py), desglose AUTORIA (maker/peon) vs REVISION (checker)
    por rol; dimension POR PEON usa la provenance de DECISION-0069 (`attested_instancing.provenance_metadata`,
    autor real + modelo) cuando exista; la dimension por_agente funciona ya desde el ledger.
- Golden test sobre fixture de eventos conocido.

AC1-AC6 en el spec. **CRITICO AC5 (READ-ONLY):** correr el agregador deja `events.jsonl` + los 5 pineados del hub
byte-identicos (sha256 antes/despues); incluye el check. El agregador SOLO lee, nunca escribe el ledger.

NO tocar pineados del hub. `scan_domain_neutrality` limpio. Commit como Arquitecto + `Co-Authored-By: Codex`,
entrega `in_review` con JSON de ejemplo + sha256 antes/despues. ETA: corta-media. Si algo bloquea -> `blocked`.
