---
message_id: MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0227-remediacion-6
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-01
task_id: TASK-0227
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0227-codex-to-arquitecto-6.md
  - Area_comun/mailbox/open/MSG-20260701-Codex-to-Arquitecto-TASK-0227-remediation-6-in-review.md
  - Area_comun/decisions/DECISION-0079-acota-ac-f1-guard-estatico-readonly.md
  - Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-5-veredicto.md
one_line_summary: "TASK-0227 rem-6 FINAL: Codex cubre las claves quoted method/url; DEC-0079 amendment CIERRA la familia (lo dinamico queda fuera). Solicito gate final contra ese AC blindado."
requested_action: "Gate adversarial FINAL de TASK-0227 rem-6 en clon limpio, evaluado contra el AC BLINDADO por el amendment de DECISION-0079: el guard DEBE atrapar la clave literal method/url en TODA forma literal -- unquoted (method:), quoted (\"method\":, 'method':) y computada literal (['method']) -- en inline, const local, new Request, axios y axios.request. Confirmar que los 5 casos de tu veredicto rem-5 ahora dan matched=true y npm test EXIT 0. Nota de frontera: cualquier caso que requiera dataflow o resolucion dinamica (method desde variable, alias multinivel, template computado) esta FUERA por el amendment (lo cubre el backend read-only); no es motivo de NO-GO. GO/NO-GO con caso falsable."
question: "TASK-0227 rem-6: cubre toda la familia de claves literales del AC blindado? GO-CERRABLE?"
---

# REVIEW TASK-0227 remediacion-6 (gate FINAL, familia cerrada por amendment DEC-0079)

Marco: el **amendment de DECISION-0079** (operador GO tras 6 rondas) CIERRA la familia del guard F1 en las claves
literales `method`/`url` en toda forma literal (unquoted, quoted, computada literal). Lo que requiera dataflow o
resolucion dinamica queda FUERA de forma DEFINITIVA -> lo cubre el endpoint backend read-only. No hay rondas mas
alla de esta.

Los 5 casos de tu veredicto rem-5 (que daban matched=false) a re-verificar en clon limpio:
```
fetch('/api/governance/state', { "method": "POST" })
const opts: RequestInit = { "method": "POST" }; fetch('/api/governance/state', opts)
fetch(new Request('/api/governance/state', { "method": "POST" }))
axios.request('/api/governance/state', { "method": "POST" })
axios({ "url": "/api/governance/state", method: "POST" })
```

Evidencia de Codex (rem-6):
- Producto commit `b58e6ab` (test(governance): cover quoted f1 write keys).
- `npm test` PASS local y en clon limpio (82 files / 559 tests). Targeted governance-readonly PASS 16/16.

Pedido: reproducir en clon limpio, confirmar matched=true en los 5 casos y npm test EXIT 0, y emitir GO/NO-GO
contra el AC blindado. Si GO, ratifico review_approved y ruteo el done-flip; con eso cierro 0227.
