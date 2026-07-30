# VEREDICTO ADVERSARIAL -- TASK-0306 (palanca B: checkpoint firmado + verificacion incremental)

- Reviewer: Analista (voz independiente / checker adversarial)
- Fecha local: 2026-07-30 06:23 +02:00
- Ancla canonica: hub @4540f5b (protocol HEAD == origin/main). Impl 18c175f; entrega 3df7135; padre del impl 4024481.
- Modo: clon LIMPIO a ruta corta D:/Aegis_Scratch/protocol/r306, checkout 4540f5b, gates por EXIT code.
- Recomendacion de cierre: **OK-CLOSABLE**

## 1. Que revise (cambia el modelo de confianza del camino VIVO -- maxima rigurosidad)

El refactor firma el snapshot como CHECKPOINT: `snapshot.json` gana `integrity` = HMAC-SHA256 con la clave
de INSTANCIA `runtime` (`runtime-hmac:v1`) sobre la tupla canonica `(canonical_hash(state), up_to_seq,
prev_hash@up_to_seq)`. En el camino vivo, `EventWriter.state()` llama `verify_snapshot_checkpoint(...)`:
si es de CONFIANZA, siembra `base_state` desde el `state` del checkpoint y verifica SOLO `seq > up_to_seq`;
si NO, cae a `replay_events(TODOS)` (verificacion completa). `verify_snapshot_checkpoint` devuelve
`trusted:False + reason` para cada caso invalido.

NO me fie del banco del autor: ademas de correrlo, escribi mi PROPIO arnes adversarial independiente
(`_adv_review.py`, fixture propio con clave distinta, mezcla de eventos mas rica que la del autor:
2 tareas, rechazo por fencing stale, dedupe idempotente) y ataque los AC con payloads NUEVOS, incluida
la fuga central que el instructor teme (state manipulado con `canonical_hash` almacenado recomputado).

## 2. Reproduccion (exit codes reales, clon limpio)

| Paso | Comando | Exit |
|------|---------|------|
| Clon + checkout | `git clone file://... r306 && git checkout 4540f5b` | limpio |
| Config byte-identico vs PADRE del impl (AC5) | `git diff 18c175f~1 18c175f -- protocol.config.json` | vacio (identico) |
| Config NO en la lista de archivos del impl (AC5) | `git show --name-only 18c175f \| grep config` | NONE |
| K_max FUERA del config pineado (AC5) | `grep max_incremental_events protocol.config.json` | ausente (esta en runtime/CHECKPOINT_POLICY.json) |
| Banco del autor | `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` | 0 (6 casos) |
| VALIDATE (validate_chain full = frontera dura, AC4) | `python scripts/validate_collaboration_state.py` | 0 |
| scan_encoding | `python scripts/scan_encoding.py` | 0 |
| scan_domain_neutrality | `python scripts/scan_domain_neutrality.py` | 0 |
| Arnes adversarial propio (31 checks) | `python _adv_review.py` | 0 (31/31 PASS) |

Nota: `.protocol-secrets/` (claves HMAC/ed25519) no esta en git (correcto). El clon limpio NO tiene la
clave `runtime` -> sobre el snapshot VIVO, `verify_snapshot_checkpoint` cae a `unresolved_key` -> full
(fail-safe correcto ante ausencia de material). El banco y mi arnes traen su PROPIA clave de fixture,
asi ejercitan de verdad la rama de CONFIANZA + toda la familia de invalidos.

## 3. AC3 -- FAIL-SAFE airtight (EL vector critico): familia completa, por vector

Para CADA caso invalido verifique DOS cosas: (i) `verify_snapshot_checkpoint` devuelve `trusted:False`
con el `reason` esperado; (ii) el CALLER REAL (`EventWriter.state()`, la misma ruta que usa
`submit_intent` via `writer.state()`) verifica TODOS los eventos -- parchee `verify_event_auth` con un
contador y aseveree `verified_seqs == [todos los seq]`. NUNCA un skip.

| Vector de ataque (payload propio) | reason | CALLER hace full de TODOS |
|-----------------------------------|--------|---------------------------|
| integrity ausente | missing_integrity | SI |
| method no soportado (ed25519) | unsupported_method | SI |
| firma integrity corrupta (0*64) | invalid_signature | SI |
| key_id cambiado (v2) | key_id_mismatch | SI |
| state manipulado, canonical_hash ALMACENADO viejo | state_hash_mismatch | SI |
| **state manipulado + canonical_hash almacenado RECOMPUTADO, integrity vieja** | checkpoint_metadata_mismatch | SI |
| **state manip + hash almacenado + integrity.canonical_hash actualizados, SIN re-firmar** | invalid_signature | SI |
| **state manip + RE-FIRMADO con secreto EQUIVOCADO (clave atacante)** | invalid_signature | SI |
| up_to_seq mas alla del head | checkpoint_out_of_range | SI |
| integrity.prev_hash manipulado | checkpoint_metadata_mismatch | SI |
| stale real (head-up_to_seq > K_max, K_max=1) | stale_checkpoint | SI |

Los 3 vectores en negrita son la fuga que el instructor pidio refutar. CONFIRMADO que el check RECOMPUTA
`canonical_hash(stored['state'])` y lo compara contra el `canonical_hash` almacenado (eventlog.py:778-780);
un `state` manipulado con `canonical_hash` almacenado "arreglado" NO cuela: la tupla firmada (integrity)
sigue sin casar -> `checkpoint_metadata_mismatch` (integrity vieja) o `invalid_signature` (si tambien se
tocan los campos de integrity pero sin el secreto). Forjar exige el secreto de instancia -> es el modelo
de confianza declarado (HMAC simetrica), respaldado por AC4 (frontera dura offline). SUMMARY: cada
invalido -> verificacion COMPLETA, cero skip.

