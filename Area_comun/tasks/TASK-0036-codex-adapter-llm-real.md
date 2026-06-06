---
id: TASK-0036
owner: Codex
status: in_review
type: implementation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0031]
relates_to: [TASK-0032]
phase: P2
spec_id: Area_comun/specs/SPEC-0035-adapter-llm-real.md
linked_decisions: [DECISION-0009, DECISION-0001]
execution_pipeline: [runtime/adapters/llm_adapter.py LLMAdapter(AgentAdapter) con invoker pluggable, RecordedInvoker grabable/mock para CI (sin red), limites sandbox-a-root + write-allowlist/denylist M1 + budget por turno, orchestrator --adapter llm --once (un turno, sin autonomia), replay comparativo (llm==replay sobre fixture), golden examples/llm_adapter_cases]
acceptance_criteria: [LLMAdapter implementa AgentAdapter, --adapter llm --once con RecordedInvoker => 1 commit determinista, replay comparativo llm==replay, changed_paths fuera de allowlist/claim => rechazo, budget excedido => abort, default replay sin regresion, enabled:false aborta, sin red ni credenciales en CI]
test_plan: [golden examples/llm_adapter_cases con RecordedInvoker (once/comparativo/rechazo-allowlist/abort-budget/default-replay/enabled-false); sin API en vivo]
closure_criteria: [LLMAdapter + invoker pluggable + RecordedInvoker + limites + replay comparativo + --adapter llm --once, golden verdes, default replay intacto, sin credenciales, handoff autocontenido, claim liberado al pasar a in_review]
---

# TASK-0036 - Adapter LLM real (un turno, limites, replay comparativo, SIN autonomia)

> `implementation` -> SDD; implementar contra [SPEC-0035](../specs/SPEC-0035-adapter-llm-real.md) bajo
> DECISION-0009. **M2 hito 2.** Estado `ready` (operador confirmo 2026-06-06). Las dos confirmaciones que
> bloqueaban quedan FIJADAS:
> - (a) **Mecanismo de invocacion = subproceso generico vendor-neutral** (invoker base parametrizable;
>   Claude SDK / Codex CLI son configuraciones de ese invoker, no el base). Mantiene el core neutral.
> - (b) **Primera corrida real sobre el repo vivo = aprobacion puntual del operador "cuando Claude avise".**
>   Implementa el adapter completo + RecordedInvoker + golden (sin red). NO disparar la corrida real: queda
>   pendiente del OK del operador. CI nunca usa el invoker real.

## Resumen
`LLMAdapter(AgentAdapter)` que construye el prompt desde el ContextPack e invoca al agente real via un
**invoker pluggable**; un `RecordedInvoker` (transcript, sin red) hace los golden deterministas para CI.
Limites: sandbox a root + write-allowlist/denylist de M1 + budget por turno (reusa budget.py). Solo
`--adapter llm --once` (un turno, sin loop autonomo). Replay comparativo: llm(RecordedInvoker) == replay
sobre el mismo fixture (mismo commit/transicion) => prueba que el adapter real es drop-in del replay.

## archivos objetivo (previstos)
- `runtime/adapters/llm_adapter.py` (+ interfaz `Invoker` + `RecordedInvoker`)
- `runtime/orchestrator.py` (anadir `--adapter llm`, gateado)
- `examples/llm_adapter_cases/`

## Coordinacion / decisiones (resueltas por el operador 2026-06-06)
- RESUELTO: mecanismo de invocacion real = **subproceso generico vendor-neutral** (invoker base
  parametrizable; SDK/CLI son configuraciones suyas). El replay sigue como invoker de respaldo.
- RESUELTO: gate humano de la primera corrida real = **aprobacion puntual del operador "cuando Claude
  avise"** (no en CI; corrida explicita; Codex no la dispara).
- ABIERTA (decision de implementacion de Codex): formato exacto del transcript que reproduce el
  `RecordedInvoker` para el replay comparativo. Proponer en el handoff; mantener determinista y sin red.

## Dogfood
Aplica liveness (senal por turno) + handoff-release (libera claim al pasar a in_review, commitea WIP
antes). ASCII-only en mailbox/state (DECISION-0012). El gate de coordinacion completo (encoding,
handoff-release, liveness, mailbox-status, poda) ya protege este trabajo.
