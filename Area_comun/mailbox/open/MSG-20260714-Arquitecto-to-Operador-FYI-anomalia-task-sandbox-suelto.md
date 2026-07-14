---
message_id: MSG-20260714-Arquitecto-to-Operador-FYI-anomalia-task-sandbox-suelto
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-14
context_refs:
  - Area_comun/tasks/TASK-SANDBOX-GRANT-EXECUTE-encargo-agente-bd.md (UNTRACKED)
one_line_summary: "Anomalia DECISION-0018: archivo suelto NO commiteado en Area_comun/tasks/ del HUB (TASK-SANDBOX-GRANT-EXECUTE encargo a 'Agente-BD', dominio producto sandbox/verifier, no-ASCII, deadline vencida 2026-07-05). No es un task del hub ni cumple su formato; no lo toco. Decide disposicion."
requested_action: "Indica disposicion: (a) moverlo al repo/instancia de producto que corresponda, (b) moverlo a personal/operador/, o (c) borrarlo si ya fue consumido. Si me autorizas, ejecuto (b) o (c)."
question: "Que disposicion le doy al archivo suelto TASK-SANDBOX-GRANT-EXECUTE?"
---

# FYI - Archivo suelto en ruta gobernada del hub (untracked)

Al auto-poll de inicio de sesion aparecio `Area_comun/tasks/TASK-SANDBOX-GRANT-EXECUTE-encargo-
agente-bd.md` como UNTRACKED (nunca commiteado). Senales de anomalia (DECISION-0018):
- Dominio de PRODUCTO (sandbox de mutadores, rol verifier, procs/vistas) en el HUB neutral --
  si se commiteara, romperia la frontera de neutralidad (AGENTS.md s.4).
- Formato: frontmatter sin `status:`/`file:` (no es un task valido del protocolo; el validador
  lo rechazaria) y contenido con acentos (no-ASCII, romperia scan_encoding).
- Destinatario `Agente-BD` no es participante del hub; deadline 2026-07-05 ya vencida.
- Al estar untracked NO afecta HEAD ni gates de clean-clone; el riesgo es que un stage amplio
  futuro lo arrastre.

No lo edito ni muevo (no es mio y la disposicion es tuya). Nota: el encargo en si parece
pertenecer al mundo del producto (precondicion P4.x sandbox) -- si sigue vivo, su lugar seria
el repo/instancia de producto o tu area personal.
