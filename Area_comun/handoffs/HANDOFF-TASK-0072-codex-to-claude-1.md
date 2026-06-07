---
task_id: TASK-0072
from: Codex
to: Claude
status: for_review
created_at: 2026-06-07
decisions_referenced: [DECISION-0022, DECISION-0017, DECISION-0015, DECISION-0018, DECISION-0020]
spec_id: SPEC-0058-intent-coordination-flow
---

# Handoff TASK-0072 - Flujo de coordinacion por intents

## Resumen

Implementado el write-path `runtime/submit_intent.py` (+ wrapper delegado `.ps1`) para someter una transicion atomica de estado de protocolo via event log:

- tipos soportados: `task_status`, `task_upsert`, `claim` (`acquire`/`release`/`block`) y `decision`;
- validacion de actor registrado/habilitado, capacidad, claim activo y scope antes de aplicar;
- idempotencia por clave explicita o hash canonico del intent;
- timestamp provisto para `intent.applied` y genesis-ref, sin reloj en el camino nuevo;
- append de `intent.applied` + `materialize_to_disk` + actualizacion de status en markdown de tarea cuando aplica;
- rollback de runtime/state y archivos calientes si falla la materializacion;
- rechazo claro si ya existe drift contra un genesis previo (requiere re-genesis antes de operar autoritativo).

## Rutas tocadas

- `runtime/submit_intent.py`
- `runtime/submit_intent.ps1`
- `runtime/eventlog.py`
- `runtime/protocol_replay.py`
- `examples/intent_flow_cases/run_intent_flow_cases.py`
- `.github/workflows/validate.yml`
- `AGENTS.md`
- `AGENTS.template.md`
- `Area_comun/protocol/TASK_PROTOCOL.md`
- `Area_comun/protocol/N_AGENT_RUNTIME.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/tasks/TASK-0072-codex-intent-coordination-flow.md`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0071-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0072-GO-intent-flow.md`
- `Area_comun/mailbox/archived/MSG-20260607-Codex-to-Claude-anomalia-task0072-ledger.md`

## Validaciones

- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK 9 cases
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK 6 cases
- `python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` -> OK 6 cases
- `python examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py` -> OK 7 cases
- `python -m compileall runtime examples\intent_flow_cases` -> OK
- `python scripts\validate_collaboration_state.py --root .` -> OK, con drift WARNING esperado por modo sombra
- `powershell ... scripts\validate_collaboration_state.ps1 -Root .` -> OK, con drift WARNING esperado
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK
- `powershell ... scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK
- `python scripts\scan_encoding.py --root .` -> OK
- `powershell ... scripts\scan_encoding.ps1 -Root .` -> OK
- `python scripts\scan_domain_neutrality.py --root .` -> OK
- `powershell ... scripts\scan_domain_neutrality.ps1 -Root .` -> OK
- `python scripts\prune_state.py --root . --check` -> OK, no due (`cold_start_tokens=14383`)
- `python examples\sbom_cases\run_sbom_cases.py` -> OK 4 cases
- `git diff --check` -> OK; solo avisos CRLF de Git

## Notas de revision

- No encendi `event_state.enforce` ni `authoritative` en el repo vivo.
- Los golden demuestran enforce ON en fixture: secuencia por intents pasa el validador con drift 0 y una edicion manual posterior hard-failea.
- El repo vivo sigue en modo sombra; el drift WARNING del validador es esperado mientras el ledger vivo se edite manualmente.
- Antes de usar `submit_intent` sobre la instancia viva en autoritativo hace falta re-emitir genesis sincronizado, como ya indicaba SPEC-0058.
