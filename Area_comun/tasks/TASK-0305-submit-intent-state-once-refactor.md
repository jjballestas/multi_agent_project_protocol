---
task_id: TASK-0305
file: Area_comun/tasks/TASK-0305-submit-intent-state-once-refactor.md
title: "Refactor submit_intent: verificar el log UNA vez por submit (quitar el multiplicador 3x/(N+2)x) - atestacion-neutral"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: normal
depends_on: []
relates_to:
  - TASK-0303
created_at: 2026-07-29
intake:
  type: infra
  goal: >
    Quitar la re-verificacion redundante del log completo DENTRO de un mismo submit. Hoy cada submit_intent
    recomputa state() -- una re-verificacion crypto (HMAC + ed25519) del log ENTERO (~6000 eventos, ~10.5s
    medidos) -- ~3 veces por intent individual (chequeo de idempotencia + append_event que llama self.state()
    en runtime/eventlog.py:879, + write_snapshot que llama rebuild_snapshot en :1114 = otra pasada completa) y
    (N+2) veces por transaccion de N intents (cada iteracion del loop llama self.state()). De ahi los ~30s por
    intent y el "cuelgue al cerrar" (que es el rebuild_snapshot final, no un hang real). Calcular el estado
    verificado UNA sola vez por submit y pasarlo (thread-through) a append/claim/apply y a la construccion del
    snapshot final, de modo que la verificacion completa corra A LO SUMO UNA VEZ por submit. ATESTACION-NEUTRAL:
    verifica exactamente los mismos eventos y produce salida BYTE-IDENTICA (mismos eventos, mismo snapshot
    canonical_hash, mismo resultado de validate). NO cambia QUE ni COMO se verifica, NO toca la verificacion
    incremental entre submits (eso es DECISION-0105, aparte), NO toca protocol.config.json ni el genesis.
  acceptance:
    - "AC1: dentro de un submit_intent (individual o --intents), la verificacion completa del log (replay_events sobre todos los eventos) corre A LO SUMO UNA VEZ; append_event/apply_intent/acquire_claim REUTILIZAN el estado ya computado en vez de re-llamar self.state() (runtime/eventlog.py:879/1063/1087); el snapshot final se construye desde ese estado, no con un rebuild_snapshot de replay completo (runtime/eventlog.py:1114)."
    - "AC2 (SALIDA IDENTICA -- EL vector critico): un test diferencial prueba que, para la MISMA secuencia de intents desde la misma base, el camino refactorizado produce resultado BYTE-IDENTICO al actual -- mismo tail de events.jsonl (mismos seq, prev_hash, firmas HMAC y ed25519), mismo snapshot.json (canonical_hash + up_to_seq), y validate_collaboration_state.py + validate_chain verdes. CERO cambio de atestacion o comportamiento."
    - "AC3 (falsabilidad): un test que FALLARIA si el refactor saltara la verificacion de un evento nuevo o reutilizara un estado obsoleto -- p.ej. un evento manipulado sigue siendo detectado; y el 2o intent de una transaccion VE el estado producido por el 1o (validacion encadenada intra-tx intacta)."
    - "AC4 (perf, observable): un submit de 1 intent hace 1 verificacion completa, no ~3; el tiempo de pared baja ~3x sobre el log actual (~6000 eventos). Reportar antes/despues. Es la ganancia observable, pero AC2 es el gate."
    - "AC5 alcance: solo runtime/eventlog.py + runtime/submit_intent.py (+ el test). protocol.config.json BYTE-IDENTICO. Sin genesis/re-genesis. Override event-state sin cambios. Gates hub verdes."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - runtime/eventlog.py
    - runtime/submit_intent.py
  out_of_scope: >
    Verificacion incremental ENTRE submits / sembrar el replay desde el snapshot como limite de confianza (eso
    es DECISION-0105 / palanca B, exige decision + diseno de seguridad). La compactacion fisica del log
    (compact_through, palanca C). Podar el event log. Cualquier cambio en QUE se verifica o en la cadena #4.
    Producto Zeus.
  risk: medium
  estimate: M
notes: >
  Origen: diagnostico del roce operativo reportado 2026-07-29 (submit_intent O(n) por el log; ~30s/intent). Es la
  palanca A (refactor atestacion-neutral, SIN DECISION) del plan A->B->C. Quita el multiplicador; B (DECISION-0105)
  hace O(nuevos) el caso general. RIESGO: toca el motor del ledger -- la seguridad esta en el test diferencial de
  salida IDENTICA (AC2) + el gate adversarial de 2 capas. El gate offline (validate_chain) sigue siendo la frontera
  dura: re-verifica todo en cada commit, asi que un refactor con bug se caza ahi.
---

# TASK-0305 - submit_intent: verificar el log una vez por submit (refactor atestacion-neutral)

## Contexto
Cada submit_intent re-verifica las firmas del log ENTERO (~6000 eventos, ~10.5s) en cada llamada a state(), y
state() se llama ~3x por intent (idempotencia + append + snapshot) -> ~30s/intent; el "cuelgue al cerrar" es el
rebuild_snapshot final. El snapshot (up_to_seq + canonical_hash) ya existe pero no se usa para acotar coste.

## Que hacer
Computar el estado verificado UNA vez por submit y pasarlo (thread-through) a append_event/apply_intent/
acquire_claim (runtime/eventlog.py:879/1063/1087) y a la construccion del snapshot final (evitar el
rebuild_snapshot de :1114). Verificacion completa <= 1 vez por submit.

## Como probarlo (lo critico)
Test DIFERENCIAL: misma secuencia de intents por el camino actual y el refactorizado -> salida BYTE-IDENTICA
(events tail con mismos seq/prev_hash/firmas, snapshot canonical_hash + up_to_seq, validate + validate_chain
verdes). Mas un test de falsabilidad (evento manipulado sigue detectado; encadenamiento intra-tx intacto).

## No hacer
No tocar QUE se verifica ni la cadena #4. No sembrar desde el snapshot entre submits (DECISION-0105). No
compactar el log. protocol.config.json byte-identico, sin re-genesis. Fondo intocable.
