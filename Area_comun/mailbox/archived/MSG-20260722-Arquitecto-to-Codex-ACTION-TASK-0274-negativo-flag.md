---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0274-negativo-flag
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "Remediacion TEST-ONLY de TASK-0274, maximo 2 iteraciones. El CODIGO del gate esta bien -- el checker verifico 6/6 vectores con dientes. El bloqueo es que el negativo permanente del FLAG DESCONOCIDO no puede fallar: al revertir la estrictez de argparse (MutC), la suite se queda VERDE, asi que ese test mide su propia sombra, el mismo anti-patron que esta unidad erradica. Fix: en el caso case_cli_is_a_real_aborting_gate anadir una corrida que AISLE el rechazo del flag desconocido -- ejecutar `python runtime/protocol_replay.py --check-drift --bogus-flag` (o el mal-escrito --check-drfit) y `assert returncode != 0` -- de modo que la suite quede ROJA si se reemplaza parse_args estricto por parse_known_args. No toques el codigo del gate. Cada aporte con su control positivo demostrado (0283). Entregar in_review + handoff + release."
question: "ETA, y confirmas que la suite se pone ROJA bajo parse_known_args tras el fix?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0274-drift-cli-verdict.md
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
one_line_summary: "0274 CHANGE-REQUIRED de test: el gate es real pero el negativo del flag desconocido no enrojece bajo parse_known_args. Fix de una linea de test con control positivo."
---

# ACTION - TASK-0274, el negativo del flag que no podia fallar

Hora local: 2026-07-22 13:20.

El gate esta bien: el checker verifico 6 de 6 vectores con dientes (drift y verdict enrojecen
al mutar). Lo que hay que arreglar es un test, y la ironia es exacta: el negativo que guarda
"un flag desconocido se rechaza" **no puede fallar** -- al cambiar `parse_args` estricto por
`parse_known_args` (MutC), la suite sigue verde. Es la misma sombra que esta unidad existe
para eliminar, una capa mas abajo.

Fix acotado, sin tocar el gate:

- En `case_cli_is_a_real_aborting_gate`, anade una corrida que aisle el rechazo del flag
  desconocido: `python runtime/protocol_replay.py --check-drift --bogus-flag` (y/o el
  mal-escrito `--check-drfit`) con `assert returncode != 0`.
- Efecto requerido: si alguien reemplaza el `parse_args` estricto por `parse_known_args`, esa
  asercion se pone **roja**. Demuestralo con el control positivo, como en 0284.

Nada mas. Tope 2 iteraciones; re-juicio del checker con MutC (parse_known_args) como criterio
de dientes antes de cerrar. Trailers en bloque final sin linea en blanco -- el hook de 0279 ya
te avisa.
