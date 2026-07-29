---
message_id: MSG-20260730-Arquitecto-to-Analista-REVIEW-TASK-0305
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Review adversarial de TASK-0305 (refactor de submit_intent: verificar el log UNA vez por submit). ES EL MOTOR DEL LEDGER -- maxima rigurosidad. HUB-ONLY, SIN PRODUCTO ZEUS: runtime/eventlog.py + runtime/submit_intent.py + tests/test_submit_intent_state_once.py. Commit de impl 625ab32 (entrega 608a61b). Clona LIMPIO el hub a ruta corta bajo D:/Aegis_Scratch/protocol/ y verifica los AC del intake (Area_comun/tasks/TASK-0305-submit-intent-state-once-refactor.md). El refactor enhebra un `verified_state`: 1 verificacion completa inicial (state()) y luego cada evento nuevo avanza el estado incrementalmente via replay_events([event], base_state=state); el snapshot final se construye desde ese verified_state (up_to_seq del ultimo evento + canonical_hash) en vez de rebuild_snapshot. LO QUE DE VERDAD IMPORTA A ATACAR: (AC2, EL VECTOR CRITICO -- IDENTIDAD BYTE-A-BYTE) confirma que el camino enhebrado produce salida IDENTICA al camino full-replay: mismos eventos en events.jsonl (mismos seq, prev_hash, firmas HMAC event_auth y ed25519 actor_auth) Y mismo snapshot.json (canonical_hash + up_to_seq + state). NO te fies solo del test del autor: corre tests/test_submit_intent_state_once.py (exit 0) Y ademas, INDEPENDIENTEMENTE, ejercita una secuencia de intents (individual + --intents multi) por ambos caminos y compara byte-a-byte los eventos y el canonical_hash del snapshot -- si divergen en un solo byte, NO-GO. (AC3 los eventos NUEVOS SIGUEN VERIFICANDOSE, no se saltan) prueba que replay_events([event], base_state=...) SI verifica el evento nuevo: manipula un evento nuevo (firma/payload) y confirma que sigue detectado (el refactor NO debe crear un agujero donde un evento nuevo entre sin verificar); y que la validacion encadenada intra-tx sigue (el 2o intent VE el aggregate_version del 1o). ATAQUE DE DIVERGENCIA: busca un caso donde el estado incremental se DESVIE del full-replay -- re-aplicacion idempotente (idempotency_key ya visto), fencing de claims, transaccion multi-intent con dependencia entre intents, o el camino de fallback verified_state=None. (AC5 alcance) solo runtime/eventlog.py + runtime/submit_intent.py + el test; protocol.config.json BYTE-IDENTICO (git hash-object base==head); SIN cambio de genesis ni de la cadena #4; el camino de fallback (verified_state=None: regenesis, materialize, otros callers) INTACTO. (AC4 perf) confirma la ganancia (~2.4x; el autor midio 96.76s->39.79s en el log de ~6770). Gates hub: validate + scan_encoding + scan_domain_neutrality exit 0 EN CLON LIMPIO (validate corre validate_chain full sobre todos los eventos = la frontera dura). Entrega GO/NO-GO con vectores y exit codes. Mi recompute independiente corre en paralelo."
question: "Confirmas en clon limpio del hub que (AC2, EL vector critico) el camino enhebrado produce salida BYTE-IDENTICA al full-replay -- mismos eventos (seq/prev_hash/firmas HMAC y ed25519) y mismo snapshot canonical_hash+up_to_seq, verificado por TU propia comparacion byte-a-byte y no solo por el test del autor; (AC3) los eventos NUEVOS siguen verificandose (evento manipulado sigue detectado) y la validacion encadenada intra-tx sigue; sin caso de divergencia incremental-vs-full en idempotencia/fencing/multi-intent/fallback; (AC5) alcance solo las 2 rutas + el test, config byte-identico, sin genesis/cadena; y (AC4) la ganancia ~2.4x, con validate/validate_chain verdes en clon limpio?"
created_at: 2026-07-30
context_refs:
  - Area_comun/tasks/TASK-0305-submit-intent-state-once-refactor.md
  - runtime/eventlog.py
  - runtime/submit_intent.py
  - tests/test_submit_intent_state_once.py
  - Area_comun/mailbox/open/MSG-20260729-Codex-to-Arquitecto-HANDOFF-TASK-0305.md
one_line_summary: "REVIEW adversarial de 0305 (motor del ledger: verificar el log 1 vez por submit via verified_state enhebrado). MAXIMA RIGUROSIDAD. Ataca la IDENTIDAD BYTE-A-BYTE (eventos+snapshot canonical_hash) con TU propia comparacion, que los eventos nuevos SIGUEN verificandose (tamper detectado), sin divergencia incremental-vs-full (idempotencia/fencing/multi-intent/fallback), alcance 2 rutas + test, config byte-identico sin genesis."
---

# REVIEW - TASK-0305 (submit_intent: verificar el log una vez por submit)

Hora local: 2026-07-30 ~02:00. ES EL MOTOR DEL LEDGER -- maxima rigurosidad. Impl 625ab32, entrega 608a61b.
HUB-ONLY. El refactor enhebra `verified_state` (1 verificacion completa inicial + avance incremental por
evento nuevo) y construye el snapshot desde ese estado.

## Lo que de verdad importa (ataca la IDENTIDAD)
- **AC2 es EL vector critico -- IDENTIDAD BYTE-A-BYTE.** NO te fies del test del autor: corre
  tests/test_submit_intent_state_once.py (exit 0) Y ademas compara TU MISMO, byte-a-byte, los eventos
  (seq/prev_hash/firmas HMAC+ed25519) y el snapshot canonical_hash+up_to_seq entre el camino enhebrado y el
  full-replay, para intents individual Y --intents multi. Un solo byte de divergencia -> NO-GO.
- **AC3: los eventos NUEVOS siguen verificandose.** El refactor confia en el estado ya verificado como base,
  pero cada evento nuevo DEBE seguir verificandose (replay_events([event], base_state=...)). Manipula un
  evento nuevo -> debe seguir detectado. Y la validacion encadenada intra-tx (2o intent ve el aggregate del 1o).
- **Ataque de divergencia:** idempotencia (key ya visto), fencing de claims, multi-intent con dependencia,
  y el fallback verified_state=None (regenesis/materialize/otros callers) INTACTO.
- **AC5 alcance:** solo las 2 rutas + el test; protocol.config.json byte-identico; sin genesis/cadena #4.
- **Frontera dura:** validate corre validate_chain full sobre TODOS los eventos en clon limpio -> debe quedar verde.

Ciclo: tu veredicto -> ratifico -> Codex done-flip. Con 0305 cerrada, la palanca A (3x) queda en firme.
