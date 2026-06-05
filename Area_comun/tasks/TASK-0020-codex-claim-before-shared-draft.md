---
id: TASK-0020
owner: Codex
status: done
type: documentation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0017, TASK-0018, TASK-0019]
phase: P2
spec_id: none
objective: Formalizar la regla claim-before-shared-draft para evitar colisiones operativas.
expected_output: Decision append-only y protocolos actualizados con la regla.
question_to_resolve: none
closure_criterion: La regla aparece en AGENTS/protocolos y el estado valida verde.
---

# TASK-0020 - Regla claim antes de borrador compartido

## objetivo
Convertir la leccion de coordinacion TASK-0019 en regla explicita: un agente no crea ni edita
archivos en rutas compartidas sin claim activo previo.

## entradas
- Solicitud directa del operador humano.
- Incidente coordinado por mailbox en TASK-0019.
- `DECISION-0005` comunicacion compacta.

## archivos_relevantes
- read: `Area_comun/state/CLAIMS.json`, `Area_comun/mailbox/open/`
- create: `Area_comun/decisions/DECISION-0007-claim-before-shared-draft.md`
- edit: `AGENTS.md`, `AGENTS.template.md`, `Area_comun/README.template.md`,
  `Area_comun/protocol/TASK_PROTOCOL.md`, `Area_comun/protocol/COMMUNICATION_PROTOCOL.md`,
  `Area_comun/state/TASK_INDEX.json`, `Area_comun/state/PROJECT_STATE.json`,
  `Area_comun/state/CLAIMS.json`

## entregables
- `Area_comun/decisions/DECISION-0007-claim-before-shared-draft.md`
- Regla en AGENTS/protocolos/templates.
- `Area_comun/handoffs/HANDOFF-TASK-0020-codex-to-claude-1.md`

## definition_of_done
- [x] Decision registrada.
- [x] Regla visible para agentes entrando en frio.
- [x] Validador verde.
- [x] Handoff creado.
- [x] TASK_INDEX.json actualizado.
- [x] No secrets.
- [x] Core permanece neutral.

## riesgos
La regla agrega disciplina operativa, pero no impide tecnicamente escrituras sin claim; el control
sigue siendo procedimental salvo futura validacion automatica.

## preguntas_abiertas
none

## notas_de_ejecucion
Se creo claim activo antes de editar, para dogfoodear la nueva regla.
