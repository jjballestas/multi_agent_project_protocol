---
id: TASK-0106
owner: Codex
status: ready
type: implementation
priority: medium
created_at: 2026-06-13
updated_at: 2026-06-13
depends_on: [TASK-0105]
relates_to: [DECISION-0031, DECISION-0030, DECISION-0009, DECISION-0024, DECISION-0022, DECISION-0008]
phase: P2
spec_id: SPEC-0078
linked_decisions: [DECISION-0031, DECISION-0030, DECISION-0009, DECISION-0024, DECISION-0022, DECISION-0017, DECISION-0008]
deliverables:
  - runtime/orchestrator.py (build_turn_context + assembled_context_tokens + delegate_subagent, off-by-default)
  - runtime/runlog.py (resumenes destilados + rolling summary)
  - protocol.config.json + protocol.config.template.json (bloque runtime.context_policy, defaults false)
  - scripts/measure_context_cost.py (+ .ps1) tokens de contexto por turno con/sin compaction + baseline
  - examples/context_policy_cases (GC-1..GC-9 deterministas)
relevant_files:
  - runtime/orchestrator.py
  - runtime/runlog.py
  - runtime/adapters/base.py
  - runtime/budget.py
  - protocol.config.json
  - protocol.config.template.json
  - scripts/measure_context_cost.py
blocked_by_questions: []
objective: (DECISION-0030 piezas 4-5) Formalizar el ensamblado del contexto del turno (compaction / tool-result clearing) para que no incluya estado full ni event log crudo y reinyecte solo resumenes destilados, y habilitar un primitivo de delegacion a sub-agente con ContextPack limpio que devuelve un resumen acotado. Evitar que el contexto vuelva a crecer al acumular turnos.
expected_output: (1) Bloque runtime.context_policy off-by-default. (2) build_turn_context arma contexto desde slim-views (SPEC-0077) + referencias + ultimos N resumenes; nunca full ni events.jsonl. (3) Tool-result clearing + rolling summary en runlog. (4) Gate de resumen destilado acotado al cerrar tarea. (5) delegate_subagent aislado y acotado por budget.py + caps de DECISION-0024. (6) measure_context_cost con/sin compaction. (7) GC-1..GC-7 verdes; validador/neutralidad/encoding verdes; sin secretos.
question_to_resolve: Ninguna abierta; SPEC-0078 fija contrato y limites. Ambiguedad en implementacion -> handoff blocked + pregunta concreta. subagents_enabled no se activa sin GO del operador (DECISION-0024).
closure_criterion: ensamblado + tool-result clearing + resumen de cierre + delegacion implementados off-by-default; GC-1..GC-7 verdes; medicion por turno adjunta; handoff autocontenido; TASK-0106 en done.
sdd_required: true
---

# TASK-0106 - Compaction / tool-result clearing y sub-agentes (DECISION-0030 piezas 4-5)

> READY+GO (Claude 2026-06-13, GO del operador via DECISION-0031). Implementa SPEC-0078 con los deltas
> corregidos (revision adversarial TASK-0109). Depende de TASK-0105 (done). `subagents_enabled` exige GO
> explicito (DECISION-0024). Implementacion y registro de estado desde VS Code (escritor unico).
>
> **GATE DE MEDICION BLOQUEANTE (DECISION-0008/0031):** corre `measure_context_cost --baseline` ANTES de
> congelar cualquier umbral/cadencia de DELTA-1/2/4 en AC7/AC8/GC-8/GC-9. Ningun numero heredado de papers
> entra a AC/golden; los goldens aseveran comportamiento estructural + umbral medido del caso.
>
> **Alcance minimo seguro:** medicion (`assembled_context_tokens` en `build_turn_context`) -> limites
> off-by-default -> tool-result clearing con referencias en `runlog` -> trigger determinista provisional
> (overhead `<5%` medido, sin LLM en hot path) -> GC-8/GC-9. **DELTA-3 (edicion atomica) FUERA de 0106**
> (Future Work TASK-0107; si entra algun dia, SOLO via `submit_intent`). DELTA-4: justifica 2000 vs 1200
> por medicion en SPEC-0078 sec.2.5, no por cita.

## Contexto

Ver DECISION-0030 (piezas 4-5) y SPEC-0078. Los turnos del runtime ya son single-shot y el ContextPack ya
pasa referencias; falta la politica que impida reinyectar estado full / log crudo / salida cruda de turnos
previos, y un primitivo de sub-agente que aisle el trabajo profundo devolviendo solo un resumen acotado.

## Entrada

SPEC-0078 cerrada (AC + test_plan + golden cases). Depende de TASK-0105 (slim-views). Codex entrega handoff
autocontenido con evidencia (medicion por turno con/sin compaction, golden cases reproducibles).
