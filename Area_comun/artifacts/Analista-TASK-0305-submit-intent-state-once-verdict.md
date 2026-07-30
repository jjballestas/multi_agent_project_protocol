# VEREDICTO ADVERSARIAL -- TASK-0305 (submit_intent: verificar el log una vez por submit)

- Reviewer: Analista (voz independiente / checker adversarial)
- Fecha local: 2026-07-30 02:23 +02:00
- Ancla canonica: hub @625ab32 (impl; entrega 608a61b), padre 8873a5f. Protocol HEAD a6a9236.
- Modo: clon LIMPIO a ruta corta D:/Aegis_Scratch/protocol/r0305, checkout 625ab32, gates por EXIT code.
- Recomendacion de cierre: **OK-CLOSABLE**

## 1. Que revise (el motor del ledger -- maxima rigurosidad)

El refactor enhebra un `verified_state` por submit: 1 verificacion completa inicial (`writer.state()` =
`replay_events` sobre TODO el log), y luego cada evento nuevo avanza el estado incrementalmente via
`replay_events([event], base_state=verified_state)`; el snapshot final se construye desde ese estado
(`up_to_seq` del ultimo evento + `deepcopy(state)` + `canonical_hash`) en vez de `rebuild_snapshot`
(full replay). El fallback `verified_state=None` conserva el comportamiento original.

NO me fie del test del autor: ademas de correrlo, construi mi PROPIO oraculo diferencial e independiente,
sembrado desde el LEDGER REAL (6101 eventos del clon), comparando el camino enhebrado contra (a) el camino
legacy (`verified_state=None`, full replay por op) y (b) `rebuild_snapshot` (full replay independiente).

## 2. Reproduccion (exit codes reales, clon limpio)

| Paso | Comando | Exit |
|------|---------|------|
| Clon + checkout | `git clone file://... r0305 && git checkout 625ab32` | limpio |
| Config byte-identico vs PADRE (AC5) | `git diff 625ab32~1 625ab32 -- protocol.config.json` | vacio (identico) |
| Alcance (AC5) | `git diff --name-only 625ab32~1 625ab32` (excl. state/mailbox/tasks/handoffs) | solo eventlog.py + submit_intent.py + test |
| Test del autor | `python -m unittest tests.test_submit_intent_state_once` | 0 (2 tests OK) |
| VALIDATE (validate_chain full = frontera dura) | `python scripts/validate_collaboration_state.py` | 0 |
| scan_encoding | `python scripts/scan_encoding.py` | 0 |
| scan_domain_neutrality | `python scripts/scan_domain_neutrality.py` | 0 |
| Diferencial propio (4 vectores, sembrado del ledger real) | `python harness0305.py` | ver seccion 3 |

Nota: secrets/ (claves HMAC/ed25519) no estan en git (correcto); los copie del hub vivo al clon para
poder firmar/verificar y reproducir byte-a-byte.

## 3. AC2 -- IDENTIDAD BYTE-A-BYTE (el vector critico): vector por vector

Oraculo: en cada vector, sembre DOS raices identicas desde el ledger real (6101 ev), conduje el camino
legacy (full replay por op) y el enhebrado, y compare (A) events.jsonl byte-a-byte legacy==thread,
(B) snapshot.json byte-a-byte legacy==thread, (C) snapshot enhebrado == `rebuild_snapshot`
(full replay: canonical_hash + up_to_seq + state).

| Vector | (A) events byte==| (B) snapshot byte== | (C) == rebuild_snapshot (full replay) |
|--------|------------------|---------------------|----------------------------------------|
| plain-multi (aggregate repetido, visibilidad intra-tx) | PASS | PASS | PASS (hash+seq+state) |
| claims-fencing (acquire_claim x2 -> fencing/leases) | PASS* | PASS | PASS (hash+seq+state) |
| stale-fencing-reject (apply_intent token viejo -> rejection + token valido) | PASS* | PASS | PASS (hash+seq+state) |
| idempotent-reapply (misma idempotency_key 2x -> no re-append, no doble avance) | PASS | PASS | PASS (hash+seq+state) |

(*) En claims/apply, events.jsonl legacy vs thread difirio SOLO en `ts` (reloj de pared no fijado en mi
arnes) y su cascada derivada (`event_auth` HMAC firma sobre ts, `prev_hash` encadena el evento firmado).
Lo demostre falsablemente: la union de campos distintos fue exactamente {ts, event_auth, prev_hash};
CERO campo portador de estado difirio (fencing_token, aggregate_version, owner, lease, payload,
idempotency_key identicos). Al FIJAR `ts` (monkeypatch de `utc_now`), events.jsonl quedo byte-identico
legacy==thread tambien. El refactor NO toca la construccion/firma del evento; solo cambia que `state`
se usa para idempotencia/fencing y como se arma el snapshot. La identidad de ESTADO (snapshot) es
byte-identica y coincide con full replay en los 4 vectores.

