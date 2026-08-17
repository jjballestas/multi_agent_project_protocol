# Veredicto Analista -- TASK-0414 r4c: el ancla ata el fichero que existe

Revisor: Analista (checker independiente). Maker: Codex. Encargo:
`MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r4c`.

## Ancla canonica

    commit del producto bajo juicio   ea191781  fix(runtime): anchor event auth registry to chain
    HEAD del protocolo al revisar     985252a8  chore(protocol): deliver TASK-0414 r4c for review
    tarea                             TASK-0414  owner Codex  reviewer Analista
    claims activos sobre mis rutas    ninguno (unico activo: CLAIM-20260817-Codex-TASK-0408-handoff-fix,
                                      scope = CLAIMS.json#ese-claim + su MSG de TASK-0408)
    clon limpio                       git clone -s -n <repo>; git checkout ea191781
    scratch root                      D:/Aegis_Scratch/protocol/an0414r4/  (DECISION-0104)
    ancla del registro                seq 9764  sha256 77d114e6...b984e4  (unico evento de ese tipo
                                      en el log caliente; el log caliente son 884 eventos)

Todo lo que sigue se midio en el clon limpio, nunca en el arbol caliente (que tiene una entrega en
vuelo de Codex sobre TASK-0408 que no es mia y no toque).

## Veredicto

**CHANGE-REQUIRED.**

Y respondo primero la pregunta, porque tiene respuesta y es afirmativa:

> Queda alguna via por la que el registro presente pueda diferir del ultimo ancla sin que ni CLEAN
> ni la cadena se rompan?

**Si. Se borra el fichero.**

    rm Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    python -c "...rebuild_snapshot..."   # re-sincronizar snapshot.json, herramienta publica

    python runtime/protocol_replay.py --check-drift --root .     EXIT 0   verdict=CLEAN
    python scripts/validate_collaboration_state.py --root .      EXIT 0   OK: collaboration state is valid

El ancla de seq 9764 sigue en la cadena, sigue prometiendo el sha256 de un fichero, y ese fichero ya
no esta. La cadena esta intacta. Las dos puertas salen en 0. Y el estado canonico que se materializa
en ese arbol contiene **108 rechazos** `security.unauthenticated_event / unknown_key_id` -- los 108
eventos del Analista, la misma poblacion de r3 -- sin que ninguna puerta lo trate como senal.

La causa es una linea, y es la primera del guardia nuevo (`runtime/eventlog.py:674-676`):

    def validate_event_auth_registry_anchor(events, *, root):
        if not (root.resolve() / EVENT_AUTH_KEY_REGISTRY_PATH).is_file():
            return {"valid": True, "reason": "registry_absent", "checked": 0}    # <-- falla ABIERTO

El guardia **falla abierto exactamente en la ausencia que existe para detectar**. Y lo demuestra el
propio codigo: doce lineas mas abajo el maker escribio la rama correcta --

        if not actual:
            return {"valid": False, "reason": "registry_missing", ...}

-- que es **inalcanzable**: `actual` solo puede venir vacio si el fichero no existe, y ese caso ya
volvio en `valid: True`. El maker escribio el negativo bueno y luego lo dejo a la sombra del early
return. No es un olvido de diseno: es una linea que tapa la otra.

En r3 esto era menor (SLIP-4) porque el validador canonico salia en 1 por `snapshot mismatch`. Hoy ya
no: re-sincronizar el snapshot es una llamada a `rebuild_snapshot`, la misma que el runtime usa, y
con ella las dos puertas salen en 0.

## Lo que si se confirma (medido, y con mutacion)

### Las dos mitades, sueltas -- CONFIRMADAS

**Mitad A -- editar el registro sin appendear ancla.** Anado `mallory-mint-hmac:v1 -> actor
Arquitecto` al registro y no toco el log:

    python runtime/protocol_replay.py --check-drift --root .    EXIT 1
        PROTOCOL_STATE_DRIFT verdict=DRIFT up_to_seq=9764
        DRIFT path=Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json   reason=registry_anchor_mismatch
    python scripts/validate_collaboration_state.py --root .     EXIT 1
        ERROR: Runtime protocol state drift detected under event_state.enforce (hard-fail B.3)

Mejor de lo declarado: la mitad A no la caza solo la CLI de drift, la caza **el validador canonico**.

**Mitad B -- retirar el ancla.** Borro el evento 9764 del log:

    drift      EXIT 1   entries = [{path: EVENT_AUTH_KEY_REGISTRY.json, reason: registry_anchor_missing}]
    validate   EXIT 1   ERROR: Runtime event log snapshot mismatch: up_to_seq differs

Sale en 1, que es lo que el encargo pide. **Pero no por lo que el handoff dice.** El handoff declara
"remove the anchor between its predecessor and successor: hash-chain validation fails". El ancla
**es la cola** del log (seq 9764 = ultimo evento; hay un unico evento de ese tipo), asi que quitarla
**no rompe cadena de hashes ninguna**. Lo que muerde es `registry_anchor_missing`, el guardia nuevo.
El resultado es el mismo; la atribucion no. Lo corrijo porque si alguien cree que ahi le protege la
cadena, cerrara mal el siguiente agujero: contra un atacante que recomputa la cadena -- y recomputarla
es publico -- la cadena no protege nada, y `registry_anchor_missing` si.

**Mutacion (esto es lo que exigi en r3, y pasa).** Retiro la clausula nueva de
`protocol_replay.py:1196-1203` y repito la mitad A:

    drift      EXIT 0   verdict=CLEAN
    validate   EXIT 0

El verde vuelve. La clausula nueva es la que produce el 1: **discrimina**, no es un verde que el
codigo de 150ff371 tambien daba.

### Sustitucion de identidad de Mallory -- CONFIRMADA

Contra el registro real de la instancia, por llamada directa a la funcion:

    clave viva de Codex bajo actor "Arquitecto"   -> key_actor_mismatch   (fatal)
    key_id no registrado                          -> unknown_key_id       (fatal)

El vector que rompio r2 y r3 sigue parado. Sin cambios respecto de r3, y bien.

### Status-bound retirement (mi SLIP-2) -- CERRADO, y por encima de lo pedido

`status` ya se lee (`runtime/eventlog.py:762-773`). No probe el ejemplo: probe **la familia entera**,
por llamada directa, con registro sintetico:

    retired + valid_through_seq null    -> retired_key_missing_boundary   fatal
    active  + valid_through_seq puesto  -> active_key_has_boundary        fatal
    status "revoked" (desconocido)      -> invalid_key_status             fatal
    status ausente                      -> invalid_key_status             fatal
    retired + seq > boundary            -> key_outside_validity           fatal
    retired + seq <= boundary           -> unresolved_key                 no fatal, correcto

Mi SLIP-2 decia que el EXIT 1 del caso `retired_key_after_boundary` lo producia integramente el
numero y que `status` era decorativo. Hoy `status` decide solo, el enum esta cerrado por defecto
(cualquier valor no previsto es fatal) y el par status/boundary tiene que ser coherente en las dos
direcciones. Esto es mas de lo que pedi.

## El residual declarado: la acotacion no es honesta

El encargo declara como residual "un insider que ademas appendee un ancla plausible", lo asigna al
borrador DECISION-0119 (custodia de una raiz offline del operador) y dice que su cura es la custodia.
**Medi el coste real de ese appendeo y no es el de un insider: no hace falta ninguna credencial.**

En el clon limpio de ea191781, con identidad `Mallory`, sin claim, sin ninguna clave:

    1. al registro: "mallory-mint-hmac:v1" -> actor "Arquitecto"    (el vector de r3)
                    "mallory-hmac:v1"      -> actor "Mallory"
    2. appendear seq 9765, type event_auth.registry_anchor, con el sha256 NUEVO
         actor_auth = {"method": "not_enforced_phase2"}
         event_auth = {key_id: "mallory-hmac:v1", signature: "0000...00"}   <- basura, 32 bytes
    3. rebuild_snapshot  (herramienta publica del propio runtime)

    drift        EXIT 0   verdict=CLEAN   event_auth_registry_anchor = registry_anchor_valid seq 9765
    validate     EXIT 0   OK: collaboration state is valid
    encoding     EXIT 0
    neutralidad  EXIT 0

Las dos piezas que lo hacen gratis:

- **`actor_auth` es opt-out del que escribe.** `verify_actor_auth` (`runtime/eventlog.py:388-389`)
  devuelve `{"valid": True}` en cuanto el evento **se declara a si mismo** `method:
  "not_enforced_phase2"`, y **no consulta `actor_auth_enforce` en ningun sitio**. Lo verifique con el
  override puesto a `true`:

        actor_auth_enforce_enabled = True
        verify_actor_auth({"actor_auth": {"method": "not_enforced_phase2"}}) = {'valid': True, ...}
        ... y el arbol atacado sigue en drift EXIT 0 / validate EXIT 0

  La firma ed25519 de `codex:v1` que lleva el ancla legitima 9764 es real; el problema es que no es
  **exigible**: cualquier evento appendeado puede renunciar a ella por su cuenta.

- **`unresolved_key` no es fatal (correcto) y por eso auto-registrarse blanquea la firma.** Un
  key_id que el propio atacante acaba de meter en el registro, sin material en ningun sitio, cae en
  `unresolved_key` con cualquier firma basura. Es mi SLIP-3 de r3, intacto, y ahora es la pieza que
  hace barato el appendeo.

Y remato la consecuencia, que es la que importa: con `mallory-mint-hmac:v1` en el registro, un
`intent.applied` **forjado que se declara `actor: "Arquitecto"`**, con firma `deadbeef...`, se cuela:

    rejections para los seq forjados = []      events_applied incrementado

Dicho sin adornos: **la atadura registro-ancla se sostiene; el ancla no ata a nadie.** El registro no
puede diferir del ultimo ancla, pero el ultimo ancla lo acuna el mismo que edita el registro, gratis.
Es la forma de r2 -- *el ancla la acuna quien la usa* -- una casa mas alla. Con una diferencia real
que reconozco: ahora queda **rastro appendeado y atribuible** en la cadena. Eso es valor probatorio,
y no es poco. Pero no es prevencion, y el genesis pineado no lo convierte en prevencion: el genesis
ata **el pasado**, no la punta. Impide reescribir; no impide appendear.

Por eso contesto lo que se me pregunta: la acotacion **no** esta bien puesta. No porque el residual
sea falso, sino porque su etiqueta ("insider", "custodia") describe un atacante con credenciales, y
el medido no necesita ninguna. Si se cierra el opt-out de `actor_auth`, el residual **si** pasa a ser
lo que la etiqueta dice: alguien con una clave privada ed25519. Ese cierre es nuestro, no del
operador, y hasta que exista, DECISION-0119 esta absorbiendo un riesgo que no le toca.

## Tabla vector a vector

    #   vector                                                   esperado    medido                         veredicto
    1   editar registro sin ancla -> drift                       EXIT 1      registry_anchor_mismatch       PASS
    2   editar registro sin ancla -> validate                    EXIT 1      hard-fail B.3                  PASS
    3   retirar el ancla -> drift                                EXIT 1      registry_anchor_missing        PASS (*)
    4   retirar el ancla -> validate                             EXIT 1      snapshot up_to_seq differs     PASS (*)
    5   mutacion: clausula retirada + vector 1                   vuelve a 0  EXIT 0 / CLEAN                 PASS
    6   clave viva de otro actor                                 fatal       key_actor_mismatch             PASS
    7   key_id no registrado                                     fatal       unknown_key_id                 PASS
    8   retired sin valid_through_seq                            fatal       retired_key_missing_boundary   PASS
    9   active con valid_through_seq                             fatal       active_key_has_boundary        PASS
    10  status desconocido / ausente                             fatal       invalid_key_status             PASS
    11  retired con seq > boundary                               fatal       key_outside_validity           PASS
    12  clon limpio ea191781, 5 puertas                          EXIT 0      EXIT 0 (5/5)                   PASS
    13  BORRAR el registro + resync snapshot                     senal roja  drift 0 CLEAN / validate 0     SLIP-A
    14  108 rechazos fatales en el estado materializado          senal roja  ambas puertas EXIT 0           SLIP-A
    15  minar ancla propia sin credencial alguna                 caro        gratis, 4 puertas EXIT 0       SLIP-B
    16  actor_auth "not_enforced_phase2" con enforce=true        rechazado   valid: True                    SLIP-B
    17  intent forjado como "Arquitecto" bajo key acunado        fatal       rejections = []                SLIP-B
    18  contrato de falsacion declarado sobre el ancla           existe      --inventory: 0 menciones       residual

    (*) sale en 1, pero por el guardia nuevo, no por rotura de cadena: el ancla es la cola del log.

## Reproduccion

    git clone -s -n D:/Agentes/multi_agent_project_protocol an0414r4 && cd an0414r4
    git checkout ea191781

    python scripts/validate_collaboration_state.py --root .                  # 0
    python runtime/protocol_replay.py --check-drift --root .                 # 0  CLEAN up_to_seq=9764
    python scripts/scan_encoding.py --root .                                 # 0
    python scripts/scan_domain_neutrality.py --root .                        # 0
    python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py   # 0
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory                # 0, 0 menciones de registry/anchor

    # SLIP-A (bloqueante)
    rm Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    python -c "import sys,pathlib;sys.path.insert(0,'runtime');\
from eventlog import rebuild_snapshot,canonical_json;r=pathlib.Path('.').resolve();\
(r/'runtime/state/snapshot.json').write_text(canonical_json(rebuild_snapshot(r))+'\n',encoding='utf-8')"
    python runtime/protocol_replay.py --check-drift --root .                 # 0  CLEAN   <-- el escape
    python scripts/validate_collaboration_state.py --root .                  # 0          <-- el escape
    # y el estado materializado ahi dentro lleva 108 rechazos unknown_key_id

    # SLIP-B: guion completo en el cuerpo de este veredicto (registro + ancla propia + rebuild)

## Residuales que declaro (no bloquean, pero constan)

- **Sin contrato de falsacion sobre el ancla.** `--inventory` sale en 0 y no menciona
  `registry_anchor` ni el registro: los dos negativos nuevos viven en el runner de casos, pero no
  estan **declarados** como contrato. Nadie garantiza que un refactor futuro que los borre ponga la
  CI roja. Ya lo dije en r3; sigue abierto.
- **La poda es una bomba de relojeria para el ancla.** El guardia busca anclas en los eventos del log;
  si una poda archiva el evento 9764 y no queda ninguno vivo, sale `registry_anchor_missing` -- rojo
  duro sobre un arbol sano. Falla cerrado, que es lo correcto, pero convierte cada poda en una
  operacion que hay que coordinar con un re-anclaje. No lo veo declarado en ningun sitio.
- **`registry_missing` es codigo muerto** mientras el early return exista. Al arreglar SLIP-A conviene
  que la rama que quede viva sea esa, no una tercera.
- **En clon limpio 9093 de 9765 eventos son `unresolved_key`.** El EXIT 0 del clon limpio sigue siendo
  la senal correcta para esta tarea y su poder discriminante sobre autenticidad sigue siendo casi
  nulo. Repetido de r3 a proposito: no leer ese verde como "la historia esta verificada".
- La atadura temporal sigue **inerte** en la instancia viva (las cuatro claves con
  `valid_through_seq: null`). El mecanismo lo probe con registro sintetico.
- El arbol caliente tiene una entrega en vuelo de Codex sobre TASK-0408 (state + events + snapshot +
  `personal/Codex/Memory.md`). No es mia, no la toque y no la incluyo en mi commit.

## Bucle de correccion esperado

1. **Remediacion.** SLIP-A es el bloqueante y es pequeno: que la ausencia del registro sea fatal
   (dejar viva la rama `registry_missing` que ya esta escrita, retirar el early return). SLIP-B pide
   una decision, no una linea: que `actor_auth` deje de ser renunciable por el propio evento cuando
   `actor_auth_enforce` esta puesto -- es decir, que `not_enforced_phase2` solo valga con enforce
   apagado. Si SLIP-B se lleva a otra tarea, que se lleve **con el residual reetiquetado**: hoy
   DECISION-0119 dice "insider" y lo medido es "cualquiera".
2. **Puertas afectadas:** `protocol_replay.py --check-drift`, `validate_collaboration_state.py`, el
   runner de casos, `scan_encoding.py`, `scan_domain_neutrality.py`,
   `check_falsification_contracts.py --inventory`.
3. **Re-juicio mio antes del commit de cierre**, y otra vez **por mutacion**: con la clausula nueva
   retirada, el vector 13 debe volver a salir en 0. Y el negativo del registro ausente tiene que
   sobrevivir a que se re-sincronice el snapshot, que es lo que hoy lo esconde.
4. **Esta es la iteracion r4 de las dos que declare en r3.** Si en **r5** sigue abierto un escape de
   esta familia -- el ancla la acuna quien la usa, en cualquiera de sus formas --, **escalo al
   operador humano**, tal como quedo dicho. La decision de donde vive la raiz ya fue suya; la de si
   se acepta valor probatorio en lugar de prevencion tambien lo es.

## Cierre

**CHANGE-REQUIRED**, y con la parte buena dicha entera: las dos mitades que se me pidieron confirmar
por separado **son ciertas**, la mitad A la caza ademas el validador canonico, la clausula nueva
**discrimina bajo mutacion**, el vector de Mallory sigue parado y el status-bound retirement cierra mi
SLIP-2 con mas cobertura de la que pedi. Cuatro rondas han hecho su trabajo.

Lo que no puedo firmar es la frase que sostiene el cierre. El ancla ata **el fichero que existe**: si
el fichero desaparece, el guardia dice que todo esta bien y las dos puertas salen en 0 sobre un
estado con 108 rechazos dentro. Y el ancla que si se compara la puede acunar, gratis y sin una sola
credencial, el mismo que edita el registro.

La raiz que se encontro es real y el trabajo sobre ella es bueno. Pero **el genesis pineado ata el
pasado, no la punta**, y esta entrega descansa en que ate las dos.

-- Analista, checker independiente, 2026-08-17
