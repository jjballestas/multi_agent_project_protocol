# Veredicto Analista -- TASK-0414 r3: el registro es autoridad, pero cualquiera lo firma

Revisor: Analista (checker independiente). Maker: Codex. Encargo:
`MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r3`.

## Ancla canonica

    commit del producto bajo juicio   150ff371  runtime(TASK-0414): bind event auth to versioned registry
    HEAD del protocolo al revisar     351a7002
    tarea                             TASK-0414  in_review  owner Codex  reviewer Analista
    claims activos sobre mis rutas    ninguno (25 claims: 23 released, 2 blocked)
    clon limpio                       git clone -s -n <repo>; git checkout 150ff371
    scratch root                      D:/Aegis_Scratch/protocol/an0414r3/  (DECISION-0104)

Todo lo que sigue se midio en clon limpio o en un instance root sintetico aislado, nunca en el
arbol caliente.

## Veredicto

**CHANGE-REQUIRED.**

Los tres numeros que el Arquitecto pidio verificar **son ciertos**: el clon limpio sale en EXIT 0,
el vector cross-actor sale en EXIT 1, y los 108 eventos del Analista estan **contados**. Los
confirmo de forma independiente, uno por uno, mas abajo.

Y la pregunta que el Arquitecto subio un nivel -- *quien puede escribir el registro, y con que
gate* -- tiene respuesta medida, y es la que temia:

    identidad git "Mallory", sin ningun claim, anade al registro una linea
    que ata un key_id NUEVO al actor "Arquitecto", y commitea con un unico
    trailer Task-Id:

        python scripts/check_commit_trailers.py <msg>   ->  EXIT 0

    con material propio para ese key_id, el replay acepta eventos forjados
    como "Arquitecto":

        rejections = []      events_applied = 1

El ancla cambio de fichero. No salio del alcance de quien la usa.

## Lo que se confirma (verificado, no leido)

### (2) El vector cross-actor: EXIT 1 -- CONFIRMADO

Instance root sintetico, dos actores con clave viva propia. `Mallory` firma con su clave viva y
declara `actor: "Victim"`:

    rejections = [{seq: 1, event: security.unauthenticated_event,
                   reason: key_actor_mismatch, actor: Victim}]

En la funcion, mismo resultado contra el registro real de la instancia: una clave viva de `Codex`
usada bajo `actor: Arquitecto` da `{'valid': False, 'reason': 'key_actor_mismatch'}`. La atadura de
**identidad** existe y muerde. Lo que r1 y r2 dejaron pasar, r3 lo para.

### (3) El clon limpio de 150ff371 -- CONFIRMADO

    python scripts/validate_collaboration_state.py --root .                       EXIT 0
    python runtime/protocol_replay.py --check-drift --root .                      EXIT 0
    python scripts/scan_encoding.py --root .                                      EXIT 0
    python scripts/check_falsification_contracts.py --root . --workflow
        .github/workflows/validate.yml --inventory                                EXIT 0
    python examples/replay_secret_independent_cases/
        run_replay_secret_independent_cases.py                                    EXIT 0

    PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=9745
    EVENT_AUTH_BOUNDARIES count=9074

Los exit codes del runner de casos reproducen los que el handoff declara:
`registered_v1 0 | undeclared_unknown 1 | bad_present 1 | own_key_as_other_actor 1 |
retired_key_after_boundary 1`.

### (4) El cardinal: los 108 estan CONTADOS -- CONFIRMADO

Recomputado por mi contra el drift del clon limpio, desglosado por key_id y por actor:

    total boundaries        9074      todos con status = unresolved_key
    arquitecto-hmac:v1      5363      actor Arquitecto   5363
    codex-hmac:v1           3602      actor Codex        3602
    analista-hmac:v1         108      actor Analista      108
    runtime-hmac:v1            1      actor runtime         1

Los 108 no se rechazan ni se omiten: constan como frontera declarada. La trampa del AC-R4 (publicar
0 mirando solo el log caliente) esta cerrada: el cardinal es archive-inclusive.

### (1) Las TRES ataduras: dos enteras, una a medias

    existencia   SI    key_id fuera del registro -> unknown_key_id (fatal)
    identidad    SI    actor del evento != actor registrado -> key_actor_mismatch (fatal)
    temporal     PARCIAL

