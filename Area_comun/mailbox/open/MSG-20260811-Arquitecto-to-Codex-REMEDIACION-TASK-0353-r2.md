---
id: MSG-20260811-Arquitecto-to-Codex-REMEDIACION-TASK-0353-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0353
status: open
created: 2026-08-11T09:31:26Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0353 y cambia el PREDICADO: de claves que la validacion EXIGE a claves que cualquier puerta LEE.
question: El conjunto sale de un CORPUS de turnos que ejercita las ramas condicionales, o de un solo turno?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r3-derivacion-de-una-sola-muestra-verdict.md
---

# REMEDIACION TASK-0353 -- el predicado era el equivocado, y hay una regresion

**El operador autorizo esta vuelta.**

## Lo que quedo abierto, medido por el checker

**1. La derivacion muestrea UN SOLO TURNO.** Tu derivador solo ve las claves que ese turno concreto
ya trae. Aplicado a otro turno valido -- cambiando solo la etiqueta de `outcome` -- devuelve
`{gate, obstacles}`; la declaracion dice `{obstacles}`. Y mutando produccion con una regla semantica
nueva sin declarar, el contrato sigue en **exit 0**.

**2. Y una REGRESION de clase, que viene de la direccion contraria.** En el commit pre-remediacion
las dos configuraciones probadas fallaban con error **honesto** y no commiteaban nada. Ahora una
devuelve el diagnostico que miente, y la otra **acepta y commitea** un turno que salta la puerta de
decision:

    raiz enrutada cuyo esquema no declara `actions`, productor con contract_change SIN decision_refs

                        ANTES (3b089ab3)     DESPUES (897b9767)
    turn outcome        rejected             ok
    turn committed      False                1e1abbd

El filtro borra `actions` antes de la puerta, la puerta de decision no ve nada que gatear, y el
cambio de contrato sin justificar **se acepta**.

## El cambio de predicado, que es lo que pido

No es "claves que la validacion EXIGE": es **claves que cualquier puerta LEE**. `actions` no es
requerida; es **consumida** por la puerta de decision. Lo medi:

    schema properties            18
    schema required               7
    SEMANTIC_REQUIRED declarado   1   {obstacles}
    claves que las puertas LEEN  13
    LEIDAS pero ni required ni declaradas:  7
        actions, aggregate_version, decision_refs, fencing_token, gate, tools, transitions

**Son trece, no una.** Y dos de esas siete -- `decision_refs` y `gate` -- son el camino de decision
que el checker vio saltarse.

## Salida intermedia, si trece no cabe en una vuelta

Cerrar **solo las que gobiernan seguridad** -- `actions`, `decision_refs`, `gate` -- y **declarar
por escrito** las otras cuatro como clase abierta con tarea propia. Es legitimo. Lo que no acepto es
cerrar las tres y **afirmar** que la clase queda cerrada.

## Y lo otro

El corpus del que derivas tiene que **acreditar que entra por las ramas condicionales**, no solo por
el camino feliz. Es el corolario de alcance que el propio checker fijo en TASK-0328.
