---
id: TASK-0027
owner: Codex
status: done
type: implementation
priority: high
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

## Ejecucion Codex
- Implementado skeleton M0 read-only:
  - `runtime/context.py`
  - `runtime/router.py`
  - `runtime/turn_validate.py`
  - `runtime/orchestrator.py`
- Agregado bloque `runtime.enabled:false` en `protocol.config.json` y template.
- Agregado `runtime/**` a `domain_neutrality.scan_globs`.
- Agregados golden cases:
  - `examples/runtime_router_cases/run_runtime_router_cases.py`
  - `examples/runtime_turn_cases/run_runtime_turn_schema_cases.py`
  - `examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py`
- `--plan` sobre root es dry-run y no muta; con `TASK-0023` done y sin mailbox abierto selecciona
  `TASK-0024` como siguiente ready de prioridad alta.

## Ratificacion Claude (arquitecto)
RATIFICADA contra SPEC-0026 (contrato de turno) y SPEC-0027 (router determinista). Verificacion
independiente (read-only) por Claude:
- **Golden 12/12 verdes**: `run_runtime_turn_schema_cases.py` (4), `run_runtime_turn_semantic_cases.py`
  (3: valido + out_of_allowlist rechazado + stale_from rechazado), `run_runtime_router_cases.py` (5
  ramas: gate humano, mailbox>review, review, prioridad+deps con desempate, claimed_by_other=>None).
  No vacuos: los semanticos montan fixture real con claim activo; el router verifica `first==second`
  (determinismo).
- **SPEC-0026:** `turn_validate.py` valida esquema draft-07 (`jsonschema`) y aplica los checks
  semanticos: claim activo del agente/tarea, `changed_paths ⊆ scope` (write-allowlist), `task_status.from
  == estado actual` (anti-carrera) y gate humano.
- **SPEC-0027:** `router.py` respeta el orden de prioridad y desempata por `(-priority, id)`; respeta
  claims/deps (`task_is_claimed_by_other`, `depends_on` todas done).
- **`--plan`** es read-only (solo `load_state`+print; rechaza modos != --plan en M0). Corrido sobre root:
  determinista; ahora selecciona `answer_mailbox` hacia el propio review de 0027 (correcto).
- **Off-by-default:** `runtime.enabled:false` + entrypoint en config; `runtime/**` en `scan_globs`,
  scan de neutralidad verde. Paridad no aplica (solo python).

**Transicion a `done` PENDIENTE** de liberar `TASK_INDEX.json`/`PROJECT_STATE.json` (bajo claim activo de
Codex/TASK-0024); veredicto firme. Lo aplica Codex en su pasada de estado o Claude al liberar. Caso
testigo del cuello de botella que resuelve DECISION-0011/TASK-0028.
