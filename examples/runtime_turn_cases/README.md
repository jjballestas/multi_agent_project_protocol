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
