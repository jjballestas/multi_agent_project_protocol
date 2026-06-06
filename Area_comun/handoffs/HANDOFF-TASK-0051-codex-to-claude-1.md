---
handoff_id: HANDOFF-TASK-0051-codex-to-claude-1
task_id: TASK-0051
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-06
context_refs:
  - Area_comun/tasks/TASK-0051-codex-property-based-i1-i8.md
  - examples/runtime_property_cases/run_runtime_property_cases.py
  - .github/workflows/validate.yml
---

# Handoff TASK-0051 - property-based I1-I8

## Entrega

- Nuevo harness `examples/runtime_property_cases/run_runtime_property_cases.py`.
- El harness genera 26 muestras deterministas enumeradas por construccion, con seeds estables
  `property-001`..`property-026` para contraejemplos reproducibles.
- Cobertura declarada:
  - rosters N=2, N=3 y N=5;
  - transiciones `review`, `qa` y `execute`;
  - claims validos sin duplicados y un intento negativo de doble claim activo;
  - secuencias de `eventlog` para `execute`, `review`, `qa`, doble claim, replay hash,
    actor/actor_auth, e intent duplicado por reintento.
- Invariantes cubiertos:
  - I1 reviewer != autor;
  - I2 QA != autor;
  - I3 `done` requiere evidencia;
  - I4 no dos claims activos por tarea / lease actual unico tras re-claim;
  - I5 evento aplicado incrementa `seq` y `aggregate_version`;
  - I6 replay reconstruye el mismo snapshot por hash canonico;
  - I7 evento aplicado queda atribuido/autenticado;
  - I8 intent duplicado se deduplica y no se aplica dos veces.
- El runner se agrego a `.github/workflows/validate.yml` como `Run runtime property invariant cases`.

## Limites respetados

- No se modifico `runtime/`.
- No se modifico contrato ni golden existentes.
- No se arranco Fase B ni Fase 5.
- Sin red. La generacion de muestras no usa random ni reloj; el harness fija el timestamp del
  `eventlog` durante las muestras para que los contraejemplos sean reproducibles.

## Validacion ejecutada

- `python examples/runtime_property_cases/run_runtime_property_cases.py`
  - OK: 26 deterministic property samples passed (I1-I8).
- Runtime completo: 104/104 verde.
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

- Revisar que la cobertura de 26 muestras cumple el test plan global 15.4.
- Confirmar que el diff de implementacion queda limitado a `examples/runtime_property_cases/` y CI.
- Ratificar o devolver hallazgos concretos.
