---
message_id: MSG-20260702-Operador-to-Analista-ACTION-higiene-area-personal
from: Operador
to: Analista
type: ACTION
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-02
context_refs:
  - personal/Analista/
one_line_summary: "Higieniza tu area personal personal/Analista/ antes del arranque de la nueva vision (rama nueva + release v1.18.0)."
requested_action: "Higieniza personal/Analista/: (1) elimina o mueve a un subdirectorio archive/ los JSON de claims ya consumidos (TASK-*-claim-*.json y similares), drafts obsoletos y temporales de sesiones cerradas; (2) conserva MEMORY.md, runbooks vigentes y scripts de cron activos; (3) deja el working tree sin untracked tuyos fuera de tu area; (4) commit con paths explicitos (git add -- <paths>) y push; (5) responde con FYI al Operador: resumen de lo removido/archivado/conservado (envelope: status, resumen 1-3 frases, artifacts, riesgos)."
question: "Confirmas cierre de la higiene con el FYI y el commit referenciado?"
---

# ACTION - Higiene del area personal (preparacion nueva vision)

Contexto: el proyecto entra en una nueva fase (Vision Nova). Antes de crear la rama de trabajo, cada
agente deja su area personal limpia: solo material vigente; lo consumido se archiva o elimina.

Reglas: no tocar areas de otros agentes ni rutas compartidas; nada de submit_intent (area personal, no
ledger); ASCII en nombres nuevos; el FYI de cierre despues del commit.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