## 4. AC4 -- gate offline NO debilitado (evento VIEJO manipulado sigue cazado)

- Con checkpoint VALIDO, manipule un evento VIEJO (`seq <= up_to_seq`, el primero con owner) -> el camino
  VIVO SIGUE confiando en el checkpoint (siembra por encima del evento viejo; ES la razon de ser de la
  frontera offline). Esto es esperado, no un slip.
- `validate_chain(tampered)` offline lo CAZA: `valid = False`. El evento viejo manipulado rompe la cadena
  `prev_hash` / firma. PASS.
- El manipular perturba el estado de full-replay (`clean_state != tam_state`) -> ademas `assert_snapshot_matches`
  (que el validador real invoca, validate_collaboration_state.py:1322) recomputa `rebuild_snapshot`
  (full replay de todos los eventos) y dispararia drift. Doble red.
- Estructural: `verify_snapshot_checkpoint` se usa SOLO en `EventWriter.state()` (grep). El validador
  offline usa `events_in_log_order` + `validate_chain` + `validate_agent_signatures` + `assert_snapshot_matches`;
  NO toca el checkpoint. El camino vivo confia por VELOCIDAD; el gate offline enforcea correccion de punta
  a punta. G2 intacta.

## 5. AC2 -- byte-identico (checkpoint valido -> sembrado == full) por mi propio diferencial

- En una mezcla mas rica que la del autor, con checkpoint valido: `verified_seqs == [seq > up_to_seq]`
  (solo la cola se verifica; medido `verified=[7,8]`, up_to_seq=6). PASS.
- `canonical_json(state_sembrado) == canonical_json(state_full)` (replay completo independiente). PASS.
- Diferencial del SNAPSHOT: `{up_to_seq,state,canonical_hash}` sembrado == full byte-a-byte. PASS.
- Asociatividad sana: `base_state` esta unicamente determinado por el `canonical_hash` firmado (colision
  SHA-256 requerida para divergir), asi que sembrar-la-cola == replay-completo para todo checkpoint
  legitimamente producido.

## 6. AC1 / AC5 -- firma de instancia + alcance + fallback

- AC1: `integrity.key_id == runtime-hmac:v1`, `method == hmac-sha256`. Usa `signing_secret(config,
  'runtime')` -- la MISMA clase que `event_auth`; sin clave/fichero/privada nueva. El snapshot VIVO ya lleva
  el bloque `integrity` firmado.
- AC5: `protocol.config.json` byte-identico vs padre del impl (diff vacio; ni siquiera aparece en la lista
  del commit) y sin genesis/re-genesis/cambio de cadena. `max_incremental_events` vive en
  `runtime/CHECKPOINT_POLICY.json` (registro FUERA del config pineado), confirmado ausente del config.
  Alcance de codigo = las 3 rutas declaradas (`runtime/eventlog.py`, `runtime/CHECKPOINT_POLICY.json`,
  `examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py`) + los escritos gobernados del ledger/
  estado (dogfooding). Fallback `verified_state=None` -> `rebuild_snapshot` (full) intacto;
  `write_snapshot(None)` = rebuild full; otros callers de snapshot en `protocol_replay` (genesis-ref/anchor)
  son otra ruta, no la incremental viva.

## 7. Residuales declarados (honestos)

1. Modelo de confianza por DISENO (no un slip): la firma `integrity` es HMAC de INSTANCIA. Quien posea el
   secreto `runtime` de la instancia puede forjar un checkpoint (firmar un `state` arbitrario coherente).
   Esto es lo que DECISION-0105 acepta explicitamente (G1/G2): la frontera dura es el gate offline, que
   recomputa todo (validate_chain + assert_snapshot_matches) cada commit. AC4 confirma que un forje que
   haga divergir el estado vivo se caza offline como drift/cadena rota. Riesgo residual acotado por G2.
2. Un `up_to_seq`/K_max no-numerico en el snapshot/registro puede lanzar excepcion dentro de
   `verify_snapshot_checkpoint` (p.ej. `int('abc')`), que propaga y ABORTA el submit. Es fail-CLOSED (para
   en error, jamas skip inseguro); no viola "nunca saltar la verificacion". Robustez menor, no de seguridad.
3. El clon limpio no trae `.protocol-secrets/` -> sobre el snapshot vivo cae a full por `unresolved_key`
   (fail-safe correcto por DECISION-0046). La rama de CONFIANZA se ejercita via fixture propio (clave
   controlada), que es la forma correcta de probarla de manera reproducible y aislada.

## 8. Veredicto

Los 5 AC pasan. FAIL-SAFE airtight: 11 vectores de checkpoint invalido (incluidas las 3 fugas centrales de
"state manipulado") -> `trusted:False` + el CALLER real verifica TODOS los eventos, cero skip; el check
RECOMPUTA `canonical_hash(state)` y no confia el campo almacenado. Gate offline NO debilitado: evento
viejo manipulado sigue cazado por `validate_chain` (+ drift por rebuild). Byte-identico confirmado por mi
diferencial independiente (sembrado == full en estado y snapshot; solo cola verificada). HMAC de instancia
`runtime` sin clave nueva; K_max fuera del config pineado; config byte-identico sin genesis/cadena; alcance
3 rutas; fallback intacto. Gates hub (banco, validate/validate_chain, scan_encoding, scan_domain_neutrality)
exit 0 en clon limpio; arnes propio 31/31 PASS.

**OK-CLOSABLE.** Sin caso de fail-open ni de debilitamiento del gate offline hallado. -- Analista
