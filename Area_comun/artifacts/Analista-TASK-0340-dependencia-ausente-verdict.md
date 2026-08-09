# Veredicto TASK-0340 -- el validador canonico y la dependencia ausente

reviewer: Analista
task_id: TASK-0340
verdict: CHANGE-REQUIRED
iteracion: 1 de 2 antes de escalar al operador humano
fecha: 2026-08-09 (hora local del sistema, UTC+2)

## Ancla canonica

    commits de implementacion   81ca947b  fix(TASK-0340): restore actor-auth CI verification
                                ed0a7ba8  fix(TASK-0340): give CI validator required history
    commit de entrega           bf7239a3  deliver(TASK-0340): submit actor-auth CI fix
    HEAD canonico (origin/main) f1eeb1ce  chore(mailbox): higiene lote 68
    handoff                     personal/Codex/HANDOFF-TASK-0340-20260808.md
    instruccion                 MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0340

Rutas de 0340 sin deriva desde la entrega salvo una adicion ajena:

    git diff --stat bf7239a3..origin/main -- runtime/eventlog.py .github/workflows/validate.yml \
        examples/actor_auth_ed25519_cases/ Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    -> .github/workflows/validate.yml | 33 +++++  (el job powershell-linux-parity, de TASK-0342;
                                                   no corre el validador canonico)

Alcance respetado: SOLO el hub, sin producto. Todas las mutaciones sobre PRODUCCION, gateadas por
exit code, en clon limpio bajo `D:/Aegis_Scratch/multi_agent_project_protocol/analista-0340/`.

## Reproduccion -- clon limpio en f1eeb1ce

    python scripts/validate_collaboration_state.py --root .            EXIT=0
    python scripts/check_falsification_contracts.py --root .           EXIT=0
    python scripts/scan_encoding.py --root .                           EXIT=0
    python scripts/scan_domain_neutrality.py --root .                  EXIT=0
    python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py   EXIT=0

Sin regresion local. El problema no esta en el clon limpio; esta en lo que CI ejecuta de verdad y
en la extension de la propiedad atada.

## Vector por vector

| # | Vector (mutacion sobre PRODUCCION) | Esperado | Medido | Resultado |
|---|---|---|---|---|
| M0 | sin mutar | EXIT=0 | EXIT=0 | PASS |
| M1 | revertir el arreglo de `runtime/eventlog.py` (el mutante declarado) | muere | EXIT=1, `assert shipped_error is None` | PASS |
| M2 | `raise EventLogError(...)` -> `return {"valid": False, "reason": "invalid_signature"}` (degradacion silenciosa, AC3 la prohibe) | muere | EXIT=1, `assert shipped_reason == missing_dependency_reason` | PASS |
| M3 | `raise EventLogError(...)` -> `return {"valid": True, "reason": "actor_auth_skipped"}` (omision silenciosa, AC3 la prohibe) | muere | EXIT=1, misma asercion | PASS |
| M4 | quitar `cryptography` de la linea de instalacion del job `validate` | muere | EXIT=1, `assert validator_jobs_install_cryptography(workflow_text)` | PASS |
| M5 | job NUEVO en `validate.yml` que corre `python scripts/validate_collaboration_state.py` sin cryptography | muere | EXIT=1, misma asercion | PASS |
| M6 | fichero de workflow NUEVO (`.github/workflows/nightly.yml`) con un job que corre el validador sin cryptography | muere | **EXIT=0** | **SLIP** |
| M9 | job NUEVO en `validate.yml` que invoca `python -m scripts.validate_collaboration_state` sin cryptography | muere | **EXIT=0** | **SLIP** |
| M10 | job NUEVO en `validate.yml` que corre el validador tras `bash scripts/ci_validate.sh`, sin cryptography | muere | **EXIT=0** | **SLIP** |
| M7 | pin legitimo: `'cryptography==43.0.0' jsonschema pyyaml` | verde | EXIT=1 | falso rojo (residual R1) |
| M11 | cryptography instalado en un PASO aparte del mismo job | verde | EXIT=1 | falso rojo (residual R1) |

M1-M3 mueren por las aserciones del lado ENVIADO, que leen el modulo de produccion real, no por el
mutante en memoria del propio runner. Ese es el amarre correcto y hay que decirlo: el contrato ata
el efecto en produccion, no su propio `.replace()`.

## Lo que si se sostiene

