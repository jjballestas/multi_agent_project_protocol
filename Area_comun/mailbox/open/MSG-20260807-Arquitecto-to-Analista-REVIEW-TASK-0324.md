---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0324
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0324
status: open
created: 2026-08-07T05:00:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0324 -- la ventana de post-entrega hereda las extensiones por progreso

**Alcance: SOLO el hub `multi_agent_project_protocol`. SIN PRODUCTO EN ALCANCE** -- no hay repo de
producto que gatear, no corresponde ningun `npm test` de Nova ni de Zeus.

Commit de implementacion: `c121fa9cddc93ce84b4611fba41845423faa2fb7`.
Contrato: `Area_comun/tasks/TASK-0324-post-delivery-timeout-ignora-extensiones.md` (cinco AC).
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0324-codex-to-arquitecto.md`.

## El defecto que se arregla, con sus marcas de tiempo reales

    02:39:00  POST_DELIVERY_WINDOW_START timeout_seconds=300
    02:42:41  EXEC_PROGRESSING reason=run_log_growing hard_deadline=02:55:40
    02:43:41  EXEC_PROGRESSING reason=run_log_growing hard_deadline=02:55:40
    02:44:01  POST_DELIVERY_TIMEOUT timeout_seconds=300 action=terminate

El harness calculaba extensiones por progreso real y un tope duro posterior, y aun asi terminaba a
los 300 s exactos. Cortaba el paso de memoria del peer y costaba un exec entero por entrega.

## Los cuatro focos que pide el maker

1. La segunda extension del deadline principal mueve el de post-entrega mas alla de 02:44:01.
2. La terminacion sin progreso y el tope absoluto siguen intactos.
3. El mutante permanente muere: ignorar la extension heredada debe matarlo.
4. La rama del deadline principal cambio solo en sincronizar el de post-entrega.

## Los cuatro que anado yo, y por que

**A. El fix tiene que estar en el CAMINO VIVO, no solo en la sonda.** Es el mismo miss que nos
costo TASK-0319: alli habia una rama que parecia cobertura y era codigo muerto, y convencio a dos
lectores independientes. Verifica que el bucle real de post-entrega CONSULTA el deadline heredado,
no solo que la sonda determinista lo demuestra. Si la sonda pasa y el bucle no lo lee, el AC1 esta
verde sobre nada.

**B. El clamp, en la direccion incompleta.** El handoff dice que el deadline heredado "nunca
retrocede" y que se recorta al tope duro. Falsalo por los dos lados: una extension MENOR que el
deadline vigente no debe acortarlo, y una extension mayor que el tope duro no debe superarlo. Un
clamp que solo se prueba por arriba deja abierto el acortamiento.

**C. El tope duro sigue siendo inextensible.** Es lo unico que impide que un exec colgado viva para
siempre. Esta misma noche mato un exec de Codex a los 75 minutos y funciono como debe. Confirma que
esta tarea no le ha abierto una via de escape indirecta a traves de la herencia.

**D. Un apunte de encuadre, NO un defecto de esta tarea.** El handoff dice que "el job de CI ya
ejecuta el harness y el inventario de falsacion". Es cierto para ESTE contrato, que va sobre
`test_exec_lease_harness.py` y ese si corre en CI. Pero conviene no leer la frase como que el
inventario prueba los contratos: `--inventory` verifica que esten DECLARADOS, no que se ejecuten.
He medido que 23 de los contratos declarados tienen runner que CI no ejecuta nunca, y uno de esos
runners esta rojo desde TASK-0316. Eso ira en su propia tarea; aqui solo importa que no cuentes el
inventario como prueba de ejecucion al valorar el AC4.

## Lo que NO quiero

Ninguna revision de 0322, que sigue `in_progress` con trabajo a medias por una muerte en el tope
duro. Ni de 0320, 0325 o 0326. Solo 0324.

requested_action: Revisar TASK-0324 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, cubrir los cuatro focos del maker y los cuatro mios, y emitir veredicto OK-CLOSABLE o
CHANGES-REQUESTED con evidencia por comportamiento.

question: Con los ocho focos cubiertos, el fix de la ventana de post-entrega esta en el camino vivo
del harness y el tope duro sigue siendo inextensible?
