---
id: TASK-0062
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0036, TASK-0039]
relates_to: [TASK-0056, TASK-0060]
phase: P2
spec_id: Area_comun/specs/SPEC-0048-wrapper-llm-real.md
linked_decisions: [DECISION-0021, DECISION-0009, DECISION-0015, DECISION-0019]
execution_pipeline: [anadir en runtime/adapters/ un helper/preset CLI concreto vendor-neutral (DELTA sobre SubprocessInvoker existente, no rehacer) que mapee un CLI nombrado a un llm-command (presets ejemplo claude y codex, sin hardcode unico); respetar la activacion de DECISION-0021 (off por defecto; solo ejecuta CLI real con runtime.enabled=true + --allow-real-invoker + --llm-command + --once + registro; sin esos => default recorded/replay); asegurar que al activar se apliquen los limites ya existentes (budget A10, tool-policy deny-by-default, guardrails anti-inyeccion, 1 commit/turno + gate) en la ruta apply/gate; crear examples/runtime_real_adapter_cases (CI con RecordedInvoker, sin red/credenciales) con los casos del test plan + CI; docs minimas de operacion real (el grueso va en D2.3)]
acceptance_criteria: [W1 off-by-default - sin los flags de DECISION-0021 el wrapper NO invoca CLI real (default recorded/replay), byte-equivalente; W2 vendor-neutral (config llm-command/preset, no hardcode claude) y sin secretos en el repo (CI con RecordedInvoker, sin red/credenciales); W3 al activar se aplican budget A10 + tool-policy deny-by-default + guardrails anti-inyeccion + 1 commit/turno + gate; replay-comparativo determinista (RecordedInvoker reproduce el mismo turn report); W4 NO autonomia (1 agente real por turno bajo gate); DELTA sobre runtime/adapters (no rehacer RecordedInvoker/SubprocessInvoker/LLMAdapter); golden y suite existentes verdes; neutralidad limpia]
test_plan: [examples/runtime_real_adapter_cases determinista (CI sin red/credenciales): (1) sin flags => no ejecuta CLI real (gated); (2) replay-comparativo: RecordedInvoker => turn report determinista == esperado; (3) activacion simulada (RecordedInvoker stand-in) => apply/gate aplica limites (budget/tool-policy/guardrails), sin secretos; (4) vendor-neutral: presets claude/codex => mismo cableado generico; suite runtime completa verde + validador/encoding/neutralidad py]
closure_criteria: [helper/preset CLI concreto vendor-neutral sobre SubprocessInvoker (DELTA, no rehacer); activacion per DECISION-0021 (off por defecto; flags + registro para ejecutar real; sin flags => recorded/replay); limites aplicados al activar (budget/tool-policy/guardrails/gate); golden runtime_real_adapter_cases verde con los 4 casos + suite + gates py; suite en CI (RecordedInvoker, sin red/credenciales); off-by-default byte-equivalente; vendor-neutral, sin secretos; NO autonomia; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0062 - Wrapper LLM real (adapter CLI concreto)

> `implementation`/security -> SDD. Bloque funcional de v1.0 (operador). Autorizada por DECISION-0021
> (politica de activacion, aprobada por el operador 2026-06-07). DELTA sobre runtime/adapters existente
> (RecordedInvoker/SubprocessInvoker/LLMAdapter); NO rehacer. Aditiva, off-by-default, vendor-neutral,
> sin secretos. Ver SPEC-0048.

## Contexto

El invoker real generico ya existe (TASK-0036/0039). Falta un adapter CLI concreto vendor-neutral + el
cableado de la activacion de DECISION-0021 (off por defecto, opt-in/gateada/supervisada). NO incluye
autonomia (1 agente real por turno bajo gate).

## Alcance (ver SPEC-0048 sec.2)

1. **Adapter CLI concreto vendor-neutral** en `runtime/adapters/` (preset claude + codex como ejemplos
   sobre SubprocessInvoker; sin hardcode unico).
2. **Activacion per DECISION-0021**: off por defecto; ejecuta CLI real solo con runtime.enabled=true +
   --allow-real-invoker + --llm-command + --once + registro; sin esos => recorded/replay.
3. **Limites al activar** (ya construidos): budget A10, tool-policy deny-by-default, guardrails, 1 commit/
   turno + gate.
4. **Golden** `examples/runtime_real_adapter_cases/` (CI con RecordedInvoker, sin red/credenciales) + docs
   minimas de operacion.

## Restricciones

- **DELTA** (no rehacer adapters); **off-by-default** byte-equivalente; **vendor-neutral**; **sin secretos**
  (CI con RecordedInvoker, sin red/credenciales).
- **NO autonomia** (1 agente real por turno bajo gate; loop autonomo post-v1.0).
- **Neutralidad**; determinismo (replay-comparativo).
- Fuera de alcance: D2.3 docs completas, D2.4 SemVer, Fase B/7, autonomia. Cambio incompatible => `blocked`
  + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

v1.0: D0 done, D2.1+D2.2 done -> **wrapper LLM real (esta)** -> D2.3 docs -> D2.4 SemVer -> DECISION-0020 +
fix prune -> release v1.0. Codex autonomo (~100s): tomala cuando este ready.
