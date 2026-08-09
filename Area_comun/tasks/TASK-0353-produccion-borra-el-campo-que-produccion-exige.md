---
id: TASK-0353
title: Produccion borra el campo que produccion exige -- schema_report elimina obstacles justo antes de validate_turn
status: in_progress
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