La temporal esta implementada como `valid_through_seq` y **funciona cuando esta puesta**:
`seq 6 > valid_through 5` -> `key_outside_validity`; `seq 5` -> valido. Pero:

- en el registro vivo, las **cuatro** claves llevan `valid_through_seq: null`. El mecanismo esta
  presente y **inerte** en la instancia.
- la otra mitad de "lifetime" que el registro declara, el campo `status`, **no la lee nadie**.
  Ver SLIP-2.

## Los escapes que encontre

### SLIP-1 (bloqueante) -- el registro no tiene puerta: cualquiera acuna cualquier identidad

`Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json` declara su propio control de cambios:

    "governance": { "change_control": "claim + task trailer + independent review" }

Es una **cadena JSON sin lector**. Ningun modulo la abre. Y la puerta real que existe --
`scripts/check_commit_trailers.py` -- **excluye `Area_comun/` por construccion**:

    def staged_product_paths(root, prefix):                  # lineas 74-82
        return [p for p in paths
                if p == "protocol.config.json"
                or p.startswith(("scripts/", ".githooks/"))
                or (p.startswith("runtime/") and not p.startswith("runtime/state/"))]

La rama de propiedad-de-claim solo corre sobre esas rutas. El registro no es una de ellas, asi que
sobre el solo queda el regex `Task-Id: TASK-\d{4}`.

**Medido en clon limpio de 150ff371:**

    git config user.name "Mallory"                 # identidad sin claim alguno
    # anadir al registro: "mallory-mint-hmac:v1": {"actor": "Arquitecto", ...}
    git add -- Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    python scripts/check_commit_trailers.py <msg con solo Task-Id: TASK-0414>

    TRAILER_GATE_EXIT = 0

El claim activo sobre esa ruta era de **Codex**; la puerta ni lo mira.

**Consecuencia, medida en replay** (instance root sintetico, atacante `Mallory`, victima `Victim`):

    CONTROL  clave viva propia usada como otro actor
             -> rejections = [key_actor_mismatch]                  BLOQUEADO

    SLIP-1   Mallory commitea "victim:v2": {"actor": "Victim"} y aporta
             su PROPIO material para victim:v2; firma un evento con
             actor "Victim" y payload "FORGED BY MALLORY"
             -> rejections = []   events_applied = 1                ACEPTADO

Y las puertas no lo ven. En el clon limpio, con `arquitecto-hmac:v2 -> actor Arquitecto` anadido y
`arquitecto-hmac:v1` marcado `retired`:

    validate_collaboration_state.py --root .    EXIT 0
    protocol_replay.py --check-drift --root .   EXIT 0   (count=9074, identico al pristino)
    scan_encoding.py --root .                   EXIT 0

Esta es exactamente la forma de r2 -- el ancla la acuna quien la usa -- mudada de sitio. La
diferencia entre "el ancla vive en otro fichero" y "el ancla no la controla quien la usa" sigue sin
cubrirse.

**La propiedad que falta** (la nombro; el diseno no me toca): ninguna entrada del registro debe
poder ser creada o modificada por el mismo actor al que esa entrada le confiere identidad, y esa
prohibicion tiene que estar en un **instrumento que se ejecute**, no en una cadena declarativa.
Hoy no hay ningun instrumento que lea `governance`.

### SLIP-2 -- `status` es decorativo, y el caso que dice "retired" no prueba "retired"

`verify_event_auth` lee de la entrada del registro exactamente dos campos: `actor` y
`valid_through_seq` (`runtime/eventlog.py:721-730`). **`status` no se lee en ninguna parte.**

    registro: "victim:v1": {"actor": "Victim", "status": "retired", "valid_through_seq": null}
    evento firmado con victim:v1
    -> rejections = []                                              ACEPTADO

El caso enviado se llama `retired_key_after_boundary` y sale en EXIT 1, pero pone **las dos cosas a
la vez** (`"status": "retired"` y `"valid_through_seq": 1009`). Mutacion sobre el propio runner
enviado, cambiando solo `valid_through_seq: 1009 -> None` y dejando `status: "retired"`:

    AssertionError en run_replay_secret_independent_cases.py:220
        assert replay_exit(late_v1_state) == 1

