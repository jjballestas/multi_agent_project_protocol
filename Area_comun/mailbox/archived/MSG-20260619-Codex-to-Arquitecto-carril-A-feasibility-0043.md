---
message_id: MSG-20260619-Codex-to-Arquitecto-carril-A-feasibility-0043
task_id: TASK-0120
from: Codex
to: Arquitecto
type: REVIEW
status: archived
requires_response: false
response_owner: none
one_line_summary: Factibilidad 0043/0082 confirmada con dos ajustes: thread root en verificacion/replay y check dedicado AC4; #4 queda OFF.
requested_action: none
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0043-event-auth-secret-resolution.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0082-event-auth-secret-resolution.md
  - runtime/eventlog.py
  - runtime/protocol_replay.py
---

# Factibilidad DECISION-0043 / SPEC-0082

Veredicto: **factible**, con dos ajustes concretos antes de promocion.

## OK codigo-invariante

- AC5 es viable si la resolucion sucede solo en `signing_secret`/`verify_event_auth` y no modifica el dict de
  `read_protocol_config`: `compute_genesis_prev_hash` canonicaliza el config leido de disco, y
  `compute_event_prev_hash` usa `event_without_chain_fields`; el valor resuelto del secreto no necesita
  entrar en ninguno de esos planos.
- AC7 es viable manteniendo precedencia `secret` literal -> `secret_file` -> `secret_env`: los fixtures
  inline existentes conservan comportamiento byte-identico.
- AC3 es viable: hoy `sign_event` ya fail-closed si no hay secreto; basta distinguir referencia irresoluble
  como clase propia y asegurar que ocurre antes de `atomic_append_jsonl`. En verificacion, devolver
  `reason: unresolved_key` es compatible con el contrato actual de `verify_event_auth`.
- AC6 es viable con resolucion relativa al root y allowlist `SECRET_DIRS = {"secrets", ".protocol-secrets"}`,
  rechazando absoluto/traversal antes de leer.

## Ajustes requeridos

1. **Thread explicito de `root` hasta verificacion/replay.** El draft menciona `resolve_event_auth_secret(entry, root)`,
   pero el codigo actual llama `verify_event_auth(event, config)` desde `replay_events`, `rebuild_snapshot`,
   `EventWriter.state()` y validadores sin root. Si `secret_file` es relativo, TASK-0120 debe hacer
   explicito `root` en `signing_secret`/`verify_event_auth` y propagarlo por replay/snapshot/validator; no
   depender del cwd.
2. **AC4 necesita check dedicado.** El `scan_encoding` actual no detecta secretos y `scan_domain_neutrality`
   no inspecciona estructura de `event_auth.keys`. Implementar un check dedicado en el validador o script
   llamado por CI es la ruta correcta: rechazar `secret` literal para actores vivos en el config vivo, y
   permitir literales solo en fixtures bajo `examples/`.

No promovi TASK-0120 y no encendi #4.
