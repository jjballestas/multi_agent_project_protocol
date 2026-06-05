---
id: TASK-0027
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0026]
relates_to: []
phase: P2
spec_id: Area_comun/specs/SPEC-0026-contrato-de-turno.md
linked_decisions: [DECISION-0009, DECISION-0007, DECISION-0001]
execution_pipeline: [runtime/ skeleton (orchestrator/router/context) sin invocar agentes, Validador de turn report contra runtime/turn_schema.json + checks semanticos (write-allowlist, anti-carrera), Router determinista select_next(state) contra SPEC-0027, Comando --plan (dry-run) que lista la proxima jugada sobre el dogfood SIN mutar, Golden de router + golden semanticos de turno, Bloque runtime en protocol.config(.template) enabled:false + runtime/** en scan_globs]
acceptance_criteria: [--plan lista jugadas correctas sobre el dogfood sin mutar estado, turn report validado por esquema + rechazo si changed_paths fuera de claim o from desfasado, router determinista (mismo estado => misma jugada) respeta claims/deps, runtime enabled:false => comportamiento actual intacto, runtime/** neutral (scan verde), paridad no aplica (python)]
test_plan: [Golden runtime_turn_cases (esquema) + nuevos golden de router y semanticos, --plan sobre root sin diffs, validador y scan verdes]
closure_criteria: [Skeleton + --plan + validador de turno + router deterministas, golden pasan, estado no mutado por --plan, handoff con evidencia, claim liberado]
---

# TASK-0027 — Runtime M0 (impl): skeleton + --plan + validador de turno + router

> `implementation` → SDD; implementar contra [SPEC-0026](../specs/SPEC-0026-contrato-de-turno.md) y
> [SPEC-0027](../specs/SPEC-0027-router-determinista.md) y DECISION-0009. **Dry-run primero**: `--plan`
> planifica sin invocar agentes ni mutar estado. Opt-in/off-by-default. `runtime/**` entra a scan_globs.
> Reclamar antes de tocar `runtime/` y `protocol.config` (DECISION-0007).

## Resumen
Primer entregable ejecutable del runtime (DECISION-0009): planifica y valida turnos de forma
determinista y segura, **sin** invocar agentes todavía (eso es M1). Diseño base ya emitido por
TASK-0026: `runtime/turn_schema.json` + SPEC-0026/0027 + golden `examples/runtime_turn_cases/`.

## archivos objetivo (previstos)
- `runtime/orchestrator.py`, `runtime/router.py`, `runtime/context.py`, `runtime/turn_validate.py`
- `protocol.config.template.json` (+ live): bloque `runtime` (`enabled:false`)
- `examples/runtime_turn_cases/` (router + semanticos)
