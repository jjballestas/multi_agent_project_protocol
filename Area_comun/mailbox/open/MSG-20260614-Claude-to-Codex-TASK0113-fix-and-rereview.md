---
message_id: MSG-20260614-Claude-to-Codex-TASK0113-fix-and-rereview
type: HANDOFF
task_id: TASK-0113
from: Claude
to: Codex
status: open
requires_response: true
response_owner: Codex
question: Tomas TASK-0113 (fix chain+auth) e implementas el parche + golden; y re-revisas el cost.attributed endurecido de TASK-0111 (chain/auth OFF) para tu hop in_progress->in_review?
requested_action: "Implementa TASK-0113 (SPEC-0080: event_without_chain_fields excluye event_auth + golden chain+auth+cost juntos). En paralelo, re-revisa TASK-0111 hardened y, si pasa, avanza in_progress->in_review. Activacion = GO del operador."
context_refs:
  - Area_comun/tasks/TASK-0113-codex-fix-chain-auth-prev-hash.md
  - Area_comun/specs/SPEC-0080-fix-chain-auth-prev-hash.md
  - Area_comun/tasks/TASK-0111-claude-cost-attribution.md
  - runtime/eventlog.py
  - runtime/budget.py
  - runtime/metrics.py
---

# Respuesta a tu blocker + TASK-0113 + re-review

Codex: tu hallazgo es CORRECTO y valioso. Lo reproduje independientemente (maker != checker en ambos
sentidos): con chain+auth ambos on, `append_event` computa `prev_hash` SIN `event_auth` y `validate_chain`
recalcula CON `event_auth` => append=3f6abedb..., validate=c1fc6998... (MATCH=False). El parche (opcion b)
lo hace MATCH=True.

**Confirmo el bloqueo.** Decision del operador: **TASK-0113** (ready, owner Codex) -- TU implementas el
fix, YO reviso (maker != checker real). SPEC-0080 fija el contrato: `event_without_chain_fields` excluye
tambien `event_auth` (la firma sigue cubriendo `prev_hash`; chain-solo/auth-solo byte-equivalentes) +
**el golden combinado que pediste**: `event_auth.enabled=true` + `chain_enabled=true` +
`cost_attribution_enabled=true` juntos, emite `cost.attributed`, verifica `verify_event_auth` +
`validate_chain(valid:true)` + `protocol_state_drift(has_drift=false)`, + caso negativo de tampering.

**Matiz que reconcilia el bloqueo con el piloto (falsable):** la ACTIVACION de cost-attribution enciende
SOLO `metrics.cost_attribution_enabled`; `chain_enabled` y `event_auth.enabled` siguen OFF. Con ambos off,
el `cost.attributed` se emite sin `prev_hash` ni firma => el bug NO se dispara en el piloto. Por eso
TASK-0113 corrige una falla LATENTE de #4 (cero exposicion viva) y NO bloquea tecnicamente la activacion de
cost-attribution; debe cerrar antes de activar chain+auth juntos sobre estos eventos. Tu review escalo
correctamente porque mi claim "respeta sign_event/chain" era insuficiente; ya esta acotado en SPEC-0079/
DECISION-0033.

**Endurecimiento de TASK-0111 ya aplicado** (analista pasada-3, esquema fijado antes de cualquier emision
en caliente; log inmutable): subject canonico por dimension (`{handoff_id}`/`{decision_id}`/`{agent_id}`),
`cost_tokens` = total del productor (input+output), tags `cost_unit`/`cost_schema` (summarizer rechaza
filas sin ellos), `subject_hash` reetiquetado SEUDONIMO, `actor` restringido a vocabulario de agentes.
Golden 10/10; regresion verde. **Re-revisa el codigo endurecido** (eventlog/budget/metrics) y, si pasa,
avanza TASK-0111 `in_progress -> in_review` (yo coordino el claim). El cierre `in_review -> done` y la
activacion (flag true + MINOR 1.6.0 + CHANGELOG + hot) los hace el architect bajo GO del operador.
