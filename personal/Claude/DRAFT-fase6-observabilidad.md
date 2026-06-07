# BORRADOR (personal) - Fase 6: observabilidad + presupuesto N-agente (DELTA sobre M2)

> Borrador privado (personal/Claude/, no reclamable por Codex). Se promueve a Area_comun cuando Codex
> libere TASK-0058 (ahora tiene el ledger). Cierra D0 (motor): Fase 5.3 ya done; falta Fase 6. Confirmado
> por el operador: Fase 6 N-agente es el DELTA sobre lo que ya existe del M2, NO rehacerlo. IDs reservados:
> SPEC-0045, TASK-0059 (6.1), TASK-0060 (6.2).

## Linea base existente (M2, NO rehacer)
- `runtime/runlog.py`: turn_entry con campo `trace` (lista por turno, M1: gate_pre..commit) + run_id determinista.
- `runtime/metrics.py`: summarize() post-hoc de 1 run-log: turns, gates_green_pct, reverts, collisions_avoided,
  cost_total/per_task, duration. NO tiene metricas N-agente (routing/QA/conflictos/escalados).
- `runtime/budget.py`: Budget(max_iter, max_cost_tokens) caps DUROS. NO tiene umbral blando, deadline,
  limite de cola, ni escalado con consumido/limite/responsable (A10 NO cubierto).
- eventlog/router/review_qa: SIN trace_id/span.

## Alcance Fase 6 = DELTA (criterios 12-13 SPEC-0038 + addenda A10)

### Rebanada 6.1 (TASK-0059): trace_id/spans + metricas N-agente
1. **trace_id por evento** en `runtime/eventlog.py` (aditivo): id DETERMINISTA derivado de run_id+task+
   attempt+seq (sin reloj/random; preserva replay y negative-replay A6). **span por transicion**: el router
   (decision) y la maquina review/qa (event) anotan un span {trace_id, parent, name, attrs} en el run-log/
   evento. Aditivo: sin observabilidad activa el comportamiento es byte-equivalente.
2. **Metricas N-agente** en `runtime/metrics.py` (extender, aditivo): `summarize_nagent()` que computa desde
   el event log + run log: distribucion de routing por agente (+ fairness), ciclos QA por tarea, conflictos/
   rechazos de fencing, escalados (architect_review/blocked), exclusiones autor (I1/I2). Post-hoc,
   determinista.
3. **Golden** `examples/runtime_observability_nagent_cases/`: trace_id presente y determinista (mismo log =>
   mismos trace_id), span por transicion, metricas correctas sobre un event-log sintetico; replay con
   trace_id reproduce mismo hash canonico (la firma/snapshot NO incluye trace_id volatil, o lo incluye de
   forma determinista). + CI.

### Rebanada 6.2 (TASK-0060): A10 budget/deadline con escalado
1. **Extender `runtime/budget.py`** (aditivo, config-gated): umbral BLANDO (warning) + DURO
   (`budget_exhausted` + escalado con payload consumido/limite/ultimo-responsable); **deadline por tarea**
   independiente de tokens; **limite de longitud de cola**. Tokens y deadline independientes (A10).
2. **Determinismo del deadline:** logico (presupuesto de turnos/intentos por tarea) o timestamp INYECTADO
   (no wall-clock) para preservar replay. Wall-clock real queda gateado.
3. **Cableado**: el orchestrator/loop consulta el budget; excedido blando => warning en run-log; duro =>
   evento de escalado + parada/gate. **Golden** `examples/runtime_budget_cases/`: blando=>warning,
   duro=>budget_exhausted+escalado, deadline excedido=>escalado, cola excedida=>rechazo/escalado. + CI.

## Invariantes
- O1: trace_id por evento determinista; replay reproduce mismo hash canonico (negative-replay A6 intacto).
- O2: metricas N-agente derivadas SOLO de logs (post-hoc), deterministas, sin red/reloj.
- O3 (A10): budget con umbral blando+duro, deadline independiente, limite de cola; escalado con
  consumido/limite/responsable; sin escalado oculto.
- O4: aditivo/config-gated; sin observabilidad/budget activos => byte-equivalente; fallback N=2 intacto.

## Fuera de alcance
- OTel/exporters externos (queda fuera; A12 dice trace_id/run_id + run-logs estructurados en el nucleo, el
  resto de OTel en fase posterior). Wall-clock real para deadline (gateado). Fase B, Fase 7.
- Cambio incompatible de contrato => blocked + DECISION.

## SemVer: MINOR (observabilidad + budget aditivos, config-gated, default off => comportamiento actual).

## Secuencia / nota
Cierra D0 (motor). 6.1 (observabilidad) -> 6.2 (A10 budget). Se promueven de a una via metodo anti-colision
(Codex tiene D2.1 ahora; promover cuando libere). D2 (distribucion) sigue en paralelo; cuando Fase 6 aterrice,
el motor distribuido por el tier runtime ya la incluye (templates). Criterio 13 SPEC-0038 cerrado con 6.2.