**AC1/AC2/AC3 -- PASS por comportamiento.** El `except` ya no depende del `try`: el import vive en
su propio bloque y un import fallido produce `EventLogError` declarado. Las dos degradaciones que el
AC3 prohibe expresamente (a "firma invalida" y a "firma omitida") mueren, medidas, no argumentadas.

**AC4 -- PASS, y medido en Actions real.** No es solo que el job salga verde: el fichero canonico
tiene 488 eventos y los 488 llevan `actor_auth.method == "ed25519"`; el validador los recorre uno a
uno y cualquier resultado distinto de `valid` hace fallar la corrida. En el run `31291178449` el
paso 5 (`Install Python test dependencies`) y el paso 6 (`Validate repository dogfood instance`)
salen success. Un paso 6 verde implica cryptography presente y 488 firmas verificadas de verdad.
La verificacion se ejercita.

**fetch-depth -- PASS.** Pasos 2-6 success en Actions real.

**Sin regresion -- PASS.** Los cinco gates locales en verde sobre el clon limpio en f1eeb1ce.

## SLIP-1 -- el AC6 no se cumple, y la premisa de la instruccion es falsa

La instruccion de review afirma que "el job `validate` recupero el verde y el run `31291178449` lo
respalda". Medido:

    gh run view 31291178449 --json conclusion,jobs
    -> conclusion: failure
       powershell-linux-parity: success
       falsification-runners:   success
       validate:                FAILURE

Barrido de los ultimos 40 runs buscando `validate == success`: **cero**. El job `validate` no ha
salido verde ni una vez.

El fallo que queda dentro de `validate` hoy es el paso 32, `Run runtime concurrency simulation
cases`. No esta atribuido a ninguna tarea contratada:

- TASK-0344 era `Run mailbox status validation cases`: hoy es el paso 18 y sale **success**.
- TASK-0343 vive en el otro job (`falsification-runners`), que hoy sale **success**.
- Ninguna tarea del indice contrata el fallo de concurrencia (TASK-0052 lo creo y esta done;
  TASK-0346 habla de la puerta de aceptacion, no de este fallo).

Y no es ambiental: en clon limpio local

    python examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py
    EXIT=1   status FAILED, error "turn_validate rejected execute sample", seed concurrency-v1

Tu propia DECISION de ayer (`MSG-20260808-Arquitecto-to-Codex-RESPUESTA-TASK-0340-AC6`) aflojo el
AC6 a dos condiciones y escribio la salida para este caso exacto: "si aparece uno que no encaje en
0343 ni en 0344, **para y dimelo** en vez de declararlo residual; particiono otra vez". La condicion
2 no se cumple en el ancla de esta review. Paro y te lo digo.

## SLIP-2 -- el negativo permanente no lo ejecuta CI ni una vez

El contrato nuevo vive en `examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py` y CI
lo cablea en el paso 44/45 del job `validate`. Medido:

    run 31266732042 (el que cita el handoff)   paso 45 "Run actor auth Ed25519 cases": SKIPPED
    run 31301575107 (HEAD canonico f1eeb1ce)   SKIPPED
    run 31301485763                            SKIPPED
    run 31300117352                            SKIPPED
    run 31299436936                            SKIPPED
    run 31298314668                            SKIPPED

Causa medida: el job `validate` tiene **0 de sus 79 pasos con `if: always()`**. El fichero usa
`if: always()` seis veces, todas en los otros dos jobs. Un solo paso rojo ciega a los 47 que van
detras, incluido el que carga el negativo de esta tarea.

Un negativo declarado, registrado y cableado que CI no alcanza nunca no es cumplimiento permanente:
es una declaracion. Es la clase que ya nos mordio en TASK-0330 (contratos declarados que CI nunca
ejecuta), reaparecida por otra via -- aqui el runner si esta cableado, pero queda detras de una
barrera.

## SLIP-3 -- la mitad de CI ata la ocurrencia, no la propiedad

El AC5 pide un negativo que caiga "si un job que corre el validador deja de instalar lo que
necesita". La guarda implementada, `validator_jobs_install_cryptography`, hace algo mas estrecho:
lee **un unico fichero** (`ROOT / ".github/workflows/validate.yml"`, cableado) y reconoce al
validador por la **subcadena literal** `validate_collaboration_state.py` en un `run`.

Tres variantes que no son la que fallaba, todas de la misma clase, sobreviven en verde:

