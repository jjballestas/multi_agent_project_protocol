---
spec_id: SPEC-0046-fase6.2-budget-deadline
task_id: TASK-0060
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0015, DECISION-0009, DECISION-0018]
relates_to: [SPEC-0038, SPEC-0045]
---

> SPEC de la Fase 6.2 (A10 budget/deadline) - cierra D0 (motor) junto con 6.1. DELTA sobre budget.py del M2
> (Budget con caps duros ya existe; NO rehacer, extender). Aditiva, config-gated, fallback N=2. Cierra el
> criterio 13 de SPEC-0038. NO requiere DECISION nueva.

# SPEC-0046 - Fase 6.2: presupuesto y deadline con escalado (A10)

## 1. Linea base (M2, NO rehacer)

`runtime/budget.py` -> `Budget(max_iter, max_cost_tokens)` con `consume()`/`exceeded()` (caps DUROS, reason
max_iter/max_cost_tokens). SIN umbral blando, deadline, limite de cola, ni escalado con detalle.

## 2. Alcance (TASK-0060) = A10

1. **Umbral blando + duro** (extender Budget, aditivo): umbral BLANDO => warning (no detiene); umbral DURO =>
   `budget_exhausted` + evento/payload de escalado con `consumed`, `limit`, `last_responsible` (agente/tarea).
2. **Deadline por tarea** independiente de tokens. **DETERMINISTA**: deadline LOGICO (presupuesto de turnos/
   intentos por tarea) o timestamp INYECTADO via parametro (NO wall-clock) para preservar replay/negative-replay.
   Wall-clock real queda gateado/fuera.
3. **Limite de longitud de cola** (A10): si la cola de tareas/intentos supera el limite => rechazo/escalado
   registrado.
4. **Cableado** (aditivo, config-gated): el orchestrator/loop consulta el budget; blando => warning en run-log;
   duro/deadline/cola => evento de escalado + parada/gate. `config.budget` (o `runtime.budget`) off/ausente =>
   comportamiento actual.

## 3. Invariantes

- **B1 (A10):** umbral blando (warning) y duro (`budget_exhausted` + escalado con consumed/limit/responsable);
  tokens y deadline independientes; limite de cola. Sin escalado oculto.
- **B2:** determinismo: deadline logico/inyectado (sin wall-clock); replay/negative-replay (A6) intacto.
- **B3:** aditivo/config-gated; budget off/ausente => byte-equivalente; fallback N=2 intacto.

## 4. Tests (golden examples/runtime_budget_cases, determinista, sin reloj/red)

1. consumo bajo umbral blando => warning, NO detiene.
2. consumo >= umbral duro => `budget_exhausted` + escalado con consumed/limit/last_responsible.
3. deadline (logico/inyectado) excedido => escalado.
4. cola excede el limite => rechazo/escalado registrado.
5. budget off/ausente => byte-equivalente (suite existente verde, fallback N=2). + CI.

## 5. Fuera de alcance

- Wall-clock real para deadline (gateado). OTel externo. Fase B, Fase 7. Activar el runtime (gateado).
- Cambio incompatible de contrato => blocked + DECISION.

## 6. SemVer: MINOR (budget/deadline aditivos, config-gated, default off => comportamiento actual).

## 7. Cierre de D0

Con 6.1 (observabilidad) + 6.2 (este, A10 budget/deadline) el motor (D0) queda CERRADO y el criterio 13 de
SPEC-0038 cubierto. Siguiente en v1.0: D2.2 (upgrade tier-aware) -> wrapper LLM real -> D2.3 docs -> D2.4 SemVer.