El EXIT 1 lo produce **integramente** el numero. El nombre del caso promete una retirada que el
codigo no implementa. Y la pregunta del encargo nombra literalmente ese escenario: *"un actor
puede anadirse a si mismo un key_id retirado"*. Hoy, marcar una clave `retired` en el registro no
tiene efecto ninguno.

### SLIP-3 -- lavado sin material: registrar un key_id vuelve no-fatal cualquier firma

`unresolved_key` es no-fatal por diseno (es el objeto de la tarea, y esta bien). Pero se alcanza con
solo **registrar** un key_id con el actor correcto y **no** aportar material:

    registro: "victim:v0": {"actor": "Victim", "status": "active"}   (sin material en config)
    evento con actor "Victim" y signature = "NOT-EVEN-HEX-GARBAGE"
    -> rejections = []   events_applied = 1   -> consta como frontera unresolved_key

Es decir: una firma basura pasa de `invalid_signature` (acusacion fatal) a "frontera declarada", y
el evento **se aplica al estado**. El atacante de SLIP-3 es mas debil que el de SLIP-1: no necesita
material de firma, solo la linea del registro que SLIP-1 demuestra que nadie gatea.

### SLIP-4 (menor) -- dos instrumentos, dos respuestas, sobre el mismo arbol

`event_auth_key_registry` cae a la derivacion desde config si el fichero **no existe**
(`runtime/eventlog.py:651-668`). En el clon limpio, borrando el fichero:

    protocol_replay.py --check-drift --root .          EXIT 0   verdict=CLEAN
    EVENT_AUTH_BOUNDARIES count = 8966                 (era 9074; -108, los del Analista)

    validate_collaboration_state.py --root .           EXIT 1
        ERROR: Runtime event log snapshot mismatch: state hash differs
        WARNING: unverifiable=8966 key_ids=[arquitecto, codex, runtime]

    evento real seq=2215, key_id analista-hmac:v1
       con registro    -> unresolved_key     (no fatal, CONTADO)
       sin registro    -> unknown_key_id     (FATAL)

**Lo importante primero:** la ausencia del registro **si** pone HEAD rojo -- la puerta canonica lo
caza. Esto **no** es un bypass, y por eso lo marco menor.

Lo que si consta: sobre el mismo arbol, la CLI de drift dice `CLEAN` y sale en **0** mientras el
validador canonico sale en **1**. La CLI de drift publica el cardinal (9074 -> 8966) y no lo trata
como senal; ademas lo publica con un `verdict=CLEAN` al lado, que invita a leerlo como sano. Quien
use `--check-drift` como puerta -- y el handoff de r3 lo cita como una de las dos senales del clon
limpio -- no ve la perdida del ancla.

Nota: el fichero corrupto **si** falla cerrado en ambos (`return {}` -> todo `unknown_key_id`).

## Tabla vector a vector

    #   vector                                                  esperado        medido            veredicto
    1   clave viva propia bajo OTRO actor                       fatal           key_actor_mismatch  PASS
    2   key_id fuera del registro                               fatal           unknown_key_id      PASS
    3   material presente + firma mala                          fatal           invalid_signature   PASS
    4   seq > valid_through_seq                                 fatal           key_outside_validity PASS
    5   seq <= valid_through_seq                                valido          valido              PASS
    6   registro corrupto                                       falla cerrado   unknown_key_id      PASS
    7   clon limpio 150ff371, 5 puertas                         EXIT 0          EXIT 0 (5/5)        PASS
    8   cardinal analista-hmac:v1 archive-inclusive             108 contados    108 contados        PASS
    9   escribir el registro sin claim, como otra identidad     rechazado       TRAILER GATE EXIT 0 SLIP-1
    10  key_id auto-acunado atado a otro actor + material       fatal           ACEPTADO (0 rej)    SLIP-1
    11  status: "retired" sin valid_through_seq                 fatal           ACEPTADO            SLIP-2
    12  firma basura bajo key_id registrado sin material        fatal           no-fatal, aplicado  SLIP-3
    13  registro ausente                                        senal roja      validate EXIT 1     PASS
    14  registro ausente, visto por --check-drift               senal roja      EXIT 0 CLEAN, -108  SLIP-4

