# Veredicto adversarial -- TASK-0279 (gate de trailers en commit-msg)

- Reviewer: Analista (voz independiente / checker)
- Fecha local: 2026-07-22
- Unidad: TASK-0279 -- el gate de trailers ABORTA en `.githooks/commit-msg` en vez de un
  validador post-hoc que solo enrojece al peer siguiente.
- Recomendacion de cierre: **OK-CLOSABLE (GO)**.

## Ancla canonica

- Commit citado por la instruccion: `15fe9c8` (feat), entrega `56f9750`.
- HEAD canonico al juzgar: `77a15b1`.
- Verifique que el codigo bajo prueba es **identico byte-a-byte** desde `15fe9c8` hasta HEAD:
  `git log 15fe9c8..HEAD -- scripts/check_commit_trailers.py scripts/test_commit_msg_hook.py .githooks/commit-msg .githooks/pre-commit` = vacio.
  Los unicos cambios `56f9750..HEAD` son mailbox + ledger de ruteo, no tocan el gate.
- Toda la reproduccion corre sobre un **clon limpio** en `D:/ccv` (checkout `77a15b1`),
  gateado por exit code. Un arbol caliente miente; no juzgue in-place.

## Reproduccion (exit codes)

Gates de protocolo en el clon limpio:

- `python scripts/validate_collaboration_state.py` -> exit 0 (OK)
- `python scripts/scan_encoding.py` -> exit 0 (OK)
- `python scripts/scan_domain_neutrality.py` -> exit 0
- `python runtime/protocol_replay.py` -> exit 0 ; `event_state` = enabled/materialize/enforce/authoritative True; drift 0
- Suite entregada `python scripts/test_commit_msg_hook.py` -> exit 0 (7 casos de commit real)

## Analisis diferencial (la propiedad que importa)

El objeto de la unidad no es "un checker nuevo": es que el commit-msg gate rechace
**exactamente lo que el validador post-hoc rechazaria**, para abortar en el instante del
commit lo que si no enrojeceria al peer despues. Compare linea a linea
`scripts/check_commit_trailers.py` (gate) contra `validate_commit_trailers` en
`scripts/validate_collaboration_state.py` (post-hoc):

- Mismo conjunto gobernado: `Area_comun/`, `runtime/`, `scripts/`, `protocol.config.json`.
- Mismos patrones `Task-Id` / `Fixes-Task` / `Ops-Reason (<=120)` / subject `fix|revert|hotfix`.
- Misma logica de bloque final unico y "known" = TASK_INDEX + TASK_INDEX_ARCHIVE.

Busque el sentido peligroso (gate mas LAXO que el validador -> pasa el commit pero enrojece
al peer): **no existe**. Las tres divergencias que hay son todas del gate mas ESTRICTO que el
validador (clave de trailer que debe empezar por letra; exactamente un `Ops-Reason`/`Task-Id`;
manejo de linea de espacios), es decir a lo sumo falsos positivos sobre entradas patologicas
que `git commit -m` no produce. Ningun commit que el gate acepta puede enrojecer al validador
despues. La promesa central se sostiene.

## Tabla vector por vector (por COMPORTAMIENTO, commits reales)

| # | Vector | Resultado esperado | Observado | Veredicto |
|---|--------|--------------------|-----------|-----------|
| 1e | commit valido | ACEPTA | exit 0 | PASS |
| 1a | linea en blanco en bloque final (Task-Id / blank / Co-Authored-By) | ABORTA | exit 1, "missing exact final trailer" | PASS |
| 1b | Ops-Reason 121 chars (>120) | ABORTA | exit 1 | PASS |
| 1b' | Ops-Reason 120 chars (frontera) | ACEPTA | exit 0 | PASS |
| 1c | ausencia de Task-Id (coordinacion) | ABORTA | exit 1 | PASS |
| 1c' | Task-Id: none sin Ops-Reason | ABORTA | exit 1 | PASS |
| 1d | fix/revert/hotfix x (`(`, `:`, `!`) sin Fixes-Task (9 combinaciones) | ABORTA | exit 1 en las 9 | PASS |
| 1d' | fix: con Fixes-Task valido | ACEPTA | exit 0 | PASS |
| 1d'' | fix: con Fixes-Task inexistente | ABORTA | exit 1 | PASS |
| 2a | Task-Id en TASK_INDEX_ARCHIVE (podada real: TASK-0001) | ACEPTA | exit 0 | PASS |
| 2b | Task-Id inexistente (TASK-9999) | ABORTA | exit 1 | PASS |
| 3 | cada negativo enrojece al revertir su arreglo | suite ROJA | ver mutantes abajo | PASS |
| 4a | ruta no gobernada (personal/, examples/, .githooks/) sin trailer | ACEPTA (no-op) | exit 0 | PASS |
| 4b | scripts/ tocado sin trailer | ABORTA | exit 1 | PASS |
| 4c | coste por invocacion | imperceptible | mediana ~0.054 s | PASS |
| 5 | escape E3 documentado y operativo | disarm/rearm funciona | ver abajo | PASS |

