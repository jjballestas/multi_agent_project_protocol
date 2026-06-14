---
message_id: MSG-20260614-ClaudeAnalista-to-Operador-pasada-3-cost-attribution
type: REVIEW
task_id: TASK-0111
from: Claude-analista
to: Operador
status: answered
requires_response: false
response_owner: Operador
answered_by: Claude (architect, por delegacion del operador)
answered_ref: Area_comun/mailbox/answered/MSG-20260614-Claude-to-ClaudeAnalista-cierre-review-pasada-3.md
one_line_summary: Pasada adversarial acotada sobre #3 (cost-attribution) entregada. Veredicto pre-GO = GO CON UN CAMBIO, no GO liso. Lente metodologia/investigacion. 4 puntos respondidos PASA/CAMBIO/RIESGO.
requested_action: "Decision de GO en caliente: revisar artifacts/ANALISTA-pasada-adversarial-3-cost-attribution.md. Bloqueante antes de activar (log inmutable): (1) tag cost_unit+cost_schema en payload; (2) contrato canonico de subject. No bloqueante para el piloto: (3) reetiquetar subject_hash=seudonimo + acotar actor; (4) byte-equiv sobre log poblado + caso en-caliente con conteo real."
context_refs:
  - Area_comun/artifacts/ANALISTA-pasada-adversarial-3-cost-attribution.md
  - Area_comun/decisions/DECISION-0033-cost-attribution-por-handoff.md
  - Area_comun/specs/SPEC-0079-cost-attribution-por-handoff.md
  - examples/runtime_cost_attribution_cases/run_runtime_cost_attribution_cases.py
---

# Pasada adversarial #3 (cost-attribution) -- entregada

Operador:

Una sola pasada, lente investigacion/metodologia (no re-verifico ingenieria; eso ya lo cubren arquitecto
+ Codex). Falsable, sin re-arquitectura. Veredicto: **GO CON UN CAMBIO DE ESQUEMA, no GO liso** -- porque
el event log es append-only/inmutable (replay + #4) y el formato que actives ahora es el que analizaras
para H2 y no podras retro-corregir.

Por punto (detalle y asertos en el artefacto):

1. **Fitness H2 (Deltatokens/handoff): PASA** para ese endpoint (subject_hash invariante a la condicion da
   apareamiento; by_handoff preserva la unidad). Metrica que NO produce: split input/output por handoff
   (cost_tokens es escalar opaco; irrecuperable despues sobre log inmutable). CAMBIO: canonizar `subject`
   por dimension (el golden hoy usa formas inconsistentes) + fijar semantica de cost_tokens.

2. **GATE-DATASET: campo senalado = `subject_hash` (seudonimo, NO anonimo** bajo RGPD/Ley 1581; payload
   retenido ? re-identificable). Secundario: `actor` si alguna vez es id humano. CAMBIO: reetiquetar como
   seudonimo, acotar actor a vocabulario de agentes, romper enlace para publicar. "publicable" se reformula.

3. **Honestidad: NO ninguno.** Excesos: (a) "medicion en caliente" sobreestima un REGISTRO de cifra
   inyectada (golden usa literales; fuente/unidad sin especificar); (b) "byte-equivalente" solo probado en
   log inexistente, no en log poblado. Confirmo que NO se exceden: no promete dolares/economia (dice tokens),
   no reclama ocap (la integridad applied:false/replay==hot SI esta testada).

4. **Retrofit (3.4): UN cambio antes de activar = tag `cost_unit`+`cost_schema` en el payload.** Seguro mas
   barato contra el arrepentimiento mas caro: sin el, filas historicas quedan auto-ambiguas para siempre.

Minimo para tu GO: (1)+(2) bloqueantes (inmutables); (3)+(4 byte-equiv/caliente) endurecen sin bloquear el
piloto. No consolido ni decido; no mute estado autoritativo. El arquitecto entra por submit_intent si lo
incorporas.
