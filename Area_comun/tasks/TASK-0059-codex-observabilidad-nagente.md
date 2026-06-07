---
id: TASK-0059
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
closed_by: Claude (ratificacion adversarial)
depends_on: [TASK-0044, TASK-0045, TASK-0046]
relates_to: [TASK-0032]
phase: P2
spec_id: Area_comun/specs/SPEC-0045-fase6.1-observabilidad-nagente.md
linked_decisions: [DECISION-0015, DECISION-0009, DECISION-0018]
execution_pipeline: [anadir trace_id DETERMINISTA por evento en runtime/eventlog.py derivado de run_id+task+attempt+seq (sin reloj/random), sin alterar el hash canonico del snapshot de forma no-determinista (excluir trace_id del hash o incluirlo determinista); anotar span {trace_id,parent,name,attrs} por transicion en el router (decision) y en review_qa (event) via run-log/evento, aditivo; extender runtime/metrics.py con summarize_nagent() post-hoc determinista que computa desde event log + run log: distribucion de routing por agente + fairness, ciclos QA por tarea, conflictos/rechazos de fencing, escalados (architect_review/blocked), exclusiones de autor I1/I2; DELTA sobre M2 (no rehacer summarize existente); crear examples/runtime_observability_nagent_cases con los casos del test plan + CI]
acceptance_criteria: [O1 trace_id por evento determinista (mismo event-log => mismos trace_id; dos corridas mismo hash) y replay reproduce el mismo hash canonico de snapshot con negative-replay (A6) intacto sin invocar red/reloj; O2 summarize_nagent() deriva metricas N-agente SOLO de logs (post-hoc), determinista (routing+fairness, ciclos QA, conflictos fencing, escalados, exclusiones autor); O4 aditivo/config-gated - sin observabilidad activa el comportamiento es BYTE-EQUIVALENTE y el fallback N=2 se preserva; DELTA sobre M2 (no rehacer summarize ni runlog existentes); los golden y la suite runtime existentes siguen verdes; sin red/reloj/random; neutralidad limpia]
test_plan: [examples/runtime_observability_nagent_cases determinista (sin red/reloj/random): (1) trace_id presente y determinista; (2) span por transicion (router decision + review/qa event) anotado; (3) summarize_nagent() correcto sobre event-log sintetico (routing/QA/conflictos/escalados/exclusiones); (4) replay con trace_id => mismo hash canonico (negative-replay safe); (5) sin observabilidad activa => byte-equivalente; suite runtime completa verde + validador/encoding/neutralidad py]
closure_criteria: [trace_id determinista por evento en eventlog.py (sin romper hash/replay/negative-replay A6); span por transicion en router + review_qa (aditivo); summarize_nagent() en metrics.py (DELTA sobre M2) con routing+fairness/ciclos QA/conflictos/escalados/exclusiones; golden runtime_observability_nagent_cases verde con los 5 casos + suite runtime completa + gates py; suite en CI; aditivo/config-gated, byte-equivalente sin activar, fallback N=2; sin red/reloj/random; neutralidad limpia; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0059 - Fase 6.1: observabilidad N-agente (trace_id/spans + metricas)

> `implementation` -> SDD. Cierra parte de D0 (motor). DELTA sobre la observabilidad del M2 (metrics.py/
> runlog.py ya existen; NO rehacerlos). Aditiva, config-gated, fallback N=2 intacto. Ver SPEC-0045. NO
> requiere DECISION nueva. Fase 6.2 (A10 budget/deadline) va aparte.

## Contexto

D0 (motor) = Fase 5.3 (done) + Fase 6. Fase 6.1 anade el DELTA N-agente de observabilidad: trace_id/spans
deterministas y metricas N-agente, sobre lo ya existente del M2 (TASK-0032). NO rehacer summarize/runlog.

## Alcance (ver SPEC-0045 sec.2)

1. **trace_id determinista por evento** en `eventlog.py` (derivado de run_id+task+attempt+seq; sin reloj/
   random; sin romper hash canonico/replay/negative-replay A6).
2. **span por transicion** en router (decision) + review_qa (event), aditivo.
3. **`summarize_nagent()`** en `metrics.py` (DELTA): routing+fairness, ciclos QA, conflictos fencing,
   escalados, exclusiones de autor (I1/I2). Post-hoc, determinista.
4. **Golden** `examples/runtime_observability_nagent_cases/` (5 casos) + CI.

## Restricciones

- **Aditivo / config-gated**; sin observabilidad activa => **byte-equivalente**; **fallback N=2**.
- **DELTA sobre M2** (no rehacer `summarize`/`runlog`).
- **Determinismo**: sin reloj/red/random; trace_id determinista; negative-replay (A6) intacto.
- **Neutralidad**; sin secretos.
- Fuera de alcance: Fase 6.2 (A10 budget/deadline), OTel externo, Fase B, Fase 7, activar runtime (gateado).
  Cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

D0: 5.3 done -> **6.1 (esta)** -> 6.2 (A10 budget). Con 6.1+6.2 el motor (D0) queda cerrado. Track de
distribucion (D2) sigue en paralelo (D2.2 pendiente). Codex autonomo (~100s): tomala cuando este ready.
