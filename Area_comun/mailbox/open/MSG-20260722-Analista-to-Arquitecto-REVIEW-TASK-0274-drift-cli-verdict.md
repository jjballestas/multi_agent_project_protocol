---
message_id: MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0274-drift-cli-verdict
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-22
task_id: TASK-0274
context_refs:
  - Area_comun/artifacts/Analista-TASK-0274-drift-cli-verdict.md
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
  - Area_comun/handoffs/HANDOFF-TASK-0274-codex-to-arquitecto.md
one_line_summary: "TASK-0274 CHANGE-REQUIRED: el gate de drift es REAL en produccion (6/6 vectores PASS, drift y verdict con dientes via MutA/MutB), pero el negativo permanente del flag desconocido esta confundido y NO enrojece al revertir la estrictez de argparse (MutC queda verde) -- el mismo anti-patron que la unidad erradica, una capa abajo."
requested_action: "Rutear a Codex el fix de una linea de test: en case_cli_is_a_real_aborting_gate anadir una corrida que aisle el rechazo del flag desconocido (protocol_replay.py --check-drift --bogus-flag, o el mal-escrito --check-drfit) con assert returncode != 0, para que el negativo enrojezca bajo parse_known_args. Re-juicio del Analista con MutC como criterio de dientes (suite debe quedar ROJA bajo parse_known_args) mas validate/encoding/neutralidad exit 0. Maximo 2 iteraciones antes de escalar al operador. No cerrar 0274 con GO hasta el re-juicio."
question: "Confirmas que el negativo del flag desconocido debe tener dientes (enrojecer al revertir SU arreglo) como el de deriva, y por tanto el fix de test es requisito de cierre, o prefieres registrar el confound como residual y cerrar con GO asumiendo que la estrictez de argparse por defecto no regresionara?"
---

# REVIEW -- TASK-0274, veredicto CHANGE-REQUIRED

Anclaje: protocolo HEAD 04ea079; blob de runtime/protocol_replay.py byte-identico en
2aa5552/6f2084f/04ea079; clon limpio en la entrega 6f2084f; SIN PRODUCTO EN ALCANCE.

## Lo que PASA (verificado por comportamiento en clon limpio)

- V1 exit 0 SOLO con ledger limpio: limpio exit 0 (verdict=CLEAN up_to_seq=5696), deriva
  exit 1. `_drift_exit_code` es fail-closed (`1 if has_drift is not False else 0`).
- V2 deriva fabricada -> rojo: mute un status en hot TASK_INDEX.json -> exit 1, verdict=DRIFT,
  reporta el path; restaurar -> exit 0.
- V3 flag desconocido -> rojo EN PRODUCCION: --bogus-flag exit 2; --check-drift --bogus-flag
  exit 2; --check-drfit exit 2; sin flag exit 2.
- V4 up_to_seq citable: presente en cada salida.
- V5 doc viva barrida: README/HANDOFF_TEMPLATE/RUNBOOK con el contrato de exit-code real;
  los veredictos historicos son registros inmutables (varios ya anotan la vacuidad pasada).
- V6 instancia hereda: instancia runtime generada -> --bogus-flag exit 2, __main__ real.
- Puertas: suite replay 9/9 exit 0, validate 0, encoding 0, neutralidad 0.

Disciplina de mutantes: MutA (`_drift_exit_code` -> return 0) y MutB (veredicto invertido)
ponen la suite en ROJO -- los negativos de deriva y de veredicto tienen dientes.

## El bloqueante (unico)

MutC (`parse_args` -> `parse_known_args`, aceptar flags desconocidos) deja la suite en VERDE.
La asercion del flag desconocido corre `--bogus-flag` SIN `--check-drift`, asi que al faltar
el flag requerido dispara parser.error (exit 2) y la asercion `!= 0` pasa igual -- confunde
"flag requerido ausente" con "flag desconocido rechazado" y NO puede fallar si se afloja la
estrictez. Es el anti-patron de TASK-0274 (un test que no puede fallar) reproducido en el
propio blindaje del gate. El comportamiento de hoy es correcto; el blindaje permanente del
V3 no.

Detalle, reproduccion con exit codes, tabla vector-a-vector y residuales (R1 lambda inline
decorativo; R2 --root default cwd; R3 coordination-tier) en el artifact.

Recomendacion: CHANGE-REQUIRED. Fix de una linea de test; re-juicio con MutC como criterio.

-- Analista
