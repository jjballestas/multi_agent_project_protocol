---
id: TASK-0423
title: El enlace de firma exige la clave que el registro ya retiro -- la rotacion esta implementada a medias
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0423-el-enlace-de-firma-exige-la-clave-que-el-registro-retiro.md
created: 2026-08-21
reviewer: Analista
intake:
  type: fix
  goal: >
    El corte v1.19.1 introdujo EVENT_AUTH_KEY_REGISTRY.json con status y valid_through_seq, y
    enseno al VERIFICADOR a honrarlo (runtime/eventlog.py:759-775 resuelve la entrada del
    registro, exige que una clave active no tenga frontera y que una retired si la tenga, y
    rechaza eventos por encima de valid_through_seq). Pero el ENLACE DE FIRMA no se actualizo:
    ensure_attested_actor_key_binding (runtime/submit_intent.py:1089 y :1095) fija el literal
    "{slug}:v1" y "{slug}-hmac:v1". El codigo contiene por tanto las DOS mitades de la rotacion
    y no se ponen de acuerdo: el registro puede retirar una clave que el enlace sigue exigiendo.
    Reportado por la instancia NOVA (2026-08-21T21:30Z), que lo sufrio en produccion con
    jheredia-hmac:v1 retired valid_through_seq 1009 y jheredia-hmac:v2 active, recibiendo
    "IntentValidationError: event_auth key_id for jheredia must be jheredia-hmac:v1" -- se le pedia
    firmar con la clave retirada, y obedecer habria producido eventos invalidos por encima de 1009.
    En ESTE hub el defecto NO esta dormido: actor_auth_enforce resuelve a True por el override
    externo, asi que el enlace SI se ejecuta para los actores tier signer; lo unico que evita el
    bloqueo es que las cuatro claves del registro del hub siguen en :v1 y active. El hub esta a UNA
    rotacion de bloquear a su propio firmante.
  acceptance:
    - "AC1: con un registro que declara <actor>-hmac:v2 como unica clave active y :v1 como retired
      con valid_through_seq, el enlace ACEPTA la firma con v2 y RECHAZA la firma con v1."
    - "AC2: SIN fichero de registro, la conducta es byte a byte la anterior -- se conserva el
      literal {slug}-hmac:v1 -- de modo que una instancia que nunca roto no cambia de conducta.
      Acreditar con el par: sin registro + v1 PASA, sin registro + v2 RECHAZA."
    - "AC3: FALLA CERRADO. Si el registro no declara EXACTAMENTE UNA clave active para el actor
      (cero activas, o dos), el enlace RECHAZA. Acreditar los dos casos por separado."
    - "AC4: el banco de pruebas se ejercita con actor_auth_enforce REALMENTE ACTIVO. Un banco sin
      enforce da verde en todos los casos porque la funcion se rinde en su guarda de entrada
      (submit_intent.py:1068) y no llega a evaluar nada: hay que exigir que un caso MUERDA antes de
      creerse ningun verde. NOVA reporta haber caido en ese banco falso; el negativo es obligatorio."
    - "AC5: no se amplia el alcance al ed25519 (submit_intent.py:1089). El registro solo versiona
      claves HMAC y no hay defecto que pida tocar la otra linea."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/submit_intent.py
    - Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    - scripts/
  out_of_scope:
    - "NO se rota ninguna clave del hub en esta tarea. Se repara el enlace; rotar es otro acto."
    - "NO se toca runtime/eventlog.py: el verificador ya honra el registro correctamente."
    - "NO se toca la linea del ed25519 (actor_auth): sin defecto que lo pida (ver AC5)."
  risk: medium
  estimate: M
---

# TASK-0423 -- el enlace de firma exige la clave que el registro ya retiro

## El hecho, verificado en este arbol

    runtime/eventlog.py:759     registry_entry = event_auth_key_registry(config, root=root).get(key_id)
    runtime/eventlog.py:766     valid_through = registry_entry.get("valid_through_seq")
        -> el VERIFICADOR honra status y frontera de secuencia

    runtime/submit_intent.py:1089    expected_actor_keyid = f"{slug}:v1"
    runtime/submit_intent.py:1095    expected_event_keyid = f"{slug}-hmac:v1"
        -> el ENLACE DE FIRMA ignora el registro y fija el literal v1

Las dos mitades de la rotacion conviven y se contradicen. No es una omision de diseno: el mismo
corte que enseno al verificador a leer `status: retired` dejo al enlace exigiendo la clave retirada.

