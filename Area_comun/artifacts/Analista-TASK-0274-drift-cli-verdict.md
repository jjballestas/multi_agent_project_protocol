---
artifact_id: Analista-TASK-0274-drift-cli-verdict
task_id: TASK-0274
reviewer: Analista
type: review-verdict
verdict: CHANGE-REQUIRED
created_at: 2026-07-22
anchors:
  protocol_head: 04ea079
  code_blob_protocol_replay: d7bd4d3
  clean_clone_checkout: 6f2084f
  scope: "SIN PRODUCTO EN ALCANCE"
---

# Veredicto TASK-0274 -- el gate de drift que ahora si puede fallar (casi)

Voz: Analista (checker adversarial). Firma: Analista.

Hora local: 2026-07-22 13:30 (reloj del sistema, sin convertir).

## Resumen ejecutivo

CHANGE-REQUIRED con UN bloqueante acotado y de bajo esfuerzo. El gate en PRODUCCION es
real: el CLI ya no es vacuo, sale 0 solo con ledger limpio y distinto de cero ante deriva
fabricada, ante flag desconocido y ante la ausencia de `--check-drift`. Los seis vectores
de aceptacion PASAN por comportamiento. El bloqueo NO es el comportamiento de hoy: es que la
PRUEBA PERMANENTE del vector 3 (flag desconocido) esta CONFUNDIDA y NO enrojece al revertir
la estrictez de argparse (mutante C queda verde). Es exactamente el anti-patron que esta
unidad existe para erradicar -- un negativo que no puede fallar -- reproducido una capa mas
abajo, en el test que blinda el gate. La pregunta de gating del Arquitecto ("cada uno de
esos negativos enrojece al revertir el arreglo?") tiene respuesta NO para el negativo del
flag desconocido, luego no puedo cerrar.

## Anclaje canonico

- HEAD del protocolo: 04ea079 (== origin/main). Validate del arbol vivo: exit 0.
- El blob de `runtime/protocol_replay.py` es byte-identico en 2aa5552, 6f2084f y 04ea079
  (d7bd4d3c...); el de la suite permanente es identico en 2aa5552 y 04ea079 (329ce79...).
- Clon limpio del protocolo a `/d/ccv0274`, checkout de la entrega 6f2084f. Todas las
  puertas se corrieron ALLI, no en el arbol caliente.
- Sin producto en alcance (respetado).

## Reproduccion (clon limpio 6f2084f, exit codes)

Puertas protocolares:

| Puerta | Comando | Exit |
|---|---|---|
| Suite replay | python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py | 0 (9/9) |
| Validate | python scripts/validate_collaboration_state.py | 0 |
| Encoding | python scripts/scan_encoding.py | 0 |
| Neutralidad | python scripts/scan_domain_neutrality.py | 0 |

Comportamiento del CLI (probado por payload, no por nombre de test):

| Caso | Comando | Exit | Salida |
|---|---|---|---|
| Ledger limpio | protocol_replay.py --check-drift --root /d/ccv0274 | 0 | verdict=CLEAN up_to_seq=5696 |
| Deriva fabricada | (status mutado en hot TASK_INDEX.json) --check-drift | 1 | verdict=DRIFT up_to_seq=5696; DRIFT path=...TASK_INDEX.json |
| Restaurado | (git checkout del hot file) --check-drift | 0 | verdict=CLEAN |
| Flag desconocido | protocol_replay.py --bogus-flag | 2 | argparse: unrecognized arguments |
| Sin flag | protocol_replay.py | 2 | argparse: --check-drift is required |
| Requerido + basura | protocol_replay.py --check-drift --bogus-flag | 2 | argparse: unrecognized arguments |
| Requerido mal escrito | protocol_replay.py --check-drfit | 2 | argparse: unrecognized arguments |

## Vector por vector

| # | Criterio | Resultado | Evidencia |
|---|---|---|---|
| 1 | exit 0 SOLO con ledger limpio | PASS | limpio exit 0 / deriva exit 1; `_drift_exit_code` es fail-closed (`1 if has_drift is not False else 0`): None o clave ausente -> 1 |
| 2 | deriva fabricada -> rojo | PASS | exit 1, verdict=DRIFT, reporta el path derivado; restaurar -> exit 0 |
| 3 | flag desconocido -> rojo | PASS en produccion / SLIP en el test permanente | --bogus-flag exit 2, combo exit 2, mal-escrito exit 2; PERO el negativo permanente NO enrojece al revertir la estrictez (ver bloqueante) |
| 4 | up_to_seq citable | PASS | "up_to_seq=5696" impreso en cada corrida |
| 5 | doc viva barrida | PASS | README runtime, HANDOFF_TEMPLATE y RUNBOOK_ONBOARDING_REMOTO citan el contrato de exit-code real ("un argumento desconocido nunca cuenta como verde"); los veredictos historicos son registros inmutables, varios ya anotan honestamente que el comando ERA vacuo |
| 6 | instancia generada hereda el gate | PASS | instancia runtime generada por new_instance.py: `runtime/protocol_replay.py` presente, --bogus-flag exit 2, `__main__`/`_drift_exit_code` reales (no el modulo vacuo). copy_runtime_dir copytree del runtime/ completo; el ignore solo excluye __pycache__ y state/runs |

## Disciplina de mutantes (cada negativo debe enrojecer al revertir SU arreglo)

Base pre-fix (blob 2aa5552~1, el modulo sin CLI): `--bogus-flag` exit 0 y `--check-drift`
exit 0. Confirma la vacuidad original: cualquier flag fabricaba un verde.

Mutantes sobre PRODUCCION, re-corriendo la suite permanente:

| Mutante | Cambio | Suite | Veredicto |
|---|---|---|---|
| A | `_drift_exit_code` -> `return 0` (gate vacuo restaurado) | exit 1 (RED) | TIENE DIENTES: el negativo de deriva enrojece |
| B | `_drift_exit_code` -> veredicto invertido | exit 1 (RED) | TIENE DIENTES: el positivo/veredicto enrojece |
| C | `parse_args` -> `parse_known_args` (acepta flags desconocidos) | exit 0 (GREEN) | SIN DIENTES: el negativo de flag desconocido NO enrojece |

## Bloqueante F-0274-01 (unico): el negativo de flag desconocido esta confundido

En `case_cli_is_a_real_aborting_gate`, la asercion del flag desconocido corre
`protocol_replay.py --bogus-flag` SIN `--check-drift`, y solo exige exit != 0. Bajo
`parse_known_args`, `--bogus-flag` se ignora y, al faltar `--check-drift`, dispara
`parser.error("--check-drift is required")` -> exit 2 -> la asercion `!= 0` PASA igual. El
test satisface su asercion por el guardia de "flag requerido", NO por el rechazo del flag
desconocido; confunde dos modos de fallo y por eso NO puede fallar si se afloja la estrictez
de argparse (mutante C queda verde). Falsable y reproducido: MutC deja la suite en exit 0.

Esto es el mismo error una capa mas arriba que TASK-0274 corrige: un gate cuyo test no puede
fallar. El comportamiento de produccion HOY es correcto (argparse estricto por defecto), pero
el blindaje permanente del criterio 3 es tan vacuo como lo era el comando original frente a
una regresion dirigida.

Aclaracion de alcance: reventar el fix COMPLETO (borrar `main()`/`__main__`) SI enrojece la
suite (con el modulo vacuo `--bogus-flag` -> exit 0 -> asercion `!= 0` falla). El hueco es
especifico del aflojamiento de la estrictez con el guardia de flag requerido intacto.

### Fix esperado (acotado)

Anadir a `case_cli_is_a_real_aborting_gate` una corrida que AISLE el rechazo del flag
desconocido: `protocol_replay.py --check-drift --bogus-flag` (o el mal-escrito
`--check-drfit`) con `assert returncode != 0`. Asi el negativo enrojece bajo
`parse_known_args`. Cambio de una linea de test, sin tocar produccion ni semantica.

### Bucle de fix declarado

- Remediacion: Codex (maker). Analista re-juzga (checker).
- Puertas afectadas por el re-juicio: la suite replay (debe pasar 10/10 o el conteo nuevo)
  MAS la verificacion de que MutC ahora deja la suite en ROJO; validate, encoding y
  neutralidad exit 0.
- Maximo 2 iteraciones antes de escalar al operador humano.

## Residuales declarados (no bloqueantes)

- R1: El bloque "mutation control" inline del test que usa el lambda local `inverted` es
  decorativo -- verifica propiedades de un lambda definido en el propio test, no de
  produccion; no puede fallar pase lo que pase en el codigo. Las aserciones sobre el
  `_drift_exit_code` real de produccion (mismo bloque) SI valen y quedaron probadas por A/B.
- R2: `--root` por defecto es `Path.cwd()`; correrlo desde un directorio que no sea la raiz
  de la instancia calcularia deriva sobre cwd. Cuestion de uso, no de correccion; fuera de
  alcance (no se cambio semantica).
- R3: En una instancia coordination-tier (event_state deshabilitado) el CLI sigue
  computando deriva real via replay; con ledger vacio da CLEAN/exit 0. No es falso verde: no
  hay eventos contra los que derivar, y la doc viva acota el gate a instancias
  runtime-authoritative. Observacion, fuera de alcance (semantica intacta).

## Recomendacion de cierre

CHANGE-REQUIRED. El deliverable de produccion es correcto y valioso -- NO es la vuelta del
gate vacuo -- pero no puedo responder "si" a la pregunta de gating del Arquitecto mientras
uno de los tres negativos no enrojezca al revertir su arreglo. Fix de una linea de test;
re-juicio con el mutante C como criterio de dientes.

-- Analista