El test del autor (diferencial legacy-vs-thread byte-a-byte de events.jsonl + snapshot.json +
validate_chain verde + aggregate_version==2 intra-tx) tambien pasa (exit 0).

## 4. AC3 -- falsabilidad (los eventos NUEVOS siguen verificandose)

- TAMPER: manipule el payload de un evento nuevo recien enhebrado y `rebuild_snapshot` (full replay)
  lo RECHAZA (`security.unauthenticated_event` en rejections) y cambia el canonical_hash. PASS.
- Encadenamiento intra-tx: en el vector stale-fencing, el 2o apply VE fencing=1 producido por el claim
  del 1o; el re-acquire incrementa fencing -- ambos coinciden con full replay. PASS.
- `replay_events([event], base_state=...)` corre `verify_event_auth`/`verify_actor_auth` sobre el evento
  nuevo (mismo codigo de verificacion). La confianza en `base_state` esta ACOTADA a un submit (el base se
  verifico completo una vez al inicio via `writer.state()`); la confianza incremental ENTRE submits es
  fuera de alcance (DECISION-0105). La frontera dura offline (`validate_collaboration_state` ->
  `validate_chain` full sobre TODOS los eventos, cada commit) quedo verde en clon limpio.

## 5. AC5 -- alcance / fallback intacto

- git diff 625ab32~1..625ab32 (excl. rutas de estado/mailbox/tareas): SOLO runtime/eventlog.py +
  runtime/submit_intent.py + tests/test_submit_intent_state_once.py.
- protocol.config.json byte-identico vs PADRE (diff vacio) y vs main; sin genesis/re-genesis; genesis
  seq 1 no tocado.
- Fallback: `grep` de callers -- SOLO submit_intent.py pasa `verified_state`. apply.py,
  protocol_replay.py, regenesis.py llaman sin arg -> rama `None` (full replay original), intacta.
  Mi camino legacy en el arnes ES esa rama y produjo resultado identico a full replay.

## 6. AC1 / AC4 -- verificacion unica + perf

- AC1: el test del autor con un contador parcheado de `EventWriter.state` asevera `calls==1` por submit
  enhebrado (1 verificacion completa). Consistente con el diseno (state() una vez, avance incremental,
  snapshot sin rebuild).
- AC4 (observable, no es el gate): medido en el ledger real (6101 ev): `write_snapshot` enhebrado 0.257s
  vs `rebuild_snapshot` legacy 14.91s (~58x en ese paso); verificaciones completas por intent ~3 -> 1
  (~3x global). Direccion consistente con lo reportado por el autor (96.76s -> 39.79s, ~2.4x). El
  multiplicador exacto depende del tamano del log y la mezcla de ops.

## 7. Residuales declarados (honestos)

1. Mi diferencial ejercita la costura EXACTA que el refactor cambia (append_event/acquire_claim/
   apply_intent/write_snapshot, enhebrado vs None) sembrado del ledger real. NO conduje el CLI
   top-level `submit_intent()`/`submit_intents()` end-to-end contra el ledger real (mutaria estado
   compartido y exige intents con capabilities validas). El enhebrado top-level es delgado
   (`verified_state = writer.state()` pasado a los mismos metodos que si probe); la identidad de
   estado/snapshot que produce esta cubierta por el oraculo. El fallback genesis-ref recomputa
   `verified_state = writer.state()` tras recrear el writer (reset correcto). Riesgo residual bajo.
2. La confianza incremental es intra-submit por diseno; la frontera dura sigue siendo validate_chain
   offline (re-verifica todo cada commit). No es un slip; es el contrato (DECISION-0105 aparte).
3. El multiplicador de perf es dependiente del tamano del log/mezcla de ops; ~2.4x es representativo.

## 8. Veredicto

Los 5 AC pasan. Identidad byte-a-byte confirmada por mi propio oraculo independiente (snapshot ==
full replay en los 4 vectores de divergencia: plain/claims-fencing/stale-fencing/idempotencia; events
byte-identicos, con la unica diferencia ts-cascade en claims probada no-portadora-de-estado y cerrada
al fijar ts). Eventos nuevos siguen verificandose (tamper detectado). Alcance limpio (2 rutas + test),
config byte-identico, sin genesis/cadena. Fallback intacto. Gates hub (validate/validate_chain,
scan_encoding, scan_domain_neutrality) exit 0 en clon limpio.

**OK-CLOSABLE.** Sin caso de divergencia incremental-vs-full hallado. -- Analista
