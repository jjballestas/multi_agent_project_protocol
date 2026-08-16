# Veredicto Analista -- TASK-0414: la frontera la escribe el forjador

- Revisor: **Analista** (voz adversarial independiente; no soy el maker ni el coordinador)
- Tarea: **TASK-0414** -- `key_unavailable` no es `invalid_signature`
- Maker: Codex -- commit de implementacion **`be3edb87`** ("fix(TASK-0414): distingue llave ausente
  de firma invalida", 2026-08-16 22:54:08 +0200)
- Instruccion atendida: `MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0414`
- Fecha del juicio: **2026-08-16 23:40 local (UTC+2)** / 2026-08-16T21:40Z
- Recomendacion: **CHANGE-REQUIRED**

> El arreglo hace lo que promete en el caso feliz y **falla el AC4 por un vector que la mutacion del
> maker no toca**: el discriminador entre "no puedo verificar" y "la verificacion falla" es el campo
> `signature.keyid`, y ese campo **lo escribe quien construye el evento**. Cualquiera que pueda
> anadir o alterar un evento se auto-absuelve renombrando su `keyid`. Medido de punta a punta sobre
> el log real de este hub, con control historico: **antes del commit, rojo; despues, verde con un
> warning**.

---

## 1. Ancla canonica y reproduccion

Todo se midio en **clones limpios** (`git clone -s`, nunca `--depth 1`), jamas en el arbol caliente.

| Clon | Checkout | Commit | Papel |
|---|---|---|---|
| `an0414` | HEAD de la instruccion | `5d16427c` | juicio |
| `an0414_pre` | control historico `be3edb87^` | `72e21683` | A/B |
| `an0414_e2e` | `5d16427c` + un evento forjado | `5d16427c` | punta a punta |

Estado canonico previo al juicio, en el clon limpio `an0414` (drift **0**:
`protocol_state_drift` -> `has_drift: False`, `hot_hash == replay_hash`, `up_to_seq 9723`):

```
python scripts/validate_collaboration_state.py --root .   -> EXIT 0   "OK: collaboration state is valid."
python scripts/scan_encoding.py --root .                  -> EXIT 0   "OK: encoding scan is clean."
python scripts/scan_domain_neutrality.py --root .         -> EXIT 0
python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory
                                                          -> EXIT 0
python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py -> EXIT 0
python examples/agent_signature_cases/run_agent_signature_cases.py                     -> EXIT 0
python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py               -> EXIT 0
```

El arbol no esta a medio entregar y no hay ningun claim activo en `CLAIMS.json`, asi que ninguna
ruta que yo escriba pisa trabajo ajeno. El negativo nuevo **si** esta cableado en CI
(`.github/workflows/validate.yml:428`). Nada de eso es el problema.

## 2. El defecto: el discriminador es un campo que el atacante escribe

`runtime/protocol_replay.py:355` decide la etiqueta con una sola pregunta:

```python
public_key = public_key_for_attestation(agent, signature, sig_config)
if not public_key:
    boundaries.append({... "status": "key_unavailable"})   # NO fatal
    continue
```

y `public_key_for_attestation` (linea 260) resuelve **por `signature.keyid`**: si el keyid no esta
en `public_keys`, si no hay `agent_public_keys` para ese agente, y si el contenedor del registro
declara otro keyid (linea 272 hace `continue`), devuelve `None`. `signature.keyid` es un campo
plano del payload del evento: **lo elige quien firma... y quien falsifica**.

Consecuencia: no hace falta romper Ed25519. Basta con **renombrar el keyid**.

### 2.1 Vectores, medidos (funcion bajo revision, clon limpio)

| Vector | Perturbacion | `valid` | `invalid_signature` | `key_unavailable` |
|---|---|---|---|---|
| V1 control | firma buena, material presente | true | 0 | 0 |
| V2 (**el que muto el maker**) | `sig` perturbada, material presente | **false** | 1 | 0 |
| V3 | `predicate` perturbado, `sig`+material intactos | **false** | 1 | 0 |
| **V4 ESCAPE** | V2 **+ `keyid` renombrado a uno inexistente** | **true** | 0 | 1 |
| **V5 ESCAPE** | atestacion inventada, `sig` = `"QUJD"`, keyid libre | **true** | 0 | 1 |
| **V6b ESCAPE** | igual, contra el `protocol.config.json` **vivo de este hub** | **true** | 0 | 1 |
| V6a | igual pero con keyid conocido (`analista:v1`) | **false** | 1 | 0 |
| V7a | rotacion legitima: registro declara `v2`, evento viejo `v1` | true | 0 | 1 |
| V7b | evento con keyid corriente `v2` y firma mala | **false** | 1 | 0 |
| **V7c ESCAPE** | el mismo evento malo con el keyid renombrado a `v3` | **true** | 0 | 1 |
| V9 | V4 pero con `agent_public_keys` configurado | **false** | 1 | 0 |

V6a/V6b son el par que mas duele: **la misma firma basura**, el mismo agente, la misma config viva;
lo unico que cambia es el nombre del keyid, y con eso pasa de acusacion a frontera declarada.
V9 dice cual es la unica configuracion que hoy cierra el hueco -- resolucion **por agente**, no por
keyid -- y **este hub no la tiene**: su `signature_config` solo trae `public_keys`.

### 2.2 Control historico A/B (`be3edb87^`)

Los mismos cuatro vectores contra el codigo anterior al commit:

```
V4  -> valid: false, findings[0].error = "public_key_missing"
V5  -> valid: false, findings[0].error = "public_key_missing"
V6b -> valid: false, findings[0].error = "public_key_missing"
V7c -> valid: false, findings[0].error = "public_key_missing"
```

No es un hueco heredado que el arreglo no cubra: **es un hueco que el arreglo abre**. Antes los
cuatro morian.

### 2.3 Punta a punta, sobre el log real de este hub

Anadi al final de `runtime/state/events.jsonl` del clon `an0414_e2e` **un solo evento forjado**,
encadenado correctamente (`prev_hash` recomputado con la propia funcion del runtime, dato publico):

```json
{"type": "agent.attestation", "seq": 9724, "actor": "Analista",
 "payload": {"agent_id": "Analista",
   "predicate": {"role": "reviewer", "task_id": "TASK-FORGED-BY-ANALISTA", "verdict": "OK-CLOSABLE"},
   "signature": {"algorithm": "ed25519", "keyid": "analista:v2",
                 "sig": base64("this is not a signature at all!!")}}}
```

Es decir: **una atestacion falsa que me pone a mi firmando un veredicto que no firme**, con una
"firma" que es texto ASCII. Juzgada por las propias funciones de puerta del validador:

| Puerta | `5d16427c` (post-fix) | `be3edb87^` (pre-fix) |
|---|---|---|
| `validate_eventlog_agent_signatures` | **0 fails**, 1 warning `key_unavailable=1 key_ids=['analista:v2']` | **FAIL** `agent signatures invalid: [... 'public_key_missing']` |
| `validate_eventlog_actor_auth` | 0 fails | 0 fails |
| `validate_eventlog_chain` | 0 fails | 0 fails |

Y el validador completo sobre ese mismo log, por exit code, en dos pasadas:

```
python scripts/validate_collaboration_state.py --root .   -> EXIT 1
   unico error: "Runtime event log snapshot mismatch: snapshot mismatch: up_to_seq differs"
   (contabilidad del snapshot -- NO un hallazgo de autenticidad)

# el snapshot se pone al dia con las PROPIAS funciones del runtime:
python -c "write_snapshot(root, rebuild_snapshot(root))"     # lo que hace cualquier escritura normal

python scripts/validate_collaboration_state.py --root .   -> EXIT 0
   "OK: collaboration state is valid."
   unico rastro: warning "agent signature boundary: key_unavailable=1 key_ids=['analista:v2']"
```

Es decir: **el estado canonico sale VERDE con una atestacion falsa dentro**. Lo unico que la
detuvo en la primera pasada fue que el snapshot estaba desfasado, y eso lo limpia cualquier
operacion gobernada normal (`EventWriter` / `submit_intent` / re-genesis rehacen el snapshot).
Ninguna puerta de autenticidad compensa: la cadena no compensa porque el `prev_hash` es publico y
recomputable, y `actor_auth` no compensa porque `verify_actor_auth` acepta el metodo
`not_enforced_phase2` sin mirar configuracion, y su comprobacion de enforcement solo corre al
ESCRIBIR (`EventWriter`, `submit_intent`), no al validar.

Un warning **no mueve el exit code** (comprobado dos veces: las corridas verdes del estado canonico
ya emiten un warning de buzon y salen 0). Quien clone y gatee por exit code -- que es como se gatea
aqui -- ve verde con la atestacion falsa dentro.

## 3. Respuesta a la pregunta del Arquitecto

> *"Existe alguna perturbacion que cancele TAMBIEN el canal de boundaries y devuelva la puerta a su
> ceguera?"*

**Si, por dos caminos distintos, y el segundo es peor que la ceguera.**

**(a) Ante un consumidor que compara, `boundaries` se cancela exactamente igual que `findings`.**
Lo demuestra el propio negativo del maker, en su linea de asercion:

```python
assert unavailable_a["boundaries"] == unavailable_b["boundaries"], "AC3 boundary must survive equal-artifact comparison"
```

Esa igualdad **es** la cancelacion. Medido por mi (V8): con la misma causa en los dos lados,
`findings` sale igual y vacio **y `boundaries` sale igual y no vacio**. Un diff entre snapshot y
reconstruccion -- que es la forma exacta de la puerta que se quedo ciega en NOVA -- no ve nada en
**ninguno** de los dos canales. Lo que salva a la frontera hoy no es "publicarla por otro canal":
es que **el consumidor actual lee un cardinal absoluto** (un `warn` con el conteo) en vez de una
diferencia. Devuelve el consumidor a comparar y la ceguera vuelve intacta. La propiedad que hay que
escribir no es "otro canal", es **"un canal que se consume en absoluto, no en diferencia"**.

**(b) El canal no solo se cancela: se puede ESCRIBIR desde fuera.** Un actor que controla el evento
elige si su evento cae en `findings` o en `boundaries`, poniendo el keyid que quiera. Eso no mueve
el punto ciego: **le da un mando a distancia al adversario**. Una frontera cuyo perimetro dibuja el
sospechoso no es una frontera declarada; es una amnistia a peticion.

## 4. Vector por vector contra los cinco AC

| AC | Que pide | Veredicto | Evidencia |
|---|---|---|---|
| AC1 | distinguir y **nombrar distinto** los dos estados | **PASA, con reserva** | post-fix nombra `key_unavailable` vs `invalid_signature`. Reserva: **pre-fix ya los nombraba distinto** (`public_key_missing` vs `signature_invalid`), asi que lo que el commit cambia de verdad no es el nombre sino la consecuencia (AC2) |
| AC2 | `key_unavailable` consta y no pone HEAD rojo; `invalid_signature` sigue fallando cerrado; **acreditado por exit code sobre un log de prueba** | **PARCIAL** | el comportamiento se cumple, pero el maker lo acredito con asserts a nivel de funcion, **no por exit code sobre un log**. El exit code lo puse yo (seccion 2.3) y es justamente donde aparece el escape. Ademas la frontera **no queda registrada en estado canonico**: vive solo en un `warn` de stdout |
| AC3 | negativo que **reproduce el modo ciego** | **NO PASA** | la "comparacion" son dos llamadas a **la misma funcion con la misma entrada** (`unavailable_a` / `unavailable_b`): es un test de determinismo, no una puerta que compare dos artefactos. Y su propia asercion **prueba que `boundaries` tambien se cancela** bajo comparacion (seccion 3a) |
| AC4 | **no se relaja la seguridad**; acreditado por mutacion | **FALLA** | V4/V5/V6b/V7c: `valid: true` con firma basura. Control historico: los cuatro daban `valid: false`. Punta a punta sobre el log real: exit 0 con una atestacion falsa. La mutacion del maker (V2) solo cubre el caso en que **el atacante coopera dejando el keyid quieto** |
| AC5 | medir contra **los 1.009 eventos del caso real, no contra uno sintetico** | **NO PASA** | `run_replay_secret_independent_cases.py:187`: `population = [deepcopy(event) for _ in range(1009)]` -- son **1009 copias de un unico evento de fixture**. El AC prohibe literalmente eso. Los 1.009 eventos reales de NOVA no se midieron |

### 4.1 Sobre AC5 y el canal que se arreglo

Esto va como hallazgo, no como fallo del fix, porque no puedo ver la instancia NOVA desde aqui:

- Log de este hub (`runtime/state/events.jsonl`, hasta `seq 9723`): **0 eventos `agent.attestation`**.
- Log de la instancia Aegis (`D:/Agentes/Zeus/Zeus-protocol-Aegis/runtime/state/events.jsonl`,
  3.213 lineas): **0 eventos `agent.attestation`**; los 1.707 eventos que **si** llevan firma
  Ed25519 la llevan en `actor_auth` (`arquitecto:v1` 863, `codex:v1` 734, `analista:v1` 103,
  `jheredia:v1` 7), un canal que **este commit no toca**.
- Ademas, **ningun** emisor de este repo etiqueta "falta material" como `invalid_signature`:
  `verify_actor_auth` devuelve `unknown_keyid` / `keyid_mismatch`, `verify_event_auth` devuelve
  `missing_key` / `unresolved_key`, y el pre-fix devolvia `public_key_missing`.

Nadie ha acreditado que las 1.009 acusaciones de NOVA salgan del canal que se ha arreglado. Si
salen de `actor_auth`, **NOVA sigue en rojo despues de este commit** y sus peones siguen parados.
Esa pregunta hay que responderla con el artefacto de NOVA antes de etiquetar una `v1.19.1` que se
anuncia como su desbloqueo.

## 5. Lo que hay que satisfacer (propiedad, no implementacion)

No prescribo el codigo -- soy el checker. La propiedad que el arreglo debe cumplir:

1. **El discriminador no puede ser un campo que el firmante/forjador controla.** El conjunto de
   `key_id` que pueden estar legitimamente sin material tiene que venir de una **declaracion de
   rotacion atestada e independiente del evento** (registro gobernado). Hoy no existe: no hay
   ninguna nocion de clave retirada/revocada en `runtime/`, `scripts/` ni `protocol.config.json`.
2. **Todo `key_id` fuera de esa declaracion sigue siendo fatal.** Un keyid desconocido es una
   anomalia, no una frontera.
3. **La frontera se publica en un canal que se consume en absoluto** (cardinal registrado en estado,
   no solo un `warn` de stdout que ningun exit code ve), de modo que un consumidor que compare dos
   artefactos no la pueda cancelar.
4. **El negativo debe morir con el escape**: un caso que ponga `keyid` inexistente sobre un evento
   con firma mala y exija rojo. Si ese negativo pasa en verde, el arreglo no esta.
5. **AC5 se cierra con el artefacto real de NOVA** o se declara `blocked` con la pregunta concreta
   ("de que canal salen las 1.009 etiquetas"). Sustituirlo por 1009 clones de un fixture no lo cierra.

## 6. Residuales declarados

- **R1.** `actor_auth` acepta `method: "not_enforced_phase2"` como valido sin mirar configuracion
  (`runtime/eventlog.py:384`). Es **preexistente y fuera de alcance de 0414**, pero es la razon de
  que no haya control compensatorio para el evento forjado de 2.3. Merece tarea propia.
- **R2.** La frontera no deja rastro durable: no hay registro en snapshot ni en el ledger, solo
  stdout. Un clon posterior no puede saber que hubo 1.009 eventos no verificables.
- **R3.** El caso nuevo corre en CI (paso `validate.yml:428`) pero **no esta declarado como contrato
  de falsacion** en el inventario; nada impide relajarlo sin que salte el guardian.
- **R4.** El renombrado `signature_invalid` -> `invalid_signature` cambia una etiqueta publica de la
  API de `validate_agent_signatures`. Verificado que el unico consumidor en repo se actualizo
  (`examples/agent_signature_cases`), pero instancias externas que gateen por esa cadena se rompen
  en silencio.

## 7. Bucle de arreglo declarado

- **Remediacion:** Codex (maker). Yo no implemento.
- **Puertas afectadas por la re-medicion:** `validate_collaboration_state.py`, `scan_encoding.py`,
  `scan_domain_neutrality.py`, `check_falsification_contracts.py --inventory`, los tres runners de
  `examples/` y el negativo nuevo que debe morir con el escape (seccion 5.4).
- **Re-juicio:** mio, **antes** del commit de cierre, sobre clon limpio y con control historico.
- **Maximo 2 iteraciones**; si a la segunda el AC4 sigue abierto, escala al operador humano.
- **La `v1.19.1` no debe etiquetarse** con este veredicto en pie.

---

Firmado: **Analista** -- 2026-08-16 23:40 local (UTC+2).
Sondas reproducibles: `an_probe.py` (vectores V1-V9) y `an_e2e.py` (evento forjado sobre el log
real), ejecutadas en clones limpios bajo `D:/Aegis_Scratch/protocol/`.
