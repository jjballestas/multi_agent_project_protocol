---
id: TASK-0414
title: El replay acusa de MANIPULACION cuando lo unico que le falta es la llave -- key_unavailable no es invalid_signature
status: blocked
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0414-el-replay-acusa-de-manipulacion-cuando-solo-le-falta-la-llave.md
created: 2026-08-16
reviewer: Analista
intake:
  type: infra
  goal: >
    Peticion de sustrato de la instancia NOVA, medida por su Arquitecto y con prioridad
    DECISION-0118. Una rotacion de claves v2 --autorizada, necesaria y limpia-- dejo 1.009 eventos
    historicos marcados `invalid_signature` porque el material de firma v1 ya no existe. Es decir:
    el estado canonico ACUSA DE MANIPULACION a su propia historia cuando lo cierto es que el
    verificador se quedo sin llave. La consecuencia operativa es HEAD rojo para cualquiera que clone
    y los peers de esa instancia parados a proposito hasta este arreglo. El defecto es semantico y
    de la familia mas cara que llevamos hoy: confundir "NO PUEDO verificar" con "la verificacion
    FALLA" convierte una frontera declarable en una acusacion, y ademas es irreversible en la
    practica, porque el material v1 no vuelve.
  acceptance:
    - "AC1 (la distincion, en el replay): `runtime/protocol_replay.py` distingue key_unavailable --
      no hay material de firma para el key_id que el evento declara -- de invalid_signature --
      el material existe y la firma NO verifica. Son estados distintos y se nombran distinto."
    - "AC2 (consecuencias distintas, que es el objeto de la tarea): key_unavailable CONSTA como
      frontera declarada y NO pone HEAD rojo; invalid_signature sigue siendo la acusacion que es y
      sigue fallando cerrado. Se acredita con los DOS casos por exit code sobre un log de prueba."
    - "AC3 (el negativo que cubre el modo ciego, y es el que mas vale): una puerta que compara dos
      artefactos AFECTADOS POR LA MISMA CAUSA no puede detectar esa causa. En NOVA, el chequeo que
      comparaba snapshot contra reconstruccion fue CIEGO precisamente porque ambos lados rechazaban
      igual. El negativo debe reproducir ese modo: introducir key_unavailable y comprobar que el
      instrumento lo DISTINGUE en vez de cancelarse contra si mismo."
    - "AC4 (no se relaja la seguridad): un evento con material presente y firma mala sigue siendo
      rechazado. Se acredita por MUTACION -- perturbar la firma de un evento cuyo key_id SI tiene
      material debe poner el replay en rojo. Si tras el arreglo eso pasa, se ha comprado comodidad
      con integridad."
    - "AC5 (la poblacion, no el ejemplar): el arreglo se mide contra los 1.009 eventos del caso real,
      no contra uno sintetico. Cuantos pasan a key_unavailable y cuantos siguen en
      invalid_signature. Si el segundo numero no es cero, eso es un hallazgo, no un fallo del fix."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/protocol_replay.py
  out_of_scope:
    - "Regenerar el snapshot a cero rechazos para que el estado quede limpio: NOVA lo rechazo
      explicitamente aun siendo suyo el error, y aqui se ratifica. Borrar la frontera no es
      arreglarla; el ledger debe poder decir 'aqui no puedo verificar' sin mentir en ninguno de los
      dos sentidos."
    - "La politica de custodia y rotacion de claves: es la causa upstream y merece via propia."
    - "Reconstruir o re-firmar el material v1: prohibido -- seria re-firmar historia."
  risk: medium
  estimate: M
---

# TASK-0414 -- el ledger no debe acusar de lo que no puede saber

## El caso, medido en campo

Una rotacion de claves **autorizada y correcta** dejo **1.009 eventos** historicos marcados
`invalid_signature`. Ninguno fue manipulado: el material de firma v1 se perdio, que es la
consecuencia normal de rotar. El verificador no distingue **falta de llave** de **firma mala**, asi
que reporta la unica etiqueta que tiene -- y esa etiqueta es una acusacion.

Efecto: **HEAD rojo para quien clone**, y una instancia entera con sus peones parados a proposito.

## Por que es un defecto y no una politica conservadora

Fallar cerrado ante lo desconocido es correcto. **Nombrar lo desconocido como fraude, no.** Un
ledger que no puede verificar un tramo tiene que poder decir exactamente eso -- ni "esto esta bien"
ni "esto esta manipulado" -- porque las dos afirmaciones son falsas y la segunda es ademas
irreparable: el material v1 no vuelve, asi que la acusacion seria permanente.

## El AC3 es el que ensena algo nuevo

En NOVA, la puerta que comparaba **snapshot contra reconstruccion** no vio nada raro: **ambos lados
rechazaban igual**. De ahi sale una propiedad general que conviene tener escrita:

    una puerta que compara dos artefactos AFECTADOS POR LA MISMA CAUSA
    no puede detectar esa causa -- se cancela contra si misma

Es pariente directo del R-5 de este hub (exenciones que envejecen a muertas o invertidas y siguen
declarandose sanas). Por eso el negativo no puede limitarse a "el fix funciona": tiene que
reproducir **el modo ciego**.

## Lo que NO se hace, y por que se declara aqui

**No se regenera el snapshot a cero rechazos.** NOVA lo rechazo siendo suyo el error, y se ratifica:
es el mismo principio que impide reescribir historia publicada. Limpiar el sintoma borraria la
frontera en vez de declararla.

## Remediation r2 - declared-key event auth

The verifier now selects HMAC material by `event_auth.key_id`, never by the event actor. An absent
key id is non-fatal only when an independently verifiable event of type
`event_auth.key_rotation_declared` contains it in `payload.unavailable_key_ids`. A declaration is
verified with presently configured material before its list is trusted; an unknown key id cannot
authorize itself. The complete boundary list is returned as the structured
`protocol_state_drift(...)["event_auth_boundaries"]` field and is also consumed by the canonical
validator. It is deliberately outside materialized protocol state, so observing the boundary does
not manufacture drift against a snapshot created while the old key was available.

Measured fixture population: 1,009 v1 events, one v2-signed rotation declaration, and two valid v2
events. Results: `key_unavailable=1009`, `invalid_signature=0`. Counterproof exit codes are:
declared v1 `0`; undeclared nonexistent key id with a false signature `1`; present material with a
false signature `1` (`invalid_signature`). The superseded actor-attestation discriminator from
`be3edb87` is reverted. `actor_auth` does not have the same actor-based lookup defect: it checks the
declared `keyid` against the actor binding and then indexes the public-key registry by that exact id.

## Remediation r3 - governed versioned key registry

`Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json` is the versioned, material-free authority for
event-auth key existence, actor identity, and lifetime. Runtime configuration may supply secret
material for a registered key, but it cannot create an identity. A registered key without locally
resolvable material is `unresolved_key` and non-fatal; an unregistered id, wrong actor, event after
`valid_through_seq`, or bad signature with material present remains fatal.

The drift CLI publishes the complete archive-inclusive boundary cardinal and key ids. The 1,009
event population remains non-fatal with zero invalid signatures. Counterproof exit codes are:
registered historical key `0`; unregistered id `1`; bad present signature `1`; one live key used as
another actor `1`; retired key after its temporal boundary `1`. Registry changes are a governed
surface: claim, TASK trailer, and independent review are required; no secret material is stored.
