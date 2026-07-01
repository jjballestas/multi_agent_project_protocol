---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0227-remediacion-6
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-01
task_id: TASK-0227
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-5-veredicto.md
  - Area_comun/decisions/DECISION-0079-acota-ac-f1-guard-estatico-readonly.md
  - Area_comun/tasks/TASK-0227-codex-zeus-aegis-npm-test-f1-boundary.md
one_line_summary: "TASK-0227 rem-6 (RONDA FINAL BLINDADA): cubrir claves string-literal quoted method/url; DEC-0079 amendment cierra la familia -> no hay rem-7."
requested_action: "Remediacion-6 FINAL de TASK-0227: extender el guard F1 de modo que matchee la clave literal method/url en TODA su forma -- identificador sin comillas (method:), string literal con comillas (\"method\":, 'method':) y computada literal (['method']) -- en objeto de opciones inline, const local (tipado o no), new Request(...), axios(...), axios.<verbo>() y axios.request(url, cfg). Usa un patron tipo [\"']?(method|url)[\"']?\\s*: que cubra quoted y unquoted de una. Casos falsables del Analista rem-5 que hoy dan matched=false: fetch(gov, { \"method\": \"POST\" }); const opts: RequestInit = { \"method\": \"POST\" }; fetch(gov, opts); fetch(new Request(gov, { \"method\": \"POST\" })); axios.request(gov, { \"method\": \"POST\" }); axios({ \"url\": gov, method: \"POST\" }). Anadir negativos permanentes. Conservar npm test EXIT 0 y los negativos previos. Redelivery a in_review. Esta es la ULTIMA ronda: el amendment de DEC-0079 declara la familia CERRADA (lo dinamico queda fuera, lo cubre el backend read-only)."
---

# ACTION TASK-0227 - remediacion-6 (RONDA FINAL, familia cerrada por DEC-0079 amendment)

Veredicto Analista rem-5: el caso `RequestInit` tipado ya matchea, pero el guard deja pasar la **clave con
comillas**. Casos falsables (hoy matched=false):

```
fetch('/api/governance/state', { "method": "POST" })
const opts: RequestInit = { "method": "POST" }; fetch('/api/governance/state', opts)
fetch(new Request('/api/governance/state', { "method": "POST" }))
axios.request('/api/governance/state', { "method": "POST" })
axios({ "url": "/api/governance/state", method: "POST" })
```

Pedido (ronda final):
1. El guard matchea la clave literal `method`/`url` en toda forma literal: `method:`, `"method":`, `'method':`,
   `['method']`. Un patron `["']?(method|url)["']?\s*:` cubre quoted y unquoted de una pasada.
2. Aplica a inline, const local (tipado o no), `new Request(...)`, `axios(...)`, `axios.<verbo>()`,
   `axios.request(url, cfg)`.
3. Negativos permanentes de los 5 casos de arriba. Conservar `npm test` EXIT 0 y los negativos previos.
4. Redelivery a in_review.

Frontera BLINDADA (DEC-0079 amendment 2026-07-01, GO operador): con esta ronda la familia de claves literales
queda CERRADA. Lo que requiera dataflow o resolucion dinamica (method desde variable, alias multinivel, template
computado) queda FUERA de forma definitiva, cubierto por el endpoint backend read-only. **No habra rem-7.**
