---
spec_id: SPEC-0048-wrapper-llm-real
task_id: TASK-0062
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0021, DECISION-0009, DECISION-0015, DECISION-0019]
relates_to: [SPEC-0035, SPEC-0036]
---

> SPEC del wrapper LLM real (adapter CLI concreto) - bloque funcional de v1.0 (operador). Autorizada por
> DECISION-0021 (politica de activacion, aprobada por el operador). DELTA sobre el adapter ya existente
> (runtime/adapters/: RecordedInvoker + SubprocessInvoker + LLMAdapter); NO rehacer. Aditiva, off-by-default,
> vendor-neutral, sin secretos.

# SPEC-0048 - Wrapper LLM real (adapter CLI concreto)

## 1. Linea base (NO rehacer)

`runtime/adapters/llm_adapter.py` ya tiene: `RecordedInvoker` (CI/tests, recorded_invoker.v1),
`SubprocessInvoker` (real, gateado, from_command Windows-safe), `LLMAdapter`. El invoker real generico y su
gating ya existen (TASK-0036/0039).

## 2. Alcance (TASK-0062) = DELTA wrapper

1. **Adapter CLI concreto vendor-neutral:** un helper/preset (sobre `SubprocessInvoker`) que mapea un CLI
   nombrado a un `llm-command` (ejemplos para `claude` y `codex` como presets/ejemplos, NO hardcode unico).
   El prompt se construye con `build_prompt` existente; el reporte de turno vuelve por el contrato actual.
2. **Activacion per DECISION-0021:** off por defecto; el wrapper solo ejecuta el CLI real con
   `runtime.enabled=true` + `--allow-real-invoker` + `--llm-command` + `--once` + registro de activacion;
   sin esos => no ejecuta (default replay/recorded). Los limites (budget A10, tool-policy, guardrails) se
   aplican en la ruta de apply/gate ya existente.
3. **Golden `examples/runtime_real_adapter_cases/`** (CI con RecordedInvoker, sin red/credenciales):
   - sin flags => NO ejecuta el CLI real (gated; default recorded/replay).
   - replay-comparativo: RecordedInvoker reproduce el mismo turn report (determinista).
   - con activacion simulada (RecordedInvoker como stand-in del CLI) => el turno pasa por apply/gate con los
     limites (budget/tool-policy/guardrails) aplicados; sin secretos.
   - vendor-neutral: el preset claude y el preset codex producen el mismo cableado generico.
4. **Docs minimas de operacion real** (el grueso entra en D2.3): como activar de forma segura.

## 3. Invariantes

- **W1:** off-by-default; sin los flags de DECISION-0021 el wrapper NO invoca CLI real (default recorded/
  replay); byte-equivalente a hoy.
- **W2:** vendor-neutral (config `llm-command`/preset, no hardcode); sin secretos en el repo (CI con
  RecordedInvoker).
- **W3:** al activar, los limites (budget A10, tool-policy deny-by-default, guardrails anti-inyeccion, 1
  commit/turno + gate) se aplican; replay-comparativo determinista.
- **W4:** NO autonomia (1 agente real por turno bajo gate; loop autonomo sigue post-v1.0).

## 4. Tests (golden determinista, CI sin red/credenciales)

1. sin flags => no ejecuta CLI real (gated).
2. replay-comparativo: RecordedInvoker => turn report determinista (== esperado).
3. activacion simulada (RecordedInvoker stand-in) => apply/gate aplica limites; sin secretos.
4. vendor-neutral: presets claude/codex => mismo cableado generico.

## 5. Fuera de alcance

- Loop autonomo multi-turno sin humano (post-v1.0, gateado). Credenciales reales / red en CI (nunca).
- D2.3 docs completas, D2.4 SemVer. Fase B, Fase 7. Cambio incompatible => blocked + DECISION.

## 6. SemVer: MINOR (adapter aditivo, off-by-default; comportamiento actual preservado).