## Por que ha estado invisible, y donde muerde

`ensure_attested_actor_key_binding` se rinde antes de comprobar nada si `actor_auth_enforce` no esta
activo (`submit_intent.py:1068`), y ese flag **solo** puede venir del override externo, porque
`actor_auth_event_state` (`eventlog.py:295-301`) lo descarta expresamente del config:

    merged.pop("actor_auth_enforce", None)
    merged.pop("actor_auth_config", None)
    merged.update(actor_auth_runtime_override(root))

De ahi que NOVA lo describa como dormido. **En este hub no lo esta**: el override tiene
`actor_auth_enforce: True`, medido hoy. Aqui el guardia esta armado y solo le falta el disparador,
que es la primera rotacion de una clave HMAC. El dano cae ademas justo en la via employee-run --
la que existe para atribuir el trabajo a un humano con su ed25519 -- que es donde mas caro sale y
donde menos ojos hay.

## Sobre el parche que NOVA ya aplico

NOVA parcheo una linea en su instancia bajo decision propia
(DECISION-NOVA-BINDING-CLAVE-ACTIVA-DEL-REGISTRO-20260821, seq 1307-1309, commit 5a4c922) y lo
declara como delta local, retirable en cuanto el hub emita el arreglo de raiz. Su calibracion 7/7
esta reproducida arriba como AC1-AC3 y su trampa metodologica como AC4. **La propuesta se estudia,
no se adopta a ciegas**: el arreglo del hub se acredita con su propio banco.

## Banco de la instancia NOVA -- entregado el 2026-08-22, y va aqui para que no muera en el buzon

Se lo pedimos y lo mandaron: los CASOS, no el diagnostico. Es material de partida, no un banco
adoptado: el arreglo del hub se acredita con su propio banco y con su propio checker.

### Lo primero es como se construye, porque ahi estuvo la trampa

`ensure_attested_actor_key_binding` sale por `if not actor_auth_enforce_enabled(config, root):
return`, y `actor_auth_enforce` **solo** puede venir del override -- `eventlog.py:295-301` lo
descarta del config a proposito. **Un banco que ponga el enforce en `protocol.config.json` no
ejercita nada y da TODO en verde.** A NOVA su primera pasada le dio los siete casos verdes y era un
banco falso.

Las **cuatro** condiciones tienen que darse a la vez:

    1. EVENT_STATE_RUNTIME_CONFIG_PATH apuntando a un override propio del banco
    2. ese override con event_state.actor_auth_enforce = true
       (y SOLO actor_auth_enforce / actor_auth_config / event_auth: cualquier otra clave
        hace que validate lo rechace con "unsupported event_state keys")
    3. attested_instancing.enabled = true en el config
    4. el actor con tier "signer" en el agent_registry, o la funcion sale por la rama
       de no-firmante antes de llegar al enlace

**El canario, y esto es lo exigible (AC4):** antes de creerse ningun verde, comprobar que
`actor_auth_enforce_enabled(config, root)` devuelve `True` **y** que un caso que debe morder muerde.
Si los siete salen verdes a la primera, el banco esta roto, no el codigo arreglado.

### Los siete casos

| # | key_id declarado en el override | registro | esperado |
|---|---|---|---|
| 1 | `<slug>-hmac:v2` | v1 retired 1009, v2 active | PASA |
| 2 | `<slug>-hmac:v1` | v1 retired 1009, v2 active | RECHAZA -- la clave retirada sigue prohibida |
| 3 | `<slug>-hmac:v3` (inexistente) | v1 retired, v2 active | RECHAZA |
| 4 | `<slug>-hmac:v2` | solo v1 retired, ninguna active | RECHAZA -- falla cerrado |
| 5 | `<slug>-hmac:v2` | v2 active Y v3 active | RECHAZA -- falla cerrado por ambiguedad |
| 6 | `<slug>-hmac:v1` | SIN fichero de registro | PASA -- conducta anterior intacta |
| 7 | `<slug>-hmac:v2` | SIN fichero de registro | RECHAZA -- conducta anterior intacta |

**6 y 7** son los que acreditan que una instancia que NO roto no cambia de conducta; sin ellos el
arreglo podria estar aflojando la puerta para todo el mundo sin que nadie lo viera. **4 y 5** son la
parte que no estaba en el defecto original: un registro que no declara exactamente una clave activa
para el actor tiene que rechazar, no elegir por su cuenta.
