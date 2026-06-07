---
id: TASK-0065
owner: Codex
status: draft
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: []
relates_to: [TASK-0055, TASK-0053]
phase: P2
spec_id: Area_comun/specs/SPEC-0051-prune-next-actions.md
linked_decisions: [DECISION-0014, DECISION-0012]
execution_pipeline: [anadir umbral de retencion config-gated para next_actions en protocol.config.json#maintenance (p.ej. recent_next_actions, default conservador; ausente/0 => comportamiento actual); extender scripts/prune_state.py:prune_project_state para condensar PROJECT_STATE.json#next_actions cuando supere el umbral - conservar las N recientes + reemplazar el resto por UNA entrada centinela determinista con el conteo removido y la traza (git history + memoria); idempotente (no re-condensa ni duplica centinela; preserva centinelas previos); paridad en scripts/prune_state.ps1; golden determinista en examples/runtime_prune_cases o nuevo; CI]
acceptance_criteria: [prune condensa next_actions sobre umbral conservando N recientes + 1 centinela con conteo correcto; idempotente; umbral ausente/0 = comportamiento actual intacto; resto del prune (claims/tasks/mailbox, umbrales DECISION-0014) sin regresion; paridad py/.ps1; golden + validador/encoding/neutralidad/prune py/ps verdes]
expected_output: prune_state.py/.ps1 condensan next_actions config-gated, idempotente, con paridad y golden; gates verdes.
test_plan: [golden 1: sobre umbral -> N recientes + 1 centinela conteo correcto; golden 2: bajo umbral -> sin cambios; golden 3: segunda corrida idempotente; golden 4: umbral ausente/0 -> intacto; regresion claims/tasks/mailbox; paridad py/ps; suite prune + validador/encoding/neutralidad py/ps verdes]
question_to_resolve: ninguna (alcance claro en SPEC-0051); si la condensacion obliga a un cambio incompatible de contrato => blocked + pregunta.
closure_criterion: prune condensa next_actions config-gated + idempotente + paridad py/.ps1 + golden + gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [umbral config-gated recent_next_actions; condensacion determinista (N recientes + centinela con conteo + traza); idempotente; preserva centinelas previos; ausente/0 = actual; sin regresion; paridad py/.ps1; golden + gates py/ps verdes; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0065 - Fix de higiene: el prune condensa next_actions

## Progreso

- 2026-06-07: Borrador preparado por Claude en personal/Claude/ (ventana segura). Pendiente de promover a
  `ready` + GO a Codex tras coordinar con el operador.

> `implementation` -> SDD completo. FOLLOW-UP de higiene rastreado desde Capa A / D2.1. Cierra la deuda:
> "el prune deberia condensar next_actions automaticamente (hoy solo poda claims/tasks/mailbox)". Ver SPEC-0051.

## Contexto

`prune_project_state` solo poda `active_tasks`; `PROJECT_STATE.json#next_actions` crece sin limite (27
entradas hoy; el historico previo se condenso A MANO con una entrada centinela "[HISTORICO PODADO]"). Esto
infla el cold-start (DECISION-0014). El prune debe condensar next_actions automaticamente, como ya hace con
tasks/mailbox.

## Alcance (ver SPEC-0051 sec.3)

1. Umbral de retencion config-gated `recent_next_actions` en `protocol.config.json#maintenance`
   (ausente/0 => comportamiento actual).
2. Condensar al podar: conservar N recientes + 1 centinela determinista (conteo + traza); idempotente;
   preservar centinelas previos.
3. Paridad en `scripts/prune_state.ps1`; golden determinista + CI.

## Restricciones

- Aditivo, config-gated; **no** cambia umbrales ni logica de claims/tasks/mailbox (DECISION-0014/SPEC-0041).
- No reescribe el texto de las next_actions (solo condensa la lista).
- **Neutralidad**; **sin secretos**; ASCII en state (DECISION-0012).
- Cambio incompatible de contrato => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

Camino a v1.0: D2.4 done -> **DECISION-0020 (regla anti-colision) + esta (fix prune)** -> RELEASE v1.0
(aprobacion humana). Promover de a una (regla anti-colision): Codex la toma cuando este `ready` + GO.
