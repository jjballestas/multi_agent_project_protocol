---
handoff_id: HANDOFF-TASK-0027-codex-to-claude-1
task_id: TASK-0027
from: Codex
to: Claude
status: in_review
requires_response: true
response_owner: Claude
requested_action: Revisar TASK-0027 contra SPEC-0026/SPEC-0027 y aceptar o pedir cambios.
created_at: 2026-06-05
---

# HANDOFF TASK-0027 - Runtime M0 skeleton

## Delta
Implementado skeleton M0 read-only del runtime:
- `runtime/context.py`
- `runtime/router.py`
- `runtime/turn_validate.py`
- `runtime/orchestrator.py`
- `runtime/README.md`

Config:
- `protocol.config.json`: `runtime.enabled:false`, entrypoint `runtime/orchestrator.py`.
- `protocol.config.template.json`: mismo bloque por defecto.
- `domain_neutrality.scan_globs`: agrega `runtime/**`.

Golden:
- `examples/runtime_router_cases/run_runtime_router_cases.py`
- `examples/runtime_turn_cases/run_runtime_turn_schema_cases.py`
- `examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py`

## Evidencia
- `python examples\runtime_turn_cases\run_runtime_turn_schema_cases.py` -> OK, 4 casos.
- `python examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py` -> OK, 3 casos.
- `python examples\runtime_router_cases\run_runtime_router_cases.py` -> OK, 5 casos.
- `python -m py_compile runtime\context.py runtime\router.py runtime\turn_validate.py runtime\orchestrator.py examples\runtime_router_cases\run_runtime_router_cases.py examples\runtime_turn_cases\run_runtime_turn_schema_cases.py examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py` -> OK.
- `python runtime\orchestrator.py --plan --root .` -> dry-run; con `TASK-0023` done y mailbox abierto vacio selecciona `TASK-0024`.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.

## Notas de revision
- M0 no invoca agentes ni muta estado.
- `turn_validate.py` usa `jsonschema` para `runtime/turn_schema.json` y agrega checks semanticos:
  claim activo del agente/tarea, `changed_paths` dentro de scope y `task_status.from` igual al
  estado actual.
- El router implementa el orden de SPEC-0027: gate humano, mailbox, review, ready.

## Pendiente para Claude
Revisar contra SPEC-0026/SPEC-0027 y aceptar o pedir cambios.
