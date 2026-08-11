---
id: MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0353-r4
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0353
status: open
created: 2026-08-11T13:39:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en r4 -- el CASO B deja de commitear y el conjunto SI se deriva, pero el contrato le resta la lista required del hub y con una raiz sin changed_paths un turno que escribe fuera del scope de su claim se acepta y se commitea.
requested_action: No cerrar TASK-0353 con el AC4 marcado como cumplido. Iteracion 2 de 2 ya consumida en r3 - elevar al operador humano la eleccion entre (1) dejar de restar el required del hub y exigir consumed_keys <= turn_schema_keys(root) entero, o (2) declarar cerrado el alcance en las ocho claves derivadas y abrir tarea propia para la clase con el CASO C como AC de partida.
question: Elevas al operador la opcion (1) quitar la resta del required dentro de TASK-0353, o la (2) cerrar el alcance en las ocho claves derivadas y abrir tarea propia con el CASO C (changed_paths, commit fa2b670) como AC de partida?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r4-la-resta-del-required-verdict.md
  - Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0353-r4.md
  - Area_comun/artifacts/Analista-TASK-0353-r3-derivacion-de-una-sola-muestra-verdict.md
---

# VERDICT TASK-0353 r4 -- CHANGE-REQUIRED

Ancla `02c58629d11c7f5b4b6f109e313c8bd656cd3658`, implementacion `1e178f3c` (ancestro verificado).
Dos clones limpios, exit codes reales, sin producto en alcance. Veredicto completo en el artefacto.

## Tus dos preguntas

**1. El CASO B deja de commitear. Si.** Por el proceso real, no por la llamada directa: raiz enrutada
sin `actions` + `contract_change` sin `decision_refs` -> guard levanta, `PROCESS exit 1`, commits
`1 -> 1`, tarea en `ready`. Control con el esquema vivo: `rejected` con el error honesto, tampoco
commitea. El CASO A cae con el mismo guard. **Cerrado.**

**2. El conjunto se DERIVA, no esta enumerado.** Sale de los enums del propio esquema (`outcome`,
`actions.items.type`) y de `review_qa.REVIEW_QA_EVENTS`, ejecutando `validate_turn` de produccion con
una sonda de lectura, y `assert_branch_coverage` acredita que cada forma entra por la rama que dice
cubrir. Ademas el mutante MP4 que sobrevivio en r3 ahora **muere** contra una mutacion real de
produccion (exit 1). Credito real.

## Por que aun asi no cierra

El contrato compara `optional_consumed = consumed_keys - set(base_schema["required"])`. **Le resta la
lista `required` del esquema del hub**, y nadie exige que una raiz enrutada conserve ese `required`.
Toda clave consumida que este en esa lista queda fuera del guard: `changed_paths`, `task_id`,
`agent`, `outcome`, `summary`, `turn_id`, `commit_message`.

**CASO C, medido, proceso real, con control.** Raiz enrutada sin `changed_paths`; el productor
escribe fuera del scope de su claim:

```
C1 sin changed_paths : guard NO levanta -> filtro borra changed_paths -> validate_turn() == []
                       turn outcome: done   turn commit: fa2b670   commits 1 -> 2   task: done
C0 esquema vivo      : validate_turn() == ['semantic: write outside active claim scope: ...']
                       turn outcome: rejected   sin commit   task: ready
```

Unica variable: la lista de propiedades del esquema de la raiz. Es el CASO B una clave mas alla, y lo
que se apaga es la frontera de escritura del sistema de claims.

Segundo punto ciego, menor: la sonda graba `get`/`__getitem__`/`__contains__` pero no iteracion ni
copia. La **misma** regla que el contrato dice cazar, escrita como `payload = dict(report)`, esta viva
en produccion y el contrato sigue en **exit 0**.

Negativo honesto: intente saltar la puerta humana quitando `outcome` de la raiz y **no se puede** --
variante y control se rechazan igual.

## Puertas en el ancla (clon limpio)

`validate_collaboration_state` 0 / `scan_encoding` 0 / `scan_domain_neutrality` 0 /
`check_falsification_contracts` 0 / `protocol_replay --check-drift` 0 (CLEAN, seq 8769) /
`run_runtime_turn_obstacle_cases` 0. Ancla verde, drift 0.

## Lazo esperado

Iteracion 2 de 2 consumida en r3: la decision es del operador. **(1)** dentro de TASK-0353, quitar la
resta y exigir `consumed_keys <= turn_schema_keys(root)` entero -- una linea en el contrato y una en
el guard, cierra el CASO C sin corpus nuevo; la version que cierra ademas el punto ciego de la sonda
es la inversion que ya recomende en r3 (afirmar la cobertura del filtro, no mantener una lista).
**(2)** cerrar el alcance en las ocho claves derivadas y abrir tarea propia con el CASO C como AC.

Lo que no acepto es cerrar con el AC4 marcado como cumplido.

-- Analista
