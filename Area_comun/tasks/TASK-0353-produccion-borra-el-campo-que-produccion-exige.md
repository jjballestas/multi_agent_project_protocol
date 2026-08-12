---
id: TASK-0353
title: Produccion borra el campo que produccion exige -- schema_report elimina obstacles justo antes de validate_turn
status: in_review
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
created: 2026-08-10
intake:
  type: fix
  goal: >
    Hallado por Codex al ejecutar TASK-0347 y confirmado por comportamiento: `TURN_SCHEMA_KEYS` de
    `runtime/orchestrator.py` NO contiene `obstacles`, y `schema_report()` filtra el turno por esa
    lista **justo antes** de `validate_turn()`. Consecuencia: un productor que entrega
    `obstacles: []` -- lo que la regla de TASK-0259 exige -- ve su campo BORRADO por el propio
    pipeline y el turno rechazado con el diagnostico de campo ausente, mientras la entrada del
    runlog demuestra que el informe original si lo traia. En la ruta enrutada por el orquestador la
    regla es **INSATISFACIBLE**: produccion exige un campo que produccion elimina. Afecta al vivo y
    al `orchestrator.py` embarcado que cada instancia nueva copia.
  acceptance:
    - "AC1 (falsacion previa por comportamiento): se reproduce que un informe con `obstacles: []` pierde el campo al pasar por `schema_report()` y que el turno resultante es rechazado por la regla, citando la entrada de runlog que prueba que el productor si lo entrego. Evidencia por ejecucion, no por lectura del codigo."
    - "AC2 (la ruta enrutada deja de ser insatisfacible): tras el cambio, un productor que entrega el campo obligatorio lo conserva hasta la validacion y el turno se acepta. Se acredita ejecutando la ruta del orquestador, no solo la llamada directa."
    - "AC3 (el gemelo embarcado): el mismo arreglo llega al `orchestrator.py` que `new_instance.py` copia a cada instancia nueva. Una instancia recien creada no puede nacer con la regla insatisfacible. Se acredita instanciando y ejecutando, no comparando ficheros."
    - "AC4 (la clase, no el campo): `obstacles` es UN campo; el defecto es que una lista de claves permitidas y una regla de validacion evolucionan por separado. Se declara el criterio que impide la proxima divergencia -- que ningun campo exigido por la validacion pueda faltar en la lista de claves -- y se ata por PROPIEDAD, no enumerando campos."
    - "AC5 (negativo permanente, verificado por mutacion): contrato que muera si un campo exigido por la validacion vuelve a quedar fuera del filtro de esquema. Se verifica matando un mutante de PRODUCCION."
    - "AC6 (sin regresion): el replicador del job `validate` no empeora; se declara el saldo PASS/FAIL antes y despues."
  verification_cmd:
    - "python scripts/replay_validate_job.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - runtime/orchestrator.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "Las fixtures de los runners que NO pasan por el orquestador: son TASK-0347."
    - "Los cuatro rojos de causa ajena (TASK-0349, TASK-0350, TASK-0351, TASK-0352)."
  risk: high
  estimate: M
---

# TASK-0353 -- el pipeline borra el campo que el gate exige

## Confirmado por comportamiento

```python
import orchestrator as o
"obstacles" in o.TURN_SCHEMA_KEYS                          -> False
r = {..., "obstacles": []}
"obstacles" in o.schema_report(r)                          -> False
```

`schema_report()` (`runtime/orchestrator.py:482`) filtra el informe por `TURN_SCHEMA_KEYS`
(`:72-90`), y esa lista no incluye `obstacles`. La regla que TASK-0259 introdujo en
`runtime/turn_validate.py` exige el bloque. **En la ruta del orquestador, ningun productor puede
satisfacerla**: entregue lo que entregue, el campo no llega a la validacion.

## Por que esto no se arregla en la fixture

Es el motivo por el que Codex paro en TASK-0347 sin tocar produccion, y paro bien. Si se hubiera
"arreglado" la fixture para que pasara, se habria tapado un defecto real de produccion con un
cambio en el verificador -- que es exactamente lo que el AC5 de 0347 prohibe.

## La forma del defecto

Una **lista de claves permitidas** y una **regla de validacion** evolucionaron por separado. La
regla se endurecio; la lista no se entero. Ningun gate lo vio porque el sintoma aparece como
"fixture obsoleta" en doce runners a la vez.

Por eso el AC4 no pide anadir `obstacles` a la lista: pide el criterio que impide la **proxima**
divergencia. Anadir el campo cierra hoy y deja la clase abierta.

## Maker delivery

Implementation commit: `f4c6c3b9`.

- `schema_report()` now derives its accepted keys from `runtime/turn_schema.json`; the independent
  allowlist was removed.
- The permanent property derives validator-required top-level fields by behavior and proves that
  every one survives the filter; a production-function mutant that removes one derived field dies.
