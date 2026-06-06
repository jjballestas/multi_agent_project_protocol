---
handoff_id: HANDOFF-TASK-0052-codex-to-claude-1
task_id: TASK-0052
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-06
context_refs:
  - Area_comun/tasks/TASK-0052-codex-concurrency-simulation.md
  - examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py
  - .github/workflows/validate.yml
---

# Handoff TASK-0052 - concurrency simulation

## Entrega

- Nuevo harness `examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py`.
- Simulacion determinista declarada:
  - seed: `concurrency-v1`;
  - 10 implementadores (`Impl01`..`Impl10`);
  - 100 tareas (`TASK-6001`..`TASK-6100`);
  - disable determinista en la tarea 50 para `Impl09` y `Impl10`;
  - colisiones en indices 3, 17, 41, 63 y 88;
  - lease re-claim en indices 11, 37 y 72;
  - retry duplicado para cada intent aplicado.
- Reutiliza runtime real:
  - `runtime.router.select_next` para asignaciones;
  - `runtime.router.evaluate_fairness` para fairness;
  - `runtime.eventlog.EventWriter`, `rebuild_snapshot`, `assert_snapshot_matches`;
  - `runtime.turn_validate.validate_turn` en muestras 0, 50 y 99.
- Runner agregado a `.github/workflows/validate.yml`.

## Metricas del harness

Ultima corrida:

- asignaciones: `{'Impl01': 11, 'Impl02': 11, 'Impl03': 12, 'Impl04': 11, 'Impl05': 11, 'Impl06': 11, 'Impl07': 12, 'Impl08': 11, 'Impl09': 5, 'Impl10': 5}`;
- colisiones: 5;
- lease reclaims: 3;
- stale fencing rejections: 8;
- dedups: 100;
- applied_intents: 100;
- fairness_ratio: 2.4;
- max_weighted_share_delta: 0.007499999999999993;
- snapshot_hash estable: `6fc1d50083e87fb33362860772f39359d911db0a35e53e687fc27f321fbd397a`.

Dos corridas consecutivas dieron las mismas metricas y el mismo hash.

## Limites respetados

- No se modifico `runtime/`.
- No se modifico contrato ni golden existentes.
- No se arranco Fase B ni Fase 5.
- Sin red, sin random y sin decisiones basadas en reloj.
- Release atomico aplicado: este handoff, mensaje a Claude, status `in_review` y claim liberado en el mismo cierre.

## Validacion ejecutada

- `python examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py`
- Runtime completo: 105/105 verde.
  - concurrency simulation 1/1
  - property 26/26
  - N-agent 6/6
  - router 10/10
  - eventlog 5/5
  - eventlog gate 5/5
  - Review/QA 15/15
  - agent registry 4/4
  - turn schema 5/5
  - turn semantic 5/5
  - apply 4/4
  - loop 8/8
  - observability 5/5
  - LLM adapter 6/6
- Validadores/gates:
  - `python scripts/validate_collaboration_state.py --root .`
  - `python scripts/validate_collaboration_state.py --root examples/minimal_instance`
  - `./scripts/validate_collaboration_state.ps1 -Root .`
  - `./scripts/validate_collaboration_state.ps1 -Root examples/minimal_instance`
  - `python scripts/scan_encoding.py --root .`
  - `./scripts/scan_encoding.ps1 -Root .`
  - `python scripts/scan_domain_neutrality.py --root .`
  - `./scripts/scan_domain_neutrality.ps1 -Root .`
  - `python examples/encoding_gate_cases/run_encoding_gate_cases.py`
  - `python examples/handoff_release_cases/run_handoff_release_cases.py`
  - `python examples/mailbox_status_cases/run_mailbox_status_cases.py`
  - `python scripts/prune_state.py --root . --check`
  - `./examples/sdd_validation_cases/run_sdd_cases.ps1`
  - `./examples/compact_comms_validation_cases/run_compact_comms_cases.ps1`
  - `./examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1`
  - YAML parse of `.github/workflows/validate.yml`
  - `git diff --check`

## Revision sugerida

- Verificar que el harness cubre el test plan 15.5: colisiones, leases/fencing, disabled mid-run, retries duplicados.
- Confirmar que el diff de implementacion queda limitado a `examples/runtime_concurrency_cases/` y CI.
- Ratificar o devolver hallazgos concretos.
