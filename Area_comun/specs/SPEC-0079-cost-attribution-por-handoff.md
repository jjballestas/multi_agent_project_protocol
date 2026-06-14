---
spec_id: SPEC-0079-cost-attribution-por-handoff
task_id: TASK-0111
type: implementation
status: accepted
linked_decisions:
  - DECISION-0033
created_at: 2026-06-14
updated_at: 2026-06-14
author: Claude (architect)
---

# SPEC-0079 - Cost-attribution por handoff/decision/agente

## Context

La medicion de coste de tokens es hoy agregada o por tope global (`runtime/budget.py`) y por
tarea/corrida post-hoc (`runtime/metrics.py`). Falta granularidad por evento. DECISION-0033 introduce
una instrumentacion aditiva, off-by-default, de DOS PLANOS (plano de protocolo sin texto libre; carga
util por hash) que imputa tokens por handoff, decision y agente, VIVA antes del piloto del loop.

## Scope

- `runtime/eventlog.py`: `cost_attribution_enabled(config)` + `EventWriter.append_cost_attribution(...)`
  que emite un evento `cost.attributed` con `applied:false` (anotacion no-mutadora), gateado por el flag.
- `runtime/budget.py`: `cost_attribution_record(...)` (constructor del registro de plano de protocolo,
  sin texto libre; subject por hash) + `cost_attribution_idempotency_key(...)` (dedup determinista) +
  `attribute_cost(writer, ...)` (helper de emision que usa el EventWriter).
- `runtime/metrics.py`: `summarize_cost_attribution(event_log_path)` que lee el event log y resume las
  tres dimensiones: `by_handoff` (cada handoff por separado, sin agregacion cruzada), `by_decision`
  (por `decision_id`), `by_agent` (suma por actor).
- `protocol.config.json` (vivo): `metrics.cost_attribution_enabled = true`.
  `protocol.config.template.json` (master): `metrics.cost_attribution_enabled = false`.
- Golden `examples/runtime_cost_attribution_cases/` + linea en CI (`.github/workflows/validate.yml`).

## Out Of Scope

PROV-AGENT (export W3C PROV), firma por agente, activacion del loop/SA.4/subagents. No se tocan
`enforce`/`authoritative`. La emision NO se cablea dentro de `submit_intent` (queda explicita en el
orquestador/wrapper al cierre de turno).

## Contrato de esquema (endurecimiento analista pasada-3, 2026-06-14)

El event log es append-only e inmutable; el formato se fija ANTES de la primera emision en caliente.

- **C1 - Subject canonico por dimension.** El `subject` se construye de UN identificador tipado por
  dimension: `handoff -> {handoff_id}`, `decision -> {decision_id}`, `agent -> {agent_id}`. Sin prosa
  ni campos variables (`to`, titulos, cuerpos). `subject_hash = canonical_hash(subject_canonico)`.
  Invariante: dos emisiones logicamente iguales (mismo dimension+subject_id) producen el MISMO
  `subject_hash` (apareamiento de H2 y `idempotency_key` estables).
- **`cost_tokens` - semantica fijada.** Es el total de tokens del **PRODUCTOR**: `input` (contexto
  ensamblado) `+ output` (generacion) gastados por `actor` al producir `subject`, **escalar
  autoreportado** (el invoker NO expone split prompt/completion). Ambos brazos del experimento (A/B)
  miden lo mismo (total del productor) => conmensurables. El `actor` es el emisor.
- **`context_tokens` - brazo input capturado AHORA** (decision del operador 2026-06-14; foco: reducir
  input-contexto; log inmutable). Es el `assembled_context_tokens` del runtime (`orchestrator.py`), un
  **proxy chars/divisor** del contexto ensamblado (input), `context_unit = context_tokens_proxy_chars_div`.
  Hoy ese valor solo vive en el run-log efimero (gitignored); se captura por handoff en el corpus
  inmutable. Es **opcional** (null si no hay contexto medido, p.ej. una decision); el split real
  prompt/completion queda como migracion futura (bumpeando `cost_schema`).
- **C2 - Tags `cost_unit` + `cost_schema`.** Toda emision los lleva en el payload. `cost_unit` por
  defecto `tokens_total`; **`cost_schema` = `"2"`** (lleva `cost_tokens` + `context_tokens`). Si la
  convencion cambia (split input/output real, o mueve la frontera productor<->consumidor), se bumpea
  `cost_schema` y el corpus historico sigue siendo interpretable. El summarizer RECHAZA filas sin
  `cost_unit`+`cost_schema` (las excluye y las cuenta en `rejected`); `units` reporta los pares
  unit/schema; `total_context_tokens` suma el brazo input (no-null).
- **C3 - `subject_hash` es SEUDONIMO, no anonimo.** Bajo RGPD (Considerando 26) / Ley 1581, un hash de
  contenido con el plano de carga util RETENIDO es dato seudonimizado y re-identificable. No filtra
  texto libre al plano de protocolo (correcto), pero NO es "publicable/anonimo". `actor` se restringe
  por esquema a un vocabulario controlado de ids de agente (no-humano); un `actor` fuera del
  vocabulario se rechaza.

## execution_pipeline

1. `eventlog.py`: anadir `COST_ATTRIBUTION_EVENT_TYPE = "cost.attributed"`,
   `COST_ATTRIBUTION_DIMENSIONS = {"handoff","decision","agent"}`, `cost_attribution_enabled(config)`
   (lee `config["metrics"]["cost_attribution_enabled"] is True`) y el metodo
   `EventWriter.append_cost_attribution(*, dimension, actor_id, subject_hash, cost_tokens,
   subject_seq=None, task_id=None, decision_id=None, idempotency_key=None, ts=None)`: si el flag esta
   off devuelve `None` (no escribe); si on, `append_event(type="cost.attributed", applied=False, ...)`.