- The real orchestrator route accepts a delivery with `obstacles: []`.
- A freshly generated runtime instance executes the copied orchestrator and preserves the field.
- Validate-job replay changed from `54 PASS / 15 FAIL / 8 UNSUPPORTED` to
  `60 PASS / 9 FAIL / 8 UNSUPPORTED`. The same eight `pwsh` steps remain explicitly unsupported.
- Self-contained handoff:
  `Area_comun/mailbox/open/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353.md`.

Independent review is required. Codex is maker only.

## Remediation 2 maker delivery

Implementation commit: `897b9767`.

- Closure A is implemented. Before filtering, the routed schema must declare every top-level key
  conditionally required by the live semantic validator or the orchestrator exits loudly with the
  routed-schema/semantic-gap diagnostic.
- The permanent contract derives the semantic-only requirement set by behavior from a valid turn
  and requires exact agreement with the production declaration. The historical 1.2.0 schema proves
  both direct filtering and the real orchestrator CLI reject before the false missing-field symptom.
- The historical 0.10.0 runtime snapshot is preserved for compatibility, migration, and
  instantiation verification. It is not an integral parity mirror; two contracts intentionally
  compare only `parse_porcelain_v1_z` and `dirty_worktree_paths` with the live runtime.
- Exact-commit clean-worktree replay output:

```text
STEP 36/77 FAIL name=Run intent flow cases
STEP 43/77 FAIL name=Run event auth runtime override cases
STEP 50/77 FAIL name=Run runtime instantiation cases
STEP 53/77 FAIL name=Run runtime Review/QA cases
STEP 58/77 FAIL name=Run runtime loop cases
STEP 59/77 FAIL name=Run supervised autonomy cases
SUMMARY declared=77 pass=63 fail=6 unsupported=8
```

The balance and failure set are produced by the remediation run itself, not copied from a prior
delivery. Focused routed-turn behavior, 71/71 falsification inventory, canonical validation,
encoding, neutrality, compile, and diff gates pass on exact commit `897b9767` in a detached clean
worktree. Independent review is required; Codex is maker only.

## Remediation 3 maker implementation

Implementation commit: `1e178f3c`.

- The production predicate now covers optional top-level keys read by any routed validation gate,
  not only keys conditionally required by one sampled turn. The declared set is `actions`,
  `aggregate_version`, `decision_refs`, `fencing_token`, `gate`, `obstacles`, `tools`, and
  `transitions`.
- The permanent property derives 23 reports from all seven schema outcomes, all six action types,
  all eight production Review/QA transitions, plus concurrency and tool-policy probes. Executing
  the live gates observes 12 top-level reads: four schema-required keys and the exact eight-key
  optional declaration.
- Branch evidence proves blocked friction, human outcomes, every Review/QA transition, stale
  aggregate version, diff-required, decision-required, and human-required action paths are
  entered. A new blocked-turn `next_hint` production rule without a declaration changes the
  behaviorally observed set and is killed by the exact-set contract.
- The regression reported by the checker is now a permanent process-level negative: a routed
  schema without `actions` fails loudly before filtering, the real orchestrator CLI exits nonzero,
  and TASK-9000 remains `ready` instead of committing the unjustified contract change.
- Exact commit `1e178f3c` passes focused routed-turn behavior, the 73/73 falsification inventory,
  canonical validation, encoding, Python and PowerShell neutrality, compile, clean drift through
  seq 8748, diff gates, and clean tracked status in a detached Aegis worktree. The unrestricted
  validate-job replay exceeded the 15-minute local harness timeout. A bounded 30-second-per-step
  diagnostic replay completed at 59 PASS / 11 FAIL / 8 UNSUPPORTED; five failures are deliberate
  timeouts of legitimate long steps, and the remaining known red steps stay outside TASK-0353.
  This diagnostic balance is not acceptance evidence. Independent review is required; Codex is
  maker only.

## Remediation 5 maker implementation

Implementation commit: `c92be390`.

- The operator-selected closure removes the `required` subtraction: the behavioral contract now
  requires the complete consumed-key set to be contained in the routed root schema.
- The production guard is inverted from a maintained consumed-key list to filter coverage.
  `schema_report()` preserves the complete producer report and leaves acceptance or honest
  rejection to the routed schema, so no validation input can disappear before `validate_turn()`.
- The permanent production mutant reinstates the former schema-key filter and dies when it erases
  `changed_paths`; the coverage property does not depend on whether validation reads by `get`,
  iteration, or copying.
- CASO C is closed by the real orchestrator process: a routed schema without `changed_paths` receives
  an out-of-claim write, rejects the turn, creates no commit, and leaves the task `ready`.
- Focused runtime-turn behavior, 74/74 falsification inventory, collaboration validation, encoding,
  domain neutrality, drift, compile, and diff gates exited 0 before the implementation commit.

Independent review and ratification remain required. Codex is maker only.
