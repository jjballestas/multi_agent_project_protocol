---
artifact_id: Analista-TASK-0274-flag-rejuicio-verdict
task_id: TASK-0274
reviewer: Analista
type: review-verdict
verdict: OK-CLOSABLE
created_at: 2026-07-22
anchors:
  protocol_head: 7decc08
  clean_clone_checkout: 0831701
  test_fix_commit: 77afe05
  code_blob_protocol_replay: d7bd4d3
  suite_blob: b996425
  scope: "SIN PRODUCTO EN ALCANCE"
---

# Veredicto TASK-0274 (re-juicio) -- el negativo del flag desconocido ya tiene dientes

Voz: Analista (checker adversarial). Firma: Analista.

Hora local: 2026-07-22 13:42 (reloj del sistema, sin convertir).

## Resumen ejecutivo

OK-CLOSABLE. Mi CHANGE-REQUIRED anterior tenia un unico bloqueante: la prueba permanente
del vector 3 (flag desconocido) NO enrojecia al aflojar la estrictez de argparse
(parse_known_args / MutC quedaba verde), porque la asercion corria `--bogus-flag` SIN
`--check-drift` y satisfacia su `!= 0` por el guardia de "flag requerido", no por el rechazo
del flag desconocido. La remediacion TEST-ONLY (commit 77afe05, entrega 0831701) anade en
`case_cli_is_a_real_aborting_gate` la corrida AISLADA que pedi -- `--check-drift --root <root>
--bogus-flag` con `assert returncode != 0` -- sin tocar produccion ni semantica. Reproducido
en clon limpio: MutC ahora deja la suite ROJA y el caso que falla es EXACTAMENTE
`case_cli_is_a_real_aborting_gate`, con el error igual a la salida CLEAN de la combinacion
aislada (prueba de que es esa asercion la que caza el mutante, no otra). La respuesta a la
pregunta de gating del Arquitecto es SI. Cierro con GO.

## Anclaje canonico

- HEAD del protocolo: 7decc08 (== origin/main). Validate del arbol vivo: exit 0.
- Clon limpio del protocolo a `/d/ccv0274b`, checkout de la entrega 0831701. Todas las
  puertas se corrieron ALLI, no en el arbol caliente.
- El blob de `runtime/protocol_replay.py` es byte-identico (d7bd4d3) en 04ea079/6f2084f/
  77afe05/0831701/7decc08: la remediacion es TEST-ONLY, produccion no cambio. Por eso los
  6/6 vectores que ya verifique por comportamiento en el juicio anterior siguen vigentes.
- El blob de la suite cambio de 329ce79 (antes) a b996425 (77afe05 en adelante), identico
  en 77afe05/0831701/7decc08. El diff es +3 lineas: la corrida aislada del flag desconocido.
- Sin producto en alcance (respetado).

## Reproduccion (clon limpio 0831701, exit codes)

Puertas protocolares:

| Puerta | Comando | Exit |
|---|---|---|
| Suite replay | python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py | 0 (9/9) |
| Validate | python scripts/validate_collaboration_state.py | 0 |
| Encoding | python scripts/scan_encoding.py | 0 |
| Neutralidad | python scripts/scan_domain_neutrality.py | 0 |

Comportamiento de produccion del vector aislado (probado por payload, no por nombre de test):

| Caso | Comando | Exit | Salida |
|---|---|---|---|
| Flag desconocido AISLADO | protocol_replay.py --check-drift --root /d/ccv0274b --bogus-flag | 2 | argparse: unrecognized arguments: --bogus-flag |
| Ledger limpio | protocol_replay.py --check-drift --root /d/ccv0274b | 0 | verdict=CLEAN up_to_seq=5714 |

La combinacion `--check-drift ... --bogus-flag` sale 2 por el RECHAZO del flag desconocido
(no por el guardia de flag requerido, que no puede disparar con --check-drift presente): la
asercion permanente ahora pasa por la razon correcta.

## Disciplina de mutantes (el criterio de cierre que declare)

Suite re-corrida sobre el clon limpio con cada mutante sobre PRODUCCION:

| Mutante | Cambio | Suite | Caso que falla | Veredicto |
|---|---|---|---|---|
| A | `_drift_exit_code` -> `return 0` (gate vacuo) | exit 1 (RED) | case_cli_is_a_real_aborting_gate | TIENE DIENTES |
| B | `_drift_exit_code` -> veredicto invertido | exit 1 (RED) | case_cli_is_a_real_aborting_gate | TIENE DIENTES |
| C | `parse_args` -> `parse_known_args` (acepta flags desconocidos) | exit 1 (RED) | case_cli_is_a_real_aborting_gate | AHORA TIENE DIENTES |

MutC, que en el juicio anterior quedaba VERDE, hoy enrojece: el error reportado por la suite
es `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=1`, es decir, la corrida aislada
`--check-drift --bogus-flag` bajo parse_known_args ignoro el flag, corrio el drift limpio,
salio 0 y la asercion `!= 0` fallo. Es la asercion nueva la que caza el mutante. Los tres
negativos del gate enrojecen ahora al revertir su arreglo.

## Vector por vector (re-juicio)

| # | Criterio | Resultado | Evidencia |
|---|---|---|---|
| 1 | exit 0 SOLO con ledger limpio | PASS (produccion sin cambio) | blob d7bd4d3 identico al ya verificado; suite 9/9 |
| 2 | deriva fabricada -> rojo | PASS (produccion sin cambio) | dirty run exit 1 verdict=DRIFT en la suite |
| 3 | flag desconocido -> rojo | PASS (produccion) + BLINDAJE CON DIENTES (test) | combo aislado exit 2 en produccion; MutC deja la suite ROJA -- SLIP anterior RESUELTO |
| 4 | up_to_seq citable | PASS | "up_to_seq=..." impreso en cada corrida |
| 5 | doc viva barrida | PASS (sin cambio) | README/HANDOFF_TEMPLATE/RUNBOOK con el contrato de exit-code real |
| 6 | instancia generada hereda el gate | PASS (sin cambio) | runtime/ copiado completo; ya verificado por comportamiento |

## Residuales declarados (no bloqueantes, arrastrados del juicio anterior)

- R1: El bloque "mutation control" inline (lineas 200-205) que usa el lambda local `inverted`
  sigue siendo decorativo -- verifica propiedades de un lambda del propio test, no de
  produccion; no puede fallar. Las aserciones sobre el `_drift_exit_code` REAL (mismo bloque)
  si valen y quedan cubiertas por MutA/MutB. Cosmetico, no bloquea.
- R2: `--root` por defecto es `Path.cwd()`; correrlo fuera de la raiz calcularia deriva sobre
  cwd. Cuestion de uso, no de correccion; fuera de alcance (semantica intacta).
- R3: En coordination-tier (event_state deshabilitado) con ledger vacio da CLEAN/exit 0; no
  es falso verde (no hay eventos contra que derivar) y la doc acota el gate a instancias
  runtime-authoritative. Observacion, fuera de alcance.

## Recomendacion de cierre

OK-CLOSABLE (GO). El deliverable de produccion ya era correcto y valioso; la remediacion
TEST-ONLY cierra el unico hueco -- el negativo del flag desconocido ahora enrojece al revertir
su arreglo, como los otros dos. La pregunta de gating tiene respuesta SI. El Arquitecto puede
flipar TASK-0274 a done y liberar la claim (accion de cierre que corresponde al orquestador,
no al checker).

-- Analista
