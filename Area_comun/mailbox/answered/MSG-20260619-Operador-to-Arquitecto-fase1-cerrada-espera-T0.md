---
message_id: MSG-20260619-Operador-to-Arquitecto-fase1-cerrada-espera-T0
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: FASE 1 CERRADA (verificado en canonico b415b4d por el asistente): #4 ON canonico-limpio + Carril B pieza 1 connector DONE. Versionado-bajo-#4 = DECISION batcheada, SIN re-genesis ahora. HOLD FASE 2: el protocolo queda EN ESPERA del handover del diseno de la DB, que sera el primer handoff gobernado = T0. No arrancar FASE 2 hasta T0.
requested_action: "(a) Dar por CERRADA FASE 1 (#4 ON + Carril B pieza 1 done, verificados). (b) Versionado-bajo-#4: abrir DECISION de POLITICA (protocol_version = version de epoca del genesis, solo cambia en re-genesis-boundary; release/capacidad en CHANGELOG/manifest fuera del config); NO bumpear ni re-genesis ahora; batchear. (c) HOLD FASE 2: NO arrancar perfil financiero / connector uso-vivo / Git / CI / skills, y NO reactivar Codex para Carril B, hasta que yo entregue el diseno de la DB como primer handoff gobernado (T0). Quedar a la espera."
question: "Confirmas FASE 1 cerrada + versionado como DECISION batcheada (sin re-genesis) + HOLD de FASE 2 hasta el handover del diseno de la DB (T0)?"
context_refs:
  - Area_comun/decisions/DECISION-0045-boundary-t0-sello-pre-t0.md
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
  - Area_comun/decisions/DECISION-0041-precondicion-acoplamiento-readonly.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
validation_refs:
  - "Asistente verifico en canonico b415b4d (clon fresco): 4 flags #4 true; validate_collaboration_state --root . SIN secretos exit 0; protocol_state_drift has_drift=False; validate_chain valid + firmas validas + anclas validas; TASK-0117 done; TASK-0121 done; golden connector exit 0 (7 deny-by-default); connectors/ sin dominio; scan_domain_neutrality exit 0. cfg pinned 1.14.0."
deadline_or_blocking_level: normal
---

# FASE 1 cerrada; protocolo en espera del handover de la DB (= T0). HOLD FASE 2

Verifique en canonico (b415b4d, clon fresco) - todo verde de forma independiente:

## FASE 1 - CERRADA
- **#4 ON canonico-limpio:** 4 flags true; `validate --root .` **sin secretos exit 0** (invariante
  DECISION-0046 sostiene); drift 0 (`has_drift=False`); chain/firmas/anclas validas; TASK-0117 done.
- **Carril B pieza 1 DONE:** TASK-0121 done; golden connector exit 0 (7 vectores deny-by-default);
  `connectors/` sin dominio; off-by-default; `connectors.config.json` fuera del config.

## Versionado bajo #4 - politica, no parche
Confirmo tu hallazgo: el genesis pinea `canonical_hash(protocol.config.json)`, asi que el config quedo
inmutable-sin-ceremonia. **No bumpees ni re-genesis ahora.** Abre una **DECISION de politica**:
`protocol_version` = version de EPOCA del genesis (solo cambia en re-genesis-boundary, batcheado, en su
propia ventana); la version de **release/capacidad** vive en CHANGELOG/manifest fuera del config. Asi el
`[1.15.0]` del CHANGELOG y el `1.14.0` vivo se reconcilian sin mentir. Capacidades nuevas siguen fuera del
config (como connectors).

## HOLD FASE 2 - el protocolo espera el handover de la DB (= T0)
El requisito duro ya se cumplio: **#4 ON antes del primer handoff**. No hace falta - y no quiero - cramear
toda FASE 2 antes del lanzamiento. Por tanto:
- **NO arranques** perfil financiero, uso vivo del connector, Git, CI ni skills. **NO reactives Codex**
  para Carril B. Carril B pieza 1 queda cerrada/off-by-default.
- El protocolo queda **EN ESPERA** de que yo entregue el **diseno de la DB** (lo termino y testeo aparte);
  ese **handover sera el primer handoff gobernado = T0**, atestado en caliente bajo #4.
- **Tras T0**, jalamos en orden y de a una: §9 read-only verificada por Codex (DECISION-0041) + mi GO de
  uso vivo del connector -> perfil financiero (`profiles/financiero_presupuesto/`, fuera del core) ->
  modulos (Seguridad, Presupuesto) con handoffs atestados.

## Gates (compliance)
PII de terceros NUNCA al event log (handoffs por id/hash; DECISION-0040). DEF-PII (TASK-0118) diferida
hasta antes de captura/publicacion. Nada mas alla de #4 sin GO nuevo. Una sola ventana de riesgo a la vez.
Piloto/ceremonia #4 nunca contra el log vivo (DECISION-0045). Codex y crons como esten; sin nuevo trabajo
de Carril B. Canal ASCII.
