---
id: TASK-0026
owner: Claude
status: done
type: analysis
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: []
phase: P2
linked_decisions: [DECISION-0009, DECISION-0007, DECISION-0001]
objective: Diseñar el contrato de turno (turn_schema.json) y el router determinista del runtime (M0), base de toda la capa.
expected_output: SPEC del contrato de turno + SPEC del router + turn_schema.json (borrador) + golden de reports válidos/inválidos.
question_to_resolve: ¿Qué campos mínimos debe tener un turn report para que el orquestador aplique transiciones de estado de forma determinista y segura (claim, mailbox, TASK_INDEX, handoff), y cómo decide el router la próxima jugada y su owner?
closure_criterion: Specs publicadas (SDD-elegibles para las tareas de implementación de Codex) y golden de turn reports; validadores verdes.
---

# TASK-0026 — Runtime M0: contrato de turno + router

> `analysis` (4 campos mínimos). Ejecuta DECISION-0009 (M0 del diseño §7). Es la pieza base: sin
> contrato de turno y router deterministas no hay orquestación segura. Neutral de dominio.

## Alcance
- **SPEC del contrato de turno** (`runtime/turn_schema.json`): qué reporta un agente al terminar un
  turno (transiciones a aplicar: claim, mailbox open→answered, TASK_INDEX status, handoff, commit
  message) y validación estricta del report.
- **SPEC del router**: selección determinista de la próxima unidad de trabajo y su owner a partir de
  `PROJECT_STATE`/`TASK_INDEX`/`CLAIMS`/`mailbox/open`.
- Golden de turn reports válidos/ inválidos.

## riesgos
- Un contrato de turno laxo permitiría transiciones inseguras. Mitigar: esquema estricto + el gate
  por turno (validador) detrás.

## notas_de_ejecucion
- Entregado: `runtime/turn_schema.json` (contrato de turno, draft-07 estricto), `runtime/README.md`,
  `SPEC-0026` (contrato de turno), `SPEC-0027` (router determinista), golden en
  `examples/runtime_turn_cases/` (valid_in_review, valid_human_required, invalid_missing_required,
  invalid_human_gate).
- **Verificado:** `jsonschema` valida los 4 golden exactamente como se espera (válidos OK; inválidos
  rechazados por `required` y por el `allOf` del gate humano). Esquema = JSON válido.
- Desbloquea **TASK-0027** (Codex, impl: skeleton + `--plan` dry-run + validador de turno + router).
- Diseño base: `Area_comun/artifacts/DISENO-runtime-orquestacion-automatizada.md` §3–§4.