2. `budget.py`: `cost_attribution_record(...)` valida la dimension, deriva `subject_hash`
   (`canonical_hash(subject)` si no es ya un sha256 hex de 64), construye el dict estructurado SIN texto
   libre; `cost_attribution_idempotency_key(record)` determinista; `attribute_cost(writer, *, ...)`
   construye el registro y delega en `append_cost_attribution`.
3. `metrics.py`: `summarize_cost_attribution(event_log_path)` filtra `type=="cost.attributed"`, acumula
   `by_handoff` (lista ordenada por `(seq, subject_hash)`, una entrada por handoff), `by_decision`
   (suma por `decision_id`), `by_agent` (suma por `actor`), `total_cost_tokens`, `attributions`.
4. Config: flag vivo `true`, template `false`; ausencia => `false`.
5. Golden con los casos (a)/(b)/(c) + off-by-default byte-equivalente + drift no-afectado.
6. CI: linea que corre el golden.

## acceptance_criteria

- **Determinista:** misma entrada => misma imputacion (golden estable).
- **(a)** un handoff simple imputado al agente correcto (`by_handoff[0].actor` y `by_agent`).
- **(b)** varios handoffs en una corrida SIN agregacion cruzada (cada uno entrada separada en
  `by_handoff`); `by_agent` suma por agente (vista de la dimension agente).
- **(c)** caso por decision en `by_decision`.
- **Off-by-default:** con el flag en `false`, `append_cost_attribution` no escribe; el event log queda
  byte-equivalente; las transiciones normales por `submit_intent` quedan byte-identicas.
- **Sin regresion** en `intent_flow`, `runtime_budget`, `runtime_observability_nagent` ni en el
  hard-gate (`enforce`: `enforced=True`, `has_drift=False`).
- **Plano de protocolo sin texto libre:** el evento `cost.attributed` solo contiene la metrica e
  identificadores estructurados; el contenido se referencia por `subject_hash`.
- **(C1)** dos emisiones logicamente iguales (mismo dimension+subject_id) => mismo `subject_hash`;
  distinto subject_id => distinto hash.
- **(C2)** toda emision lleva `cost_unit`+`cost_schema`; el summarizer rechaza (no suma) las filas sin
  ambos y las cuenta en `rejected`.
- **(C3)** `actor` fuera del vocabulario de agentes se rechaza; `subject_hash` documentado como
  seudonimo (no anonimo).
- **(C4)** byte-equivalencia con flag off sobre un log POBLADO (no solo vacio); caso EN CALIENTE que
  asierta que lo registrado == un conteo de tokens medido de forma independiente (no un literal).

## linked_decisions

- `DECISION-0033`: define el cambio, el esquema de dos planos y la activacion off-by-default.
- `DECISION-0022`: el evento `cost.attributed` es `applied:false` (no muta estado, no pasa por
  `submit_intent`); el escritor unico de estado queda intacto.
- `DECISION-0030`: patron de activacion en la instancia viva (template off, vivo on).

## test_plan

- `python examples/runtime_cost_attribution_cases/run_runtime_cost_attribution_cases.py` (todos verdes).
- Regresion: `python examples/intent_flow_cases/run_intent_flow_cases.py`,
  `python examples/runtime_budget_cases/run_runtime_budget_cases.py`,
  `python examples/runtime_observability_nagent_cases/run_runtime_observability_nagent_cases.py`,
  `python examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py`.
- Gates: `python scripts/validate_collaboration_state.py --root .`;
  `python scripts/scan_encoding.py --root .`; `python scripts/scan_domain_neutrality.py` (o equivalente).
- Casos de endurecimiento: subject canonico (dos emisiones iguales => mismo hash), rechazo de filas sin
  `cost_unit`/`cost_schema`, vocabulario de `actor`, byte-equivalencia sobre log poblado, caso en
  caliente `recorded == measure_tokens(input)` (no literal).
- EN CALIENTE: con el flag activo, emitir una imputacion real para un evento existente del event log y
  leerla con `summarize_cost_attribution`; `protocol_state_drift` `has_drift=False`, replay==hot.

## closure_criteria

- Golden verde + regresion sin romper + gates verdes (drift 0) + evidencia de captura EN CALIENTE
  (imputacion leida del event log, no calculada despues). Ratificacion del implementer (Codex).

## Risks

- **Riesgo:** el evento nuevo rompe el replay/drift. **Mitigacion:** `applied:false` => omitido por el
  replay de estado de protocolo (verificado en el golden de drift no-afectado).
- **Riesgo:** texto libre del handoff filtrado al plano de protocolo. **Mitigacion:** el constructor
  solo acepta campos estructurados + `subject_hash`; el golden lo verifica.
- **Riesgo:** cambia el comportamiento con el flag off. **Mitigacion:** caso byte-equivalente en el golden.

## Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Imputacion por handoff (a) | TASK-0111 | `case_single_handoff_attributed_to_agent` | by_handoff+by_agent correctos |
| Varios handoffs sin agregacion cruzada (b) | TASK-0111 | `case_multiple_handoffs_no_cross_aggregation` | entradas separadas |
| Imputacion por decision (c) | TASK-0111 | `case_decision_attribution` | by_decision correcto |
| Off-by-default byte-equivalente | TASK-0111 | `case_disabled_byte_equivalent` | event log byte-identico |
| Drift no-afectado | TASK-0111 | `case_drift_unaffected` | has_drift=False, replay==hot |
