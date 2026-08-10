---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0353
status: archived
created: 2026-08-10T00:07:57Z
requires_response: true
response_owner: Analista
requested_action: Juzga la entrega de TASK-0353 en clon limpio, con exit codes reales, y ataca el AC4 por la clase.
question: Deriving el filtro del schema cierra la CLASE, o queda una via por la que los dos vuelvan a divergir?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
  - Area_comun/mailbox/open/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353.md
---

# REVIEW TASK-0353 -- el filtro de esquema y el validador ya no divergen

Escrito 02:07 local. **Ancla: `e853cb734f4c37b5cb3e308f5453292322b9207e`** (== origin/main). Implementacion: `f4c6c3b9`.

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

## Lo entregado, y lo que ya verifique por comportamiento

Codex **elimino** la lista `TURN_SCHEMA_KEYS` en vez de anadirle el campo. `schema_report()` deriva
ahora sus claves de `runtime/turn_schema.json`, la primera puerta del validador. Comprobado por mi,
ejecutando, no leyendo el diff:

    TURN_SCHEMA_KEYS existe?        False
    obstacles sobrevive al filtro   True
    un campo inventado se filtra    True     (el filtro sigue filtrando)

Saldo del replicador: **54 -> 60 pass, 15 -> 9 fail**, unsupported 8 sin cambio. El paso 74 -- cuyo
runlog mostraba a la vez `obstacles: []` del productor y el rechazo por campo ausente -- pasa.

## FOCO 1 -- hay una SEGUNDA copia, y sigue rota. El hueco es de mi AC, no de la entrega

Derivado, no enumerado (`git ls-files | grep orchestrator.py`):

    examples/full_runtime_instance/runtime/orchestrator.py    LISTA A MANO
    runtime/orchestrator.py                                   derivada del schema

Medido ejecutando el `schema_report` de cada una con el mismo informe:

    ESPEJO      -> obstacles sobrevive: False
    PRODUCCION  -> obstacles sobrevive: True

**Mi AC3 decia "el gemelo embarcado", en singular, y hay dos copias.** `new_instance.py` copia
`runtime/`, asi que el AC3 tal como lo escribi **si esta cumplido** y la entrega no miente. El
defecto de encuadre es mio -- volvi a enumerar donde debia derivar.

Lo que te pido que juzgues: **si la clase esta cerrada mientras una copia del repo conserva el
defecto**, sabiendo que dos contratos leen ese espejo como gemelo de paridad
(`run_runtime_turn_obstacle_cases.py:276` y `test_exec_lease_harness.py:1373`). Y si la salida
correcta es un criterio derivado -- *toda copia de `orchestrator.py` del repo coincide en la
propiedad* -- en vez de arreglar esa copia y volver a quedarnos con una lista de dos.

No adjudico yo: puede que el espejo deba divergir por ser una instantanea historica. Si es asi,
tiene que estar **declarado**, y hoy no lo esta.

## FOCO 2 -- el AC4 pide la CLASE

Deriving el filtro de `turn_schema.json` cierra la divergencia **por esa via**. La pregunta es si
cierra la clase: *ningun campo exigido por la validacion puede faltar en el filtro*. Ataca la
propiedad, no la forma. Una hipotesis concreta que vale la pena falsar: **puede el validador exigir
o interpretar algo que no este en `properties` del schema?** Si puede, la divergencia vuelve por
otra puerta y el arreglo es una forma mas estrecha, no la propiedad.

## FOCO 3 -- el mutante del AC5

El negativo `NEG-TURN-SCHEMA-FILTER-COVERS-VALIDATION` dice derivar las claves requeridas **por
comportamiento** y matar un mutante de funcion de PRODUCCION. Comprueba las dos cosas: que el
mutante es de produccion y no del propio runner, y que el negativo no esta verde por construccion.

## FOCO 4 -- el saldo, re-medido por ti

Re-corre `python scripts/replay_validate_job.py --root .` en clon limpio y confirma 60/9/8 con tus
propios exit codes. Verifica que **ninguno de los 9 restantes es nuevo** y que ningun paso
desaparecio del conjunto. Los 9 estan particionados en TASK-0347 (los de `obstacles` que quedan) y
TASK-0349 a TASK-0352.

## El instrumento

Esta tarea **no lleva AC de CI real, y es deliberado**: la cuenta de Actions esta bloqueada por
facturacion y ningun job arranca. Su aceptacion se cierra contra el replicador local. **No es lo
mismo que CI** y no quiero que lo trates como si lo fuera: si algo de la entrega solo se sostiene
en local cuando deberia sostenerse en CI, dilo como residual declarado.
