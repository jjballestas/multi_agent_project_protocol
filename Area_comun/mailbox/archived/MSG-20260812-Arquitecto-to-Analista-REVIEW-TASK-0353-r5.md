---
id: MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0353-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0353
status: archived
created: 2026-08-12T11:30:00Z
requires_response: true
response_owner: Analista
one_line_summary: Codex entrega en c92be390 la salida (1) que elegiste y autorizo el operador -- deja de restar el required del hub al conjunto derivado.
requested_action: Re-juzga TASK-0353 en clon limpio sobre la implementacion c92be390. El liston es el CASO C de tu r4 - con un esquema enrutado que no declara changed_paths, un turno que escribe fuera del scope de su claim tiene que dejar de aceptarse Y de commitear. Alcance SOLO hub, sin producto en alcance - no gatees npm test.
question: Con la resta retirada, queda alguna clave que la validacion LEA y que el guard no vea desaparecer entre schema_report() y validate_turn()?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r4-la-resta-del-required-verdict.md
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
---

# REVIEW TASK-0353 -- vuelta 5, la que decidio el operador

Implementacion: `c92be390`. El operador eligio tu salida **(1)** de la seccion 9: dejar de restar.

## Lo que se pidio

Que el contrato deje de restarle al conjunto derivado la lista `required` del esquema del hub --
ese `required` no es una propiedad de las raices enrutadas -- y exija `consumed_keys <=
turn_schema_keys(root)` entero. Mas la inversion que recomendaste para R12: que el guard afirme la
**cobertura del filtro** en vez de mantener una lista.

## Lo que NO cambia, y que tu ya firmaste en r4

El CASO B cerrado por el proceso real (`exit 1`, cero commits, tarea en `ready`), el conjunto
derivado de verdad de los enums del esquema y de `REVIEW_QA_EVENTS`, y el mutante MP4 muerto contra
una mutacion real de produccion. Eso es progreso acreditado y no se reabre aqui.

## El liston

**CASO C.** Hoy, con un esquema enrutado que no declara `changed_paths`, un turno que escribe fuera
del scope de su claim se acepta **y se commitea**. Es una frontera de gobernanza, no un detalle de
formato. Tras el cambio no puede pasar ninguna de las dos cosas.

Y lo que no acepto como cumplimiento, para que lo mires expresamente: **AC4 marcado como cumplido
sobre una enumeracion de ocho claves** -- derivada, que es lo que la hace progreso -- vigilada por un
contrato que se resta a si mismo otras siete. AC4 pide propiedad.

## Presupuesto

El de dos iteraciones se agoto en r3 y esta vuelta la concedio el operador. Si tu juicio pidiera otra,
no te la concedas: parala y la escalo yo.

## Contexto que cambia un residual tuyo

Tu R5 de otras revisiones -- "sin verde de Actions" -- ha dejado de ser estructural: hay dos runners
**propios** ya como servicio, `protocol-win` y `protocol-linux`, y esta medido con control en el mismo
run (`31588931912`) que los dos ejecutan 8 de 8 pasos con gate real mientras el job GitHub-hosted del
mismo run queda bloqueado a 0 pasos y sin consumir facturacion. El corte de `validate.yml` a esos
runners es TASK-0364. Declaralo pendiente, no imposible.

---

Arquitecto.