Detalle mutantes (criterio 3, doble prueba):

- Prueba directa (guarda load-bearing): baseline rechaza los 5 negativos; al desactivar cada
  guarda, EXACTAMENTE su negativo asociado se voltea a ACEPTADO y los demas siguen rojos.
  guard1(bloque final) -> voltea blank-line + missing-Task-Id; ops-length -> voltea long-Ops;
  unknown-task -> voltea unknown; fix-subject -> voltea fix-sin-Fixes.
- Prueba literal (la suite entregada enrojece): con el checker mutado, `test_commit_msg_hook.py`
  pasa de exit 0 a exit 1 (AssertionError) para cada una de las cuatro mutaciones. La suite no
  es verde vacio.

Escape E3: `git config --unset core.hooksPath` deja pasar un commit de trailer malo (exit 0);
`git config core.hooksPath .githooks` rearma (exit 1). El checker imprime el disarm/rearm en
cada rechazo. Documentado tambien en la tarea.

## Deuda de fixture PREEXISTENTE (confirmada, NO contra 0279)

El maker declaro que el runner de instanciacion completa ya estaba rojo. Lo confirme por mi
cuenta: `examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` falla (exit 1)
en HEAD en dos casos (`case_coordination_default_and_flag`, `case_runtime_tier_scaffolds_motor_gates_ci_off`
con `ModuleNotFoundError: No module named 'ledger_head'` en el `prune_state.py` escafoldado).
Corri el MISMO runner en el commit padre `6197e10` (sin codigo de 0279): falla en los MISMOS
dos casos. Por tanto la deuda es PREEXISTENTE y no la introduce 0279; 0279 solo agrega dos
entradas al set GATE_SCRIPTS sin regresionar el runner. No la cuento contra esta unidad. Si el
Arquitecto quiere, merece unidad propia (fix del import de `ledger_head` en la instancia
escafoldada runtime-tier).

## Export born-operational

- `scripts/new_instance.py`: `check_commit_trailers.py` en `GATE_SCRIPT_FILES`; `.githooks`
  (ambos hooks) en `COPIED_DIRS`. El pin sha256 de `.githooks/pre-commit` en el CI coincide con
  el archivo actual (0279 no toco pre-commit; su ultimo cambio fue TASK-0273). Espejo correcto.

## Residuales declarados (no bloquean)

- R1: la regla "sin linea en blanco" se aplica solo DENTRO del bloque final. Una linea en blanco
  ARRIBA del bloque final (Co-Authored-By en un parrafo anterior, Task-Id solo como bloque final)
  la aceptan gate Y validador por igual (probado). No reintroduce bloqueo del peer porque no hay
  divergencia; se anota como forma del contrato existente, no como defecto de 0279.
- R2: `.githooks/` y `examples/` no son "gobernadas" para trailers (coincide con
  `GOVERNED_TRAILER_PATHS` del validador). Editar solo un hook o un ejemplo pasa sin trailer.
  Consistente con el validador; fuera del alcance de 0279 (mueve DONDE, no QUE rutas).
- R3: el gate es mas estricto que el validador en clave-de-trailer con-letra-inicial, un-solo
  Ops-Reason/Task-Id, y linea de espacios. Todo en el sentido seguro (nunca mas laxo). Solo
  patologico; `git commit -m` no lo dispara.
- R4: `test_commit_msg_hook.py` no viaja en el export (como ningun otro test suite; solo viajan
  gates + hooks). La instancia nueva nace con el gate VIVO pero no con esta suite de dev.

## Cierre

TASK-0279 hace exactamente lo que promete y es un espejo fiel -- ligeramente mas estricto -- del
validador post-hoc, por lo que no puede dejar pasar un commit que enrojezca al peer despues, que
es la razon entera por la que existe la unidad. **OK-CLOSABLE (GO).**

-- Analista
