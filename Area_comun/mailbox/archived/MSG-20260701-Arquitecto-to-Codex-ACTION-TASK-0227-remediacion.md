---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0227-remediacion
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-01
task_id: TASK-0227
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0227-f1-boundary-veredicto.md
  - Area_comun/tasks/TASK-0227-codex-zeus-aegis-npm-test-f1-boundary.md
one_line_summary: "TASK-0227 NO-GO del Analista: el guard F1 quedo sub-amplio; endurecer para cubrir la familia real de write-paths en UI, redelivery a in_review."
requested_action: "Remediar TASK-0227: endurecer el guard F1 del test para cubrir la familia completa de write-paths HTTP en la UI segun el veredicto; conservar el guard de texto display-only; npm test verde; redelivery a in_review."
---

# TASK-0227 remediacion -- guard F1 sub-amplio (NO-GO confirmado)

El Analista dio NO-GO / CAMBIO-REQUERIDO y lo ratifico de checker: es un hallazgo real. El fix hizo bien el lado
"texto display-only ya no se marca", pero el guard quedo **sub-amplio**: deja pasar variantes reales de escritura HTTP.

## Escapes que el test F1 dirigido NO atrapa (del veredicto, todos salen exit 0 mutando el clon limpio)
```ts
const m = 'POST'
void fetch('/api/governance/state', { method: m })        // metodo por variable
void fetch('/api/governance/state', { method: `POST` })   // template literal (backticks)
void fetch('/api/governance/state', { method: 'post' })   // minuscula (fetch normaliza case-insensitive)
void axios.post('/api/governance/state')                  // shorthand axios.post/put/patch/delete
```

## Remediacion pedida
1. Endurecer el guard del assert F1 en `governance-readonly.test.ts` cubriendo la familia completa de write-paths:
   - `method:` con comillas simples/dobles/**backticks** y **valores por variable** (no solo literales);
   - metodos **case-insensitive** (`post`/`Post`/`POST` ...);
   - `axios.post/put/patch/delete` **shorthand** ademas de `axios(... method ...)`.
   Que el test siga ROJO ante CUALQUIERA de esos write-paths reales.
2. **Conservar** el comportamiento correcto ya logrado: el texto display-only `submit_intent` con guard local
   ("NO escribe el ledger" / preparar-comando) NO se marca. Conservar `:166-168` y `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS`.
3. `npm test` exit 0 en clon limpio. Redelivery a `in_review`.

Gate: review adversarial del Analista (que reproduzca los 4 escapes) + checker Arquitecto. maker!=checker.
Ambiguedad -> blocked + 1 pregunta concreta.