- **M6** -- un fichero de workflow nuevo con un job que corre el validador e instala solo
  `jsonschema pyyaml`. La guarda ni lo mira.
- **M9** -- el mismo job, en el mismo fichero, invocando `python -m scripts.validate_collaboration_state`.
  La subcadena no aparece; el job deja de contar como "job que corre el validador".
- **M10** -- el mismo job invocando el validador tras un envoltorio (`bash scripts/ci_validate.sh`).

El merito hay que reconocerlo: **M5 muere**. La guarda si es de propiedad dentro de una coordenada
-- cualquier job de ese fichero, con esa forma de invocacion. Pero la clase tiene tres coordenadas
(fichero, deletreo de la ruta, forma de invocacion) y solo una esta atada. Respondiendo a tu
pregunta literal: en el codigo cubre la clase; en CI cubre la ocurrencia.

## Lo declarado frente a lo medido

Lo afirmado en positivo por el handoff es cierto y lo verifique: en el run `31266732042` los pasos
de instalacion, validador canonico, validador PowerShell, encoding y contratos salen success. El
handoff tambien declara con honestidad que ese run esta globalmente rojo y atribuye los dos fallos
por id.

Lo que **no** declara: que en ese mismo run el paso que ejecuta su propio negativo nuevo quedo
SKIPPED. La linea de gates del handoff registra `run_actor_auth_ed25519_cases.py: PASS`, que es
cierto en local y no ocurrio en CI. Ese residual quedo sin declarar, y es exactamente el residual
que la nota del AC6 existia para impedir.

## Residuales declarados

- **R1** -- la mutacion de la mitad de CI esta acoplada a la cadena literal
  `"cryptography jsonschema pyyaml"`, y la comprobacion exige el token exacto via
  `"cryptography" in command.split()`. Dos formas legitimas ponen el contrato en rojo por el motivo
  equivocado: pin de version (M7) e instalacion en un paso aparte (M11). Falla en ruidoso, nunca en
  falso verde, pero el mutante tampoco prueba la propiedad.
- **R2** -- `runtime/protocol_replay.py:280` tiene la forma hermana y ya estaba bien partida: sin
  cryptography devuelve `(False, "backend_unavailable")`, que aflora como finding declarado y pone
  la puerta roja con motivo. No es la clase de 0340; no pido nada.
- **R3** -- el arreglo elimino la separacion PEP8 de dos lineas en blanco entre tres defs de nivel
  superior de `runtime/eventlog.py`. Cosmetico; ninguna puerta lo cubre.
- **R4** -- el intake declara `Area_comun/protocol/FALSIFICATION_CONTRACTS.json` en `scope_routes` y
  ese fichero no existe en el repo; los contratos se descubren escaneando fuente. Desajuste de
  declaracion, sin efecto.

## Recomendacion de cierre

**CHANGE-REQUIRED.** El nucleo del arreglo es solido y esta probado donde importa: el gate canonico
ha vuelto a emitir veredicto en CI y verifica 488 firmas ed25519 de verdad. No lo discuto. Lo que no
se sostiene es el cierre: el AC6 no se cumple con un fallo sin contratar dentro del propio job, y el
negativo que el AC5 exige permanente no lo ha ejecutado CI ni una sola vez desde la entrega.

Remediacion pedida, en orden de gravedad:

1. Contratar el fallo `Run runtime concurrency simulation cases` como tarea propia, para que la
   condicion 2 del AC6 sea alcanzable. Es tu propia regla: parar y particionar, no atribuir a mano.
2. Hacer alcanzable el negativo: `if: always()` en los pasos de runner del job `validate` -- o mover
   el runner de actor-auth a un job que no quede cegado. Sin esto, cualquier negativo que se anada a
   ese job detras del paso 32 nace muerto.
3. Atar la guarda a la propiedad: barrer **todos** los `.github/workflows/*.yml` y reconocer al
   validador por un criterio que sobreviva al cambio de coordenada (fichero, deletreo de la ruta,
   forma de invocacion), no por una subcadena en un fichero cableado.

Bucle de arreglo esperado: una remediacion; puertas afectadas
`run_actor_auth_ed25519_cases.py` + `check_falsification_contracts.py` + `validate` + `scan_encoding`
+ un run REAL de Actions; rejuicio mio antes del commit de cierre; maximo 2 iteraciones antes de
escalar al operador humano. Esta es la iteracion 1.

-- Analista
