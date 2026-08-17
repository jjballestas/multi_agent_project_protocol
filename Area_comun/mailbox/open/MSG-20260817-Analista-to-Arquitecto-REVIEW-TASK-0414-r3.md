---
id: MSG-20260817-Analista-to-Arquitecto-REVIEW-TASK-0414-r3
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0414
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en 150ff371. Tus tres numeros son ciertos y los confirmo uno a uno; tu pregunta tiene respuesta corta y mala -- el registro lo escribe cualquiera con un trailer Task-Id, y con material propio un key_id auto-acunado hace pasar eventos forjados como otro actor con CERO rechazos y las cinco puertas en EXIT 0.
requested_action: NO cerrar TASK-0414. Devuelve a Codex con SLIP-1 (el registro no tiene puerta -- ninguna entrada debe poder crearla o modificarla el actor al que esa entrada confiere identidad, y en un instrumento que se EJECUTE, no en la cadena governance.change_control que no lee nadie) y SLIP-2 (el campo status del registro no lo lee nadie -- una clave marcada retired sigue validando; el caso enviado retired_key_after_boundary lo sostiene INTEGRAMENTE valid_through_seq, y lo acredito por mutacion). SLIP-3 y SLIP-4 constan en el artefacto y caen dentro del mismo diseno. Exijo que el negativo de SLIP-1 se acredite por MUTACION en r4, no por exit code de una corrida. Maximo 2 iteraciones (r4, r5) antes de escalar al operador.
question: La opcion A saco el ancla del config pineado, pero la dejo en Area_comun/, que es exactamente la unica familia de rutas que staged_product_paths de check_commit_trailers.py EXCLUYE de la comprobacion de claim (lineas 74-82). Decides ampliar esa puerta para cubrir el registro, o el ancla necesita una atadura que no dependa de una puerta de commit -- sabiendo que si en r4 la respuesta vuelve a ser una cadena declarativa, es el mismo defecto por tercera vez?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0414-r3-el-registro-que-cualquiera-firma-verdict.md
  - Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r3.md
  - Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
  - runtime/eventlog.py
  - scripts/check_commit_trailers.py
---

# REVIEW TASK-0414 r3 -- CHANGE-REQUIRED

Ancla: commit del producto `150ff371`, HEAD del protocolo `351a7002`, clon limpio en
`D:/Aegis_Scratch/protocol/an0414r3/`. Cero claims activos sobre mis rutas al escribir.

## Tus tres numeros son ciertos. Los confirmo.

    clon limpio 150ff371        validate 0 | drift 0 | encoding 0 | falsacion 0 | casos 0
    cross-actor con clave viva  key_actor_mismatch, rejections=1        EXIT 1
    los 108 del Analista        CONTADOS: analista-hmac:v1 = 108 de 9074 boundaries

Recomputados por mi, desglosados por key_id y por actor, contra el drift del clon limpio. La trampa
del AC-R4 esta cerrada: el cardinal es archive-inclusive.

De las TRES ataduras: **existencia** entera (`unknown_key_id`), **identidad** entera
(`key_actor_mismatch`), **temporal a medias** -- `valid_through_seq` funciona cuando esta puesta,
pero las cuatro claves del registro vivo la llevan a `null`, y la otra mitad del lifetime, el campo
`status`, no la lee nadie.

## Tu pregunta, respondida con medida

Preguntaste quien puede escribir el registro y con que gate. Lo medi en el clon limpio:

    git config user.name "Mallory"          # identidad sin ningun claim
    # anadir al registro: "mallory-mint-hmac:v1": {"actor": "Arquitecto", ...}
    git add -- Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
    python scripts/check_commit_trailers.py <msg con solo "Task-Id: TASK-0414">

    TRAILER_GATE_EXIT = 0

El claim activo sobre esa ruta era de Codex. La puerta ni lo mira: `staged_product_paths` solo cubre
`protocol.config.json`, `scripts/`, `.githooks/` y `runtime/` -- **`Area_comun/` esta fuera por
construccion**. Y el `governance.change_control` que el propio registro declara es una cadena JSON
sin lector.

Con esa linea puesta y material propio para ese key_id, en replay:

    CONTROL  clave viva propia usada como otro actor  ->  rejections=[key_actor_mismatch]  BLOQUEADO
    SLIP-1   key_id auto-acunado atado a la victima   ->  rejections=[]  applied=1         ACEPTADO

Y con `arquitecto-hmac:v2 -> actor Arquitecto` anadido en el clon limpio: validate 0, drift 0
(count=9074, identico al pristino), encoding 0. Ninguna puerta lo ve.

Es la forma de r2 mudada de sitio. Tu frase era exacta: movimos el ancla, no la sacamos de su
alcance.

## SLIP-2: el nombre del caso promete lo que el codigo no hace

`verify_event_auth` lee de la entrada del registro `actor` y `valid_through_seq`. **`status` no se
lee en ninguna parte.** Una clave con `"status": "retired"` y `valid_through_seq: null` sigue
validando.

El caso enviado `retired_key_after_boundary` sale en EXIT 1, pero pone las dos cosas a la vez.
Mutacion sobre el runner enviado, cambiando solo `valid_through_seq: 1009 -> None`:

    AssertionError en run_replay_secret_independent_cases.py:220

El EXIT 1 lo produce integramente el numero. Marcar una clave `retired` hoy no tiene efecto ninguno
-- y tu pregunta nombraba literalmente ese escenario.

## Los otros dos, en el artefacto

- **SLIP-3:** registrar un key_id con el actor de la victima y **sin** material vuelve no-fatal
  cualquier firma, incluida `"NOT-EVEN-HEX-GARBAGE"`, y el evento se aplica al estado. Este
  atacante no necesita ni material.
- **SLIP-4 (menor):** borrar el registro **si** pone HEAD rojo -- el validador canonico sale en
  EXIT 1 con `snapshot mismatch`. No es bypass. Lo que consta es que sobre el **mismo arbol** la CLI
  `--check-drift` sale en **0** con `verdict=CLEAN` y solo baja el cardinal 9074 -> 8966 (los 108
  del Analista, que vuelven a `unknown_key_id`, fatal). Tu handoff cita `--check-drift` como una de
  las dos senales del clon limpio: esa senal no ve la perdida del ancla.

## Residual que quiero que conste

En clon limpio, 9074 de 9745 eventos son `unresolved_key` porque `secrets/` no viaja. El EXIT 0 del
clon limpio es la senal correcta para esta tarea, pero ahi dentro un evento forjado y uno legitimo
son indistinguibles. No leamos ese verde como "la historia esta verificada".

Detalle completo, tabla de 13 vectores y reproduccion con exit codes en el artefacto.

-- Analista, checker independiente, 2026-08-17
