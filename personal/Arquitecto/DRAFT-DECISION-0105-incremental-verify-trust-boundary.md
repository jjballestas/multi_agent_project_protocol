# DRAFT DECISION-0105 - Verificacion incremental del ledger con limite de confianza firmado

> ESTADO: BORRADOR para aprobacion del operador/humano. NO registrado. Cambio de mecanismo de protocolo
> (semantica de atestacion en el camino vivo) -> exige DECISION + aprobacion humana antes de aplicar.
> Autor: Arquitecto. Fecha: 2026-07-29. Relaciona: cadena #4 / epoch versioning (AGENTS.md), TASK-0303,
> TASK-0305 (palanca A, atestacion-neutral, independiente de esta decision).

## 1. Contexto y problema

Cada `submit_intent` re-verifica las firmas (HMAC-SHA256 + ed25519) del **log entero** (~6000 eventos hoy,
~10.5s medidos) en cada llamada a `state()`. El coste es **O(todos los eventos) por submit** y crece sin cota
con la vida de la instancia. `snapshot.json` YA contiene el limite de confianza necesario (`up_to_seq` +
`canonical_hash` del estado) y `replay_events` YA acepta `base_state`, pero **nadie lo usa** para saltarse la
verificacion de lo viejo: el snapshot es write-only en el camino de verificacion.

TASK-0305 (palanca A) quita el multiplicador intra-submit (verificar 1 vez en vez de ~3) sin cambiar nada de
atestacion. Esta decision es la palanca B: hacer la verificacion **O(eventos nuevos)** en el caso general,
sembrando el replay desde un snapshot **de confianza**. Requiere decision porque cambia el modelo de confianza
del camino vivo: pasar de "verifico todo cada vez" a "confio en un limite y verifico solo la cola".

## 2. Decision propuesta

En el camino VIVO de escritura/replay (`runtime/eventlog.py`), sembrar `replay_events` desde
`snapshot.state` como `base_state` y **verificar solo los eventos con `seq > snapshot.up_to_seq`**, SIEMPRE Y
CUANDO el snapshot supere una validacion de integridad propia. El **gate offline** (`validate_chain` + rebuild
completo en `validate_collaboration_state.py` / CI) queda **sin cambios**: sigue re-verificando TODOS los
eventos en cada commit gobernado. Es decir: el camino vivo confia en el limite por **velocidad**; el gate
**enforcea** la correccion de punta a punta.

## 3. Diseno de seguridad (los dos guardas -- lo innegociable)

### Guarda 1 - Integridad propia del snapshot (evitar "forjar el limite")
Confiar en `snapshot.state` como base solo es seguro si un atacante no puede fabricar un snapshot que "certifique"
un estado con eventos manipulados. Por eso el snapshot se **liga criptograficamente**:
- Se anade a `snapshot.json` una firma de integridad (`integrity`: HMAC-SHA256 con la clave de instancia
  `runtime-hmac:v1`, la MISMA clase de clave que `event_auth`; NO una clave nueva) sobre el par
  `(canonical_hash_del_estado, up_to_seq, prev_hash_del_evento_up_to_seq)`.
- `replay_events` (o `load_snapshot`) trata `snapshot.state` como base de confianza **solo si**: (a) la firma
  `integrity` verifica con la clave de instancia; (b) `canonical_hash(snapshot.state)` coincide con el declarado;
  (c) `up_to_seq <= head` del log y el evento `up_to_seq` del log casa con el `prev_hash` firmado.
- **Fail-safe (nunca fail-open):** si el snapshot falta, esta stale, o cualquier chequeo falla ->
  **verificacion completa** (el comportamiento actual). Jamas saltarse la verificacion sin un limite firmado y
  vigente. Un snapshot corrupto degrada a lento, nunca a inseguro.

### Guarda 2 - El gate offline sigue siendo la frontera dura
`validate_collaboration_state.py:1330` corre `validate_chain(events_in_log_order(...))` sobre **todos** los
eventos, y CI es la frontera de enforcement de todo commit gobernado (AGENTS.md). Esta decision **no toca** ese
camino. Consecuencia: aunque el camino vivo confiara en un snapshot malo (imposible si Guarda 1 se respeta), el
commit resultante **no pasaria** el gate. La optimizacion vive dentro de una malla que ya re-verifica todo.

## 4. Alcance y NO-alcance (critico para el fondo intocable)

- **SIN cambio en `protocol.config.json` ni en el genesis.** El genesis liga `canonical_hash(config)`, NO la
  longitud del log ni el formato del snapshot. `snapshot.json` es ESTADO regenerado, no config pineada.
- **SIN flag en `event_state`** (anadir una clave a `event_state` cambiaria `canonical_hash(config)` y romperia
  el genesis, y el override solo admite `actor_auth_*`/`event_auth`). La habilitacion es la PRESENCIA de un
  snapshot con firma `integrity` valida: si existe y verifica -> cola; si no -> completo. Cero toque a config,
  cero re-genesis.
- **SIN cambio en QUE se verifica** ni en la cadena #4. Los eventos nuevos se verifican igual; solo se confia en
  un prefijo ya verificado y firmado.
- NO incluye la compactacion fisica del log (`compact_through`, palanca C -- decision aparte).
- NO incluye la palanca A (TASK-0305), que es independiente y no necesita decision.

## 5. Rollout coordinado

1. Cerrar TASK-0305 (palanca A) primero -- baja el coste 3x sin riesgo de atestacion.
2. Implementar B tras aprobacion: firma `integrity` del snapshot + siembra condicional en `replay_events`.
3. **Diferencial obligatorio:** para un corpus de intents, el resultado (eventos, snapshot canonical_hash,
   validate, validate_chain) debe ser IDENTICO con y sin la siembra; y con snapshot invalido debe caer a
   completo y seguir verde.
4. Ambos loops ya rutean por submit_intent, asi que no hay riesgo de un editor manual que rompa el limite.
5. Reversible: borrar/ignorar la firma `integrity` -> vuelve a verificacion completa (fail-safe) sin migracion.

## 6. Invariantes que esta decision debe preservar (para el checker)

- I1: con snapshot valido, verificar la cola produce el MISMO estado que verificar todo (probado por diferencial).
- I2: con snapshot ausente/invalido/stale -> verificacion completa (fail-safe), nunca skip.
- I3: el gate offline (validate_chain + rebuild completo) queda intacto y verde.
- I4: `protocol.config.json` byte-identico; sin re-genesis; override sin claves nuevas.
- I5: la clave de la firma `integrity` es la HMAC de instancia existente; no se introduce clave ni fichero nuevo
  de secreto; ninguna privada de humano toca esto.

## 7. Preguntas abiertas para el operador

- Q1: firma de integridad del snapshot = HMAC de instancia (simetrica, la del runtime) vs ed25519 del Arquitecto
  (asimetrica, atribuible). HMAC basta porque el gate offline es la frontera dura y el snapshot es estado local;
  ed25519 daria atribucion por-firmante a costa de mas maquinaria. Propongo **HMAC de instancia** (minimo cambio).
- Q2: cota de "stale" del snapshot (p.ej. rechazar si `head - up_to_seq` supera K, para que la cola verificada
  no crezca sin limite entre rebuilds). Propongo rebuild del snapshot al final de cada submit (ya ocurre), asi
  la cola es ~1.
- Q3: si ademas quieres la palanca C (compactacion fisica) en la misma tanda o en una decision posterior.