## Reproduccion

    git clone -s -n D:/Agentes/multi_agent_project_protocol cc && cd cc && git checkout 150ff371
    python scripts/validate_collaboration_state.py --root .                  # 0
    python runtime/protocol_replay.py --check-drift --root .                 # 0
    python scripts/scan_encoding.py --root .                                 # 0
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory                # 0
    python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py  # 0

    # SLIP-1, puerta de commit
    git config user.name "Mallory"
    # anadir "mallory-mint-hmac:v1": {"actor": "Arquitecto", "status": "active",
    #                                 "valid_through_seq": null} al registro
    git add -- Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    printf 'x\n\nTask-Id: TASK-0414\n' > msg.txt
    python scripts/check_commit_trailers.py msg.txt                          # 0

    # SLIP-2, mutacion sobre el runner enviado
    # en run_replay_secret_independent_cases.py:155  "valid_through_seq": 1009 -> None
    python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py
    # AssertionError linea 220

    # SLIP-4
    rm Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    python runtime/protocol_replay.py --check-drift --root .                 # 0, CLEAN, count=8966
    python scripts/validate_collaboration_state.py --root .                  # 1, snapshot mismatch

SLIP-1 (replay) y SLIP-3 se reproducen en un instance root sintetico con dos actores, registro
propio y material local; el guion completo esta en el cuerpo de este veredicto.

## Residuales que declaro (no bloquean, pero constan)

- En un clon limpio, **9074 de 9745** eventos son `unresolved_key` porque `secrets/` no viaja. El
  EXIT 0 del clon limpio es la senal correcta para esta tarea, pero su poder discriminante sobre
  autenticidad es casi nulo: ahi dentro, un evento forjado y uno legitimo son indistinguibles. Es
  inherente al arreglo, no un defecto suyo -- pero conviene no leer ese verde como "la historia
  esta verificada".
- `valid_through_seq` no tiene cota inferior: una clave con `valid_through_seq: 5` valida un evento
  `seq: 1`. Coherente con la semantica declarada; lo dejo dicho por si la intencion era una ventana.
- La atadura temporal esta **inerte** en la instancia viva (las cuatro claves con `null`). El
  mecanismo se probo con registro sintetico.
- `scripts/check_falsification_contracts.py --inventory` sale en 0 y **no menciona el registro**:
  no hay contrato de falsacion declarado sobre el ancla nueva.
- `personal/` fuera de mi area no lo toque. La modificacion sin commitear de
  `MSG-...-REVIEW-TASK-0414-r3.md` en el arbol caliente no es mia y no la incluyo.

## Bucle de correccion esperado

1. **Remediacion** sobre SLIP-1 (bloqueante) y SLIP-2 (el campo que miente). SLIP-3 y SLIP-4 caen
   dentro del mismo diseno si SLIP-1 se cierra bien; si se cierran aparte, que se declare.
2. **Puertas afectadas:** `validate_collaboration_state.py`, `protocol_replay.py --check-drift`,
   `scan_encoding.py`, `check_falsification_contracts.py --inventory`, el runner de casos, y
   `check_commit_trailers.py` si la puerta se pone ahi.
3. **Re-juicio mio antes del commit de cierre.** Exijo que el negativo de SLIP-1 se acredite por
   **mutacion**: con la clausula nueva retirada, el vector 9/10 debe volver a pasar. Un verde que el
   codigo de 150ff371 tambien produce no discrimina.
4. **Maximo 2 iteraciones** (r4, r5). Si en r5 sigue abierto SLIP-1, escala al operador humano: la
   decision de donde vive el ancla ya fue suya (opcion A), y la de quien la firma tambien lo es.

## Cierre

**CHANGE-REQUIRED.** Lo entregado en r3 es un avance real y verificado: la identidad ya no la
escribe el forjador dentro del evento, la existencia se exige, el clon limpio esta verde y los 108
del Analista por fin se cuentan. Pero el registro que ahora **es** la autoridad no tiene puerta: una
identidad git cualquiera, sin claim, le anade una linea que ata un key_id nuevo a otro actor, y las
cinco puertas salen en 0.

La pregunta del Arquitecto tiene respuesta, y es la respuesta corta: **lo escribe cualquiera, con un
trailer.**

-- Analista, checker independiente, 2026-08-17
