---
handoff_id: HANDOFF-TASK-0049-codex-to-claude-1
task_id: TASK-0049
from: Codex
to: Claude
status: in_review
created_at: 2026-06-06
requires_response: true
response_owner: Claude
requested_action: Revisar TASK-0049 contra el task-file y aceptar o devolver hallazgos concretos.
---

# TASK-0049 - Handoff de review

## Resumen

Implementado el hardening de autor-de-record (Capa A.6):

- `runtime/review_qa.py` agrega `author_of_record(task)`, que lee solo `task.original_author` y fallback
  `task.owner`.
- `task_author(...)` queda alineado con `author_of_record(...)` y deja de usar `payload.author` /
  `payload.original_author`.
- `runtime/turn_validate.py` usa `author_of_record(task)` para la guarda reviewer/QA != autor.
- `runtime/apply.py` persiste `original_author` en `TASK_INDEX` si falta antes de aplicar una transicion
  de tarea. No lo sobrescribe si ya existe.
- `examples/runtime_review_qa_cases/run_runtime_review_qa_cases.py` sube de 9 a 15 casos:
  - autor real no puede self-review/self-QA aunque falsifique `payload.author`;
  - reviewer/QA legitimos no son rechazados aunque `payload.author` sea igual al actor;
  - `original_author` se persiste en el primer apply;
  - `assign_fix` no sobrescribe `original_author`.

No implementado: Fase B del writer-vivo ni Fase 5.

## Validacion ejecutada

- Runtime suites: 72/72 verdes.
  - router 10/10
  - eventlog 5/5
  - eventlog gate 5/5
  - review_qa 15/15
  - agent_registry 4/4
  - turn schema 5/5
  - turn semantic 5/5
  - apply 4/4
  - loop 8/8
  - observability 5/5
  - llm adapter 6/6
- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/validate_collaboration_state.py --root examples/minimal_instance`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root examples/minimal_instance`
- `python scripts/scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .`
- `python examples/encoding_gate_cases/run_encoding_gate_cases.py`
- `python examples/handoff_release_cases/run_handoff_release_cases.py`
- `python examples/mailbox_status_cases/run_mailbox_status_cases.py`
- `python scripts/prune_state.py --root . --check`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/sdd_validation_cases/run_sdd_cases.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/compact_comms_validation_cases/run_compact_comms_cases.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1`
- workflow YAML parse OK.
- `git diff --check` OK; solo warnings CRLF esperados.

## Notas de review

- `payload.author` sigue permitido por schema como dato informativo, pero ya no decide la exclusion de
  autor.
- El fallback para tareas sin `original_author` es `task.owner`, como pidio TASK-0049.
- La persistencia ocurre despues de validar el turno y antes de cambiar el estado, de modo que conserva
  el owner original y evita sobrescrituras posteriores.
