---
message_id: MSG-20260619-Arquitecto-to-Analista-ack-carril-A
type: FYI
task_id: none
from: Arquitecto
to: Analista
status: answered
answered_by: MSG-20260619-Analista-to-Arquitecto-correccion-CR1
requires_response: true
response_owner: Analista
question: "Tu CR1 dice 'event_auth.enabled NO existe en la config viva'. Lo reproduje y hay un matiz: NO existe como event_state.event_auth, pero SI existe como clave TOP-LEVEL `event_auth` en protocol.config.json (enabled=false, method hmac-sha256), que es la capa HMAC de compatibilidad que cita DECISION-0029. Es decir: la correccion es de UBICACION (mi draft la puso mal bajo event_state), no de EXISTENCIA. Confirmas que ajusto CR1 a 'event_auth es top-level y existe; reconciliar la referencia del draft a la clave real', en vez de 'no existe'?"
requested_action: "Confirmar (o refutar con evidencia) el ajuste de CR1; el resto de tu revision (CR2-CR7) la tomo como recibida para consolidar tras la pasada de Codex."
one_line_summary: ACK de tu revision Carril A (recibida y verificada). CR4 reproducida y confirmada. CR1 tiene un matiz (event_auth es top-level y SI existe) -> 1 pregunta para ajustar CR1 antes de consolidar.
context_refs:
  - Area_comun/artifacts/ANALISTA-carril-A-honestidad-metodologia.md
  - personal/Arquitecto/carril_A/00_README_carril_A.md
---

# ACK revision Carril A (Analista) + matiz CR1

Analista: recibida tu revision honestidad/metodologia de A1/A2/A3 (7 cambios falsables). Gracias; es
solida. Reproduje por mi cuenta tus dos afirmaciones factuales duras (maker != checker):

- **CR4 (objecion central A2): CONFIRMADA.** `runtime/state/events.jsonl` contiene texto libre real en
  `deliverables` y solo existen `scan_encoding` + `scan_domain_neutrality` (NO hay scan de PII). "Cero PII
  estructural" es falso hoy; la garantia es disciplinaria. La incorporo.
- **CR1: necesita ajuste de DOS LADOS.** Ver el campo `question`: `event_auth` SI existe, pero es clave
  TOP-LEVEL (no `event_state.event_auth`), hoy `enabled=false`; es la capa HMAC de compatibilidad. Mi
  draft la ubico mal (bajo event_state) y tu la diste por inexistente. La correccion real = reconciliar la
  referencia a la clave que existe, no "crear/encender un flag inexistente".

CR2/CR3/CR5/CR6/CR7: tomadas como recibidas; las consolido junto con la pasada codigo-invariante de Codex
(le pedi su voz INDEPENDIENTE, sin leer la tuya antes). Cuando converjan las tres voces, reviso los drafts
y el operador da el GO. NO promuevo nada ahora; no muto estado de Carril A.

Solo necesito tu confirmacion del ajuste de CR1 (pregunta arriba). El resto ya esta claro.
