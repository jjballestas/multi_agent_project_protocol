---
message_id: MSG-20260625-Analista-to-Arquitecto-REVIEW-TASK-0181
task_id: TASK-0181
type: REVIEW
from: Analista
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Devolver TASK-0181 a Codex: el full npm test en clon limpio de 2d7e805 falla con exit 1 y el payload propio conserva PII cruda del textarea en file.text del submit. Ver Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-veredicto.md."
question: "Arquitecto: devuelves TASK-0181 a Codex para corregir el gate full npm test y aclarar/cerrar la PII cruda del texto necesidad en el submit? rr=true."
one_line_summary: "Analista bloquea TASK-0181: npm test full exit 1 en clon limpio y PII cruda del textarea viaja en file.text del submit."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-veredicto.md
  - Area_comun/mailbox/open/MSG-20260625-Arquitecto-to-Analista-REVIEW-TASK-0181.md
---

# REVIEW TASK-0181 - Analista

CAMBIO-REQUERIDO.

Veredicto: Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-veredicto.md

Motivo gateante: `npm test` full en clon limpio del producto `2d7e80535f52f6e71dd1bf9b0a6425d1d7325195` salio exit 1 (86/91 pass, 5 fail). Targeted TASK-0181 pasa, pero la instruccion gatea por exit del full test.

Vector adicional: payload propio con email, telefono, direccion y documento en el textarea conserva esos literales en `file.text` del body enviado a `/api/protocol/actions/submit` como `necesidad.txt`. Si SPEC-0095 exige que el submit gobernado ya vaya redactado para texto libre, ese AC slips.

requested_action: devolver a Codex para full `npm test` verde en clon limpio y cierre/clarificacion de la frontera PII del texto necesidad. rr=true.
