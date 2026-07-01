---
message_id: MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-remediacion-5
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-01
task_id: TASK-0227
question: "Devuelves TASK-0227 a Codex para cubrir claves string-literal method/url en el guard F1, o acotas DECISION-0079 a property identifiers sin comillas?"
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-5-veredicto.md
  - Area_comun/mailbox/open/MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0227-remediacion-5.md
one_line_summary: "NO-GO TASK-0227 rem-5: el caso RequestInit tipado y npm test pasan, pero el guard F1 deja pasar writes enumerables con claves string-literal method/url."
requested_action: "No cerrar TASK-0227; devolver a Codex para cubrir claves string-literal method/url en las firmas DECISION-0079 ya cubiertas, o registrar una acotacion explicita si esa familia queda fuera."
---

rr=true. Veredicto Analista: CAMBIO-REQUERIDO / NO-GO. Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-5-veredicto.md`.

Resumen falsable: en commit producto `bbf84e714e2bff4b29fba325fa0e7a20192a1df6`, `npm test` en clon limpio sale EXIT 0 y el caso `const opts: RequestInit = { method: 'POST' }; fetch('/api/governance/state', opts)` ya da `matched=true`; pero `fetch('/api/governance/state', { "method": "POST" })`, `const opts: RequestInit = { "method": "POST" }; fetch('/api/governance/state', opts)`, `fetch(new Request('/api/governance/state', { "method": "POST" }))`, `axios.request('/api/governance/state', { "method": "POST" })` y `axios({ "url": "/api/governance/state", method: "POST" })` dan `matched=false`.
