# runtime_turn_cases — Golden del contrato de turno (SPEC-0026)

Casos para validar `runtime/turn_schema.json` (draft-07). Resultado esperado por archivo:

| Caso | Esquema | Por qué |
|------|---------|---------|
| `valid_in_review.json` | **VÁLIDO** | report completo: tarea ready→in_review, claims/mailbox/handoff bien formados |
| `valid_human_required.json` | **VÁLIDO** | `outcome:human_required` con `gate.human_required:true` (cumple el allOf) |
| `invalid_missing_required.json` | **INVÁLIDO** | falta `commit_message` (required) |
| `invalid_human_gate.json` | **INVÁLIDO** | `outcome:decision_required` pero `gate.human_required` no es true (viola el allOf) |

Chequeos **semánticos** (no de esquema, los hace el orquestador en TASK-0027): `changed_paths ⊆ claim`
(write-allowlist), `task_status.from` == estado actual (anti-carrera). Sus golden se añaden con el
orquestador.

Runners:
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py`
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py`
- `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`
- `python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py`

The post-gate runner covers the objective C3/E7 boundary after the gate result
exists. The real `RunLog.append` entrypoint rejects `gate_green:false` with
absent or empty `obstacles`; a green gate does not require narration.
Self-declared transition and revert signals remain in `turn_validate.py`.

The obstacle runner proves the conditional semantic gate: delivery outcomes (`in_review`
or `done`) require a non-empty `obstacles` array, while non-delivery outcomes may omit it.
Its permanent negative disables delivery detection and requires the missing-obstacles case
to become incorrectly accepted, demonstrating that the predicate is load-bearing.
