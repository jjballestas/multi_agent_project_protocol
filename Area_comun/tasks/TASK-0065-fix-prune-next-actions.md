---
id: TASK-0065
owner: Claude
status: done
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: []
relates_to: [TASK-0055, TASK-0053]
phase: P2
spec_id: Area_comun/specs/SPEC-0051-prune-next-actions.md
linked_decisions: [DECISION-0014, DECISION-0012]
execution_pipeline: [anadir umbral config-gated recent_next_actions en protocol.config.json#maintenance (vivo+template); extender scripts/prune_state.py:prune_project_state con condense_next_actions (conserva N recientes + 1 centinela determinista con conteo + traza; fusiona centinelas previos; idempotente); reportar next_actions_condensed en run-log; paridad py/.ps1 (delegacion); golden en examples/runtime_prune_cases; gates]
acceptance_criteria: [prune condensa next_actions sobre umbral conservando N recientes + 1 centinela con conteo correcto; idempotente; umbral ausente/0 = comportamiento previo; centinela previo fusionado; resto del prune (claims/tasks/mailbox, umbrales DECISION-0014) sin regresion; paridad py/.ps1; golden + validador/encoding/neutralidad/prune py/ps verdes]
expected_output: prune_state.py condensa next_actions config-gated, idempotente; golden 4 cases nuevos verdes; gates verdes.
test_plan: [golden runtime_prune_cases: sobre umbral, bajo umbral, ausente/0, centinela previo fusionado; regresion mailbox/claims/tasks; paridad py/ps; validador/encoding/neutralidad py/ps verdes]
question_to_resolve: ninguna (alcance claro en SPEC-0051).
closure_criterion: prune condensa next_actions config-gated + idempotente + paridad py/.ps1 + golden + gates verdes.
closure_criteria: [umbral config-gated recent_next_actions (vivo+template); condensacion determinista idempotente con fusion de centinelas; ausente/0 = previo; sin regresion; paridad py/.ps1; golden + gates py/ps verdes]
---

# TASK-0065 - Fix de higiene: el prune condensa next_actions

## Progreso

- 2026-06-07: Borrador preparado por Claude en personal/Claude/ (ventana segura).
- 2026-06-07: RESUELTA por Claude (instruccion del operador): `recent_next_actions` config-gated (vivo=8,
  template=8) + `condense_next_actions` determinista/idempotente en `scripts/prune_state.py` (fusiona
  centinelas previos) + `next_actions_condensed` en run-log + 4 golden nuevos en `examples/runtime_prune_cases`.
  Paridad py/.ps1 por delegacion. Gates verdes. CIERRA el FOLLOW-UP de Capa A / D2.1.

## Contexto

`prune_project_state` solo podaba `active_tasks`; `PROJECT_STATE.json#next_actions` crecia sin limite. El
prune ahora lo condensa automaticamente, como ya hacia con tasks/mailbox. Ver SPEC-0051.

## Resultado

- `scripts/prune_state.py`: `DEFAULT_CONFIG["recent_next_actions"]=0`, `condense_next_actions(state, keep)`,
  `prune_project_state` devuelve `(removed, condensed)`, `apply_prune` reporta `next_actions_condensed`.
- `protocol.config.json` / `protocol.config.template.json`: `maintenance.recent_next_actions: 8`.
- `examples/runtime_prune_cases/run_runtime_prune_cases.py`: 4 cases nuevos (sobre/bajo umbral, ausente/0,
  fusion de centinela previo) + idempotencia; existentes intactos.

## Nota

Camino a v1.0: D2.4 done -> DECISION-0020 + **esta (fix prune, done)** -> RELEASE v1.0 (aprobacion humana,
concedida por el operador 2026-06-07).
