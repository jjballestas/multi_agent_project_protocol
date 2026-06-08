---
handoff_id: HANDOFF-TASK-0082-codex-to-claude-1
task_id: TASK-0082
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0082 - SA.5 docs supervised autonomy

## Entrega

Implementada la rebanada documental SA.5, sin cambios funcionales:

- Nuevo `Area_comun/protocol/SUPERVISED_AUTONOMY.md`.
- La guia cubre `runtime.supervised_autonomy`, registro de activacion, caps obligatorios y
  `--allow-supervised-autonomy`.
- Documenta paradas duras: `max_turns_reached`, `paused` por `runtime/state/PAUSE`,
  `wallclock_exhausted`, `human_checkpoint` por K turnos y checkpoint por fix-cycles.
- Documenta `*.runreport.md` y como leerlo antes de una corrida posterior.
- Deja explicito que SA.4 (invoker real multi-turno) sigue gateado por GO del operador + rollback; el
  invoker real conserva `--once`.
- Enlaces agregados desde `Area_comun/protocol/N_AGENT_RUNTIME.md` y `README_INSTANCIACION.md`.

## Archivos tocados

- `Area_comun/protocol/SUPERVISED_AUTONOMY.md`
- `Area_comun/protocol/N_AGENT_RUNTIME.md`
- `README_INSTANCIACION.md`
- `Area_comun/tasks/TASK-0082-codex-autonomia-SA5-docs.md`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/TASK_INDEX_ARCHIVE.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/CLAIMS_ARCHIVE.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0081-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0082-GO-autonomia-SA5.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0082-in-review.md`

## Validacion

- `python scripts\scan_encoding.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK, warning esperado de runtime drift.
- `python scripts\prune_state.py --root . --check` -> OK.
- `git diff --check` -> OK, solo warnings CRLF.

## Riesgos residuales

- No se valida una corrida real multi-turno porque SA.4 esta fuera de alcance y gateada.
- La guia describe la operacion existente SA.1-SA.3; si SA.4 cambia el contrato, requerira actualizacion posterior.

## Requested action

Ratificar TASK-0082 contra SPEC-0064 y, si procede, cerrarla como done.
