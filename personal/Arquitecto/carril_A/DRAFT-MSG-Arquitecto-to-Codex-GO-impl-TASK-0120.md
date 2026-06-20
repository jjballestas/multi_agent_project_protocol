---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-GO-impl-TASK-0120
type: GO
task_id: TASK-0120
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: GO a implementar TASK-0120 (cargador HMAC event_auth, SPEC-0082) con 4 condiciones; #4 OFF; maker!=checker.
requested_action: "Implementar TASK-0120 segun SPEC-0082 (con los 2 ajustes de tu pasada ya incorporados); entregar in_review con el golden event_auth_secret_resolution_cases verde o blocked concreto. NO encender #4, NO provisioning real."
question: "Confirmas arranque de TASK-0120 (in_progress, claim activo) bajo las 4 condiciones, sin encender #4 ni provisionar secretos reales?"
context_refs:
  - Area_comun/specs/SPEC-0082-event-auth-secret-resolution.md
  - Area_comun/tasks/TASK-0120-event-auth-secret-resolution.md
  - Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md
---

# GO implementacion TASK-0120 - cargador de secreto HMAC de event_auth (SPEC-0082)

GATE: encolar/entregar SOLO cuando el mirror confirme la promocion 1.12.0 (commit + drift 0 + read-back en
disco). Promovido DECISION-0043 + SPEC-0082 + TASK-0120 (ready). Implementa TASK-0120 segun SPEC-0082, con
los 2 ajustes de tu pasada de factibilidad ya incorporados (thread explicito de `root` en
`signing_secret`/`verify_event_auth` y sus llamadores replay/snapshot/validador; AC4 = check DEDICADO, no
`scan_encoding`/`scan_domain_neutrality`).

## 4 condiciones (operador)
1. Golden nuevo `examples/event_auth_secret_resolution_cases` (AC1-AC8) **verde**, en copia verificada
   limpia == HEAD que persiste.
2. **#4 OFF**; sin provisioning real; secretos SOLO fixtures bajo `examples/`; sin tocar
   `event_state`/flags ni `event_auth.enabled`.
3. **maker!=checker**: tu implementas -> Arquitecto reproduce/revisa (corre el golden + suites #4
   existentes byte-identicas + gates).
4. Disciplina de persistencia/corrupcion del FS: verifica limpio == HEAD al escribir (el mount del
   sandbox se re-trunca; ver RUNBOOK-windows-sandbox-temp-acl); usa staging repo-local, no `%TEMP%`.

## Entrega
- `runtime/eventlog.py` (resolutor `resolve_event_auth_secret(entry, root)` + precedencia literal->file->env
  + fail-closed `unresolved_key` + path-safety `SECRET_DIRS`), thread de `root` por replay/snapshot/validador,
  check dedicado AC4, golden + cableado en CI, CHANGELOG.
- Avanza in_progress -> in_review con claim activo (libera al entregar). Si aparece bloqueo: `blocked` +
  pregunta concreta. Canal ASCII.

#4 sigue OFF. El encendido (provisioning real + anchor + re-genesis + flip) es GO aparte del operador.
