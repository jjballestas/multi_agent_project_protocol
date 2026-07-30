---
decision_id: DECISION-0105
title: "Checkpoint verificado firmado: verificacion incremental (palanca B) + compactacion fisica del log (palanca C)"
status: accepted
date: 2026-07-30
proposed_by: Arquitecto
approved_by: operador humano
supersedes: []
relates_to:
  - TASK-0305
  - DECISION-0022
  - DECISION-0028
---

# DECISION-0105 - Checkpoint verificado firmado (verificacion incremental B + compactacion C)

## Contexto

El coste de verificacion del ledger es O(todos los eventos) por operacion: cada replay re-verifica las firmas
(HMAC-SHA256 + ed25519) del log entero. TASK-0305 (palanca A, DONE, atestacion-neutral) elimino el multiplicador
intra-submit (verificar 1 vez en vez de ~3), pero el caso general sigue siendo O(n) por submit y crece sin cota con
la vida de la instancia. `snapshot.json` ya lleva `up_to_seq` + `canonical_hash` (un limite de confianza LATENTE)
pero nada lo usa para acotar coste, y `scripts/prune_state.py` NO toca el event log (solo el estado). El
`compact_through` de `runtime/eventlog.py` existe pero no tiene callers ni da ganancia (re-lee los archivos).

Esta decision introduce UN solo primitivo -- el **checkpoint verificado firmado** -- y lo aplica a dos palancas
que el operador aprobo para la MISMA tanda: verificacion incremental entre submits (B) y compactacion fisica del
log (C). La palanca A (TASK-0305) queda como cimiento ya en firme.

## Decision

### Primitivo comun: checkpoint verificado firmado

`snapshot.json` gana un campo `integrity`: una firma **HMAC-SHA256 con la clave de INSTANCIA**
(`runtime-hmac:v1`, la misma clase que `event_auth`; NO una clave nueva, NO una privada de humano) sobre la tupla
canonica `(canonical_hash(state), up_to_seq, prev_hash_del_evento@up_to_seq)`. Un checkpoint es de CONFIANZA solo si:
(a) la firma `integrity` verifica con la clave de instancia; (b) `canonical_hash(state)` coincide con el declarado;
(c) `up_to_seq <= head` del log y el evento `@up_to_seq` casa con el `prev_hash` firmado. **HMAC de instancia**
(no ed25519 del Arquitecto): el snapshot es estado local y el gate offline es la frontera dura, asi que basta la
simetria de instancia -- minimo cambio, ninguna maquinaria de firmante nueva.

### Palanca B - verificacion incremental entre submits

En el camino VIVO de replay (`runtime/eventlog.py`), sembrar `replay_events` desde el `state` del checkpoint de
confianza como `base_state` y **verificar solo los eventos con `seq > up_to_seq`**. El snapshot se reconstruye al
final de cada submit (ya ocurre), asi que la cola verificada es normalmente ~1 (respuesta a la pregunta de "stale":
rebuild por submit). Ademas un cap `K_max` (en un registro FUERA del config pineado): si `head - up_to_seq > K_max`,
NO sembrar -> verificacion completa. Convierte O(todos) en O(nuevos).

### Palanca C - compactacion fisica del log

Cablear `compact_through(up_to_seq)` sobre el limite del checkpoint de confianza: mover los eventos `<= up_to_seq`
a un archivo (`runtime/state/archives/events-<lo>-<hi>.jsonl`) y dejar solo la cola caliente en `events.jsonl`.
`events_in_log_order` / `replay_events` **confian en el prefijo archivado** (su integridad la respalda el checkpoint
firmado + el hash del propio archivo) y solo re-verifican la cola caliente. Acota el log fisicamente (disco +
cold-start). El umbral de compactacion vive en el mismo registro fuera del config pineado.

## Guardas de seguridad (innegociables, aplican a B y C)

- **G1 - integridad propia del checkpoint (evitar 'forjar el limite'):** confiar en el checkpoint solo tras verificar
  su firma `integrity` + hash + coherencia con el log. **Fail-safe (nunca fail-open):** checkpoint ausente/invalido/
  stale, o archivo de compactacion cuyo hash no casa -> **verificacion completa** (comportamiento actual). Degradar a
  lento, jamas a inseguro.
- **G2 - el gate offline sigue siendo la frontera dura:** `scripts/validate_collaboration_state.py` (CI) sigue
  corriendo `validate_chain` + verificacion de firmas sobre TODOS los eventos (leyendo tambien los archivos de
  compactacion para la auditoria profunda). El camino vivo confia en el limite por VELOCIDAD; el gate ENFORCEA la
  correccion de punta a punta. Un limite forjado (imposible si G1 se respeta) no pasaria el gate que todo commit debe pasar.

## Alcance y NO-alcance (fondo intocable)

- **SIN cambio en `protocol.config.json` ni en el genesis.** El genesis liga `canonical_hash(config)`, NO el formato
  del snapshot ni la longitud del log. `snapshot.json` es estado regenerado. La firma `integrity` usa el HMAC de
  instancia existente. El cap `K_max` y el umbral de compactacion viven en un registro FUERA del config pineado
  (patron COMMIT_TRAILERS.json). Cero re-genesis.
- **SIN cambio en QUE se verifica** ni en la cadena #4: los eventos nuevos se verifican igual; solo se confia en un
  prefijo ya verificado y firmado.
- La habilitacion es la PRESENCIA de un checkpoint con `integrity` valido (B) / de archivos de compactacion validos
  (C); sin ellos, todo cae al camino completo actual. No hay flag en `event_state`.

## Invariantes (para el checker de cada tarea)

- I1: con checkpoint valido, verificar la cola produce el MISMO estado que verificar todo (diferencial byte-identico).
- I2: checkpoint/archivo ausente/invalido/stale -> verificacion completa (fail-safe), nunca skip.
- I3: el gate offline (validate_chain + firmas sobre todos los eventos, incl. archivos) queda intacto y verde.
- I4: `protocol.config.json` byte-identico; sin re-genesis; override sin claves nuevas.
- I5: la firma `integrity` usa el HMAC de instancia existente; ninguna clave/fichero/privada-humana nueva.
- I6 (C): tras compactar, la union (archivos + cola) re-materializa al MISMO estado; el gate offline lee ambos.

## Rollout coordinado (misma tanda B+C, secuenciado)

1. Palanca A (TASK-0305) ya DONE -- cimiento.
2. **B primero** (tarea propia): campo `integrity` firmado del checkpoint + siembra condicional con cap K_max +
   fail-safe. Gate: diferencial byte-identico (con y sin siembra IDENTICO) + fail-safe (checkpoint invalido -> full,
   verde) + gate offline sin debilitar + config byte-identico.
3. **C despues** (tarea propia): cablear `compact_through` sobre el limite + confianza del prefijo archivado + gate
   offline que lee archivos. Gate: re-materializar union == estado; validate_chain full sobre archivos+cola verde;
   fail-safe si un archivo no casa.
4. Cada tarea por el ciclo gobernado + gate adversarial de 2 capas (recompute Arquitecto + Analista). Reversible:
   borrar/ignorar la firma `integrity` o los archivos -> vuelve a verificacion completa (fail-safe) sin migracion.
