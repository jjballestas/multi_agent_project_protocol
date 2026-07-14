---
message_id: MSG-20260714-Operador-to-Arquitecto-RESP-disposicion-task-sandbox
from: Operador
to: Arquitecto
type: RESP
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - Area_comun/mailbox/open/MSG-20260714-Arquitecto-to-Operador-FYI-anomalia-task-sandbox-suelto.md
  - Area_comun/tasks/TASK-SANDBOX-GRANT-EXECUTE-encargo-agente-bd.md (UNTRACKED)
one_line_summary: "Disposicion de la anomalia TASK-SANDBOX-GRANT-EXECUTE (archivo suelto untracked en Area_comun/tasks/ del hub): opcion (b) -- PRESERVAR moviendolo a personal/operador/ (no borrar). Sacarlo de la ruta gobernada para que ningun stage amplio lo arrastre."
requested_action: "Ejecuta la opcion (b): mueve (sin destruir) el archivo untracked Area_comun/tasks/TASK-SANDBOX-GRANT-EXECUTE-encargo-agente-bd.md a personal/operador/ (p.ej. personal/operador/encargos-sueltos/ o la subcarpeta que el operador use). No lo commitees a la ruta gobernada; queda preservado en el area del operador para su decision posterior."
question: "Confirmas el move a personal/operador/ ejecutado?"
---

# RESP - Disposicion de la anomalia TASK-SANDBOX-GRANT-EXECUTE

Recibida tu FYI (DECISION-0018) sobre el archivo suelto untracked en la ruta gobernada del hub.

**Disposicion: opcion (b) -- PRESERVAR en personal/operador/.** No borrar: aunque la deadline
(2026-07-05) esta vencida y nunca entro a la historia, el encargo puede seguir vivo (precondicion
P4.x sandbox), asi que se conserva en mi area en vez de destruirse.

Ejecuta el move (sin destruir) desde `Area_comun/tasks/` a `personal/operador/`. Con eso:
- La ruta gobernada del hub queda limpia (ningun stage amplio futuro lo arrastra).
- El contenido se preserva para mi decision posterior (moverlo al repo de producto sandbox si sigue
  vivo, o descartarlo si ya se consumio).

No hace falta sanear su no-ASCII ni su formato: al vivir en mi area personal no pasa por el
validador ni por scan_encoding del hub.
