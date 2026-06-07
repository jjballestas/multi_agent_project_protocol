---
id: TASK-0060
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0059]
relates_to: [TASK-0032]
phase: P2
spec_id: Area_comun/specs/SPEC-0046-fase6.2-budget-deadline.md
linked_decisions: [DECISION-0015, DECISION-0009, DECISION-0018]
execution_pipeline: [extender runtime/budget.py (DELTA sobre Budget existente, no rehacer) con umbral BLANDO (warning, no detiene) y DURO (budget_exhausted + payload de escalado con consumed/limit/last_responsible); anadir deadline por tarea independiente de tokens, DETERMINISTA (logico = presupuesto de turnos/intentos, o timestamp INYECTADO por parametro; NO wall-clock); anadir limite de longitud de cola (excede => rechazo/escalado registrado); cablear aditivo y config-gated en orchestrator/loop (config.budget o runtime.budget; off/ausente => comportamiento actual): blando => warning en run-log, duro/deadline/cola => evento de escalado + parada/gate; crear examples/runtime_budget_cases con los casos del test plan + CI]
acceptance_criteria: [B1 A10 - umbral blando (warning) y duro (budget_exhausted + escalado con consumed/limit/last_responsible); tokens y deadline INDEPENDIENTES; limite de cola; sin escalado oculto; B2 determinismo - deadline logico o inyectado (sin wall-clock), replay/negative-replay (A6) intacto, sin red/reloj/random; B3 aditivo/config-gated - budget off/ausente => BYTE-EQUIVALENTE y fallback N=2 preservado; DELTA sobre M2 (no rehacer Budget existente); golden y suite runtime existentes verdes; neutralidad limpia]
test_plan: [examples/runtime_budget_cases determinista (sin reloj/red): (1) consumo bajo umbral blando => warning, no detiene; (2) consumo >= umbral duro => budget_exhausted + escalado con consumed/limit/last_responsible; (3) deadline (logico/inyectado) excedido => escalado; (4) cola excede limite => rechazo/escalado registrado; (5) budget off/ausente => byte-equivalente; suite runtime completa verde + validador/encoding/neutralidad py]
closure_criteria: [budget.py extendido (umbral blando/duro + deadline determinista + limite de cola + escalado con consumed/limit/last_responsible) DELTA sobre M2; cableado aditivo config-gated en orchestrator/loop; golden runtime_budget_cases verde con los 5 casos + suite runtime completa + gates py; suite en CI; aditivo/config-gated byte-equivalente sin activar, fallback N=2; determinismo (sin wall-clock), negative-replay A6 intacto; neutralidad limpia; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0060 - Fase 6.2: presupuesto y deadline con escalado (A10)

> `implementation` -> SDD. Cierra D0 (motor) junto con 6.1. DELTA sobre budget.py del M2 (Budget con caps
> duros ya existe; NO rehacer, extender). Aditiva, config-gated, fallback N=2 intacto. Ver SPEC-0046. NO
> requiere DECISION nueva. Cierra el criterio 13 de SPEC-0038.

## Contexto

`runtime/budget.py` ya tiene Budget(max_iter, max_cost_tokens) con caps duros. Falta A10: umbral blando/duro,
deadline independiente, limite de cola, escalado con detalle. Esta tarea anade ese DELTA.

## Alcance (ver SPEC-0046 sec.2)

1. **Umbral blando + duro** en Budget (blando=warning; duro=budget_exhausted + escalado consumed/limit/
   last_responsible).
2. **Deadline por tarea** independiente de tokens, DETERMINISTA (logico o inyectado; NO wall-clock).
3. **Limite de longitud de cola** (excede => rechazo/escalado registrado).
4. **Cableado aditivo config-gated** en orchestrator/loop (config.budget off/ausente => comportamiento actual).
5. **Golden** `examples/runtime_budget_cases/` (5 casos) + CI.

## Restricciones

- **DELTA sobre M2** (no rehacer Budget); **aditivo/config-gated**; budget off => **byte-equivalente**; **fallback N=2**.
- **Determinismo**: deadline logico/inyectado, sin wall-clock; **negative-replay (A6) intacto**; sin red/reloj/random.
- **Neutralidad**; sin secretos.
- Fuera de alcance: wall-clock real (gateado), OTel externo, Fase B, Fase 7, activar runtime (gateado).
  Cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

D0: 5.3 done -> 6.1 done -> **6.2 (esta)**. Con 6.2 el motor (D0) queda CERRADO (criterio 13 SPEC-0038).
Siguiente en v1.0: D2.2 (upgrade tier-aware) -> wrapper LLM real -> D2.3 docs -> D2.4 SemVer -> release.
Codex autonomo (~100s): tomala cuando este ready.
