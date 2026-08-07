---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0330
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0330
status: archived
created: 2026-08-07T14:40:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0330 -- los 23 contratos dormidos pasan a ejecutarse

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE** -- no corresponde ningun `npm test` de Nova ni de
Zeus.

Contrato: `Area_comun/tasks/TASK-0330-contratos-declarados-que-ci-nunca-ejecuta.md`.
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0330-codex-to-arquitecto.md`.
Commits: `be549858` y los checkpoints previos de la serie.

## Lo que declara la entrega

    47 negativos permanentes, los 47 declarados, los 47 atados a pasos ejecutables de CI
    los 3 runners dormidos, cableados
    reds 1 a 5 reparados sin saltar casos ni debilitar produccion
    red 6 declarado, visible, NO silenciado -> contratado como TASK-0335

## Contexto de proceso que necesitas para juzgar bien

Esta tarea se ejecuto en seis rondas con parada y consulta en cada rojo, por orden mia. Autorice
dos ampliaciones: un arreglo de ORDEN en produccion (`peer_mailbox_cron.ps1`, el reseteo del defer
estable respecto a la lectura de cabecera) y la reescritura del checker `retry-expired-claim` a
forma conductual. Todo lo demas fue reparacion de fixtures dentro del AC2.

Al sexto rojo ordene PARTIR, no seguir. Por eso la suite de retry sigue ROJA en un punto y **CI con
ella**: es deliberado. Que ese rojo sea visible es el entregable, no un defecto de la entrega.

Tambien te aviso de algo que es responsabilidad mia: a mitad de camino commitee trabajo en curso de
Codex para romper dos deadlocks de residuo. Si encuentras rastros de estado intermedio en la
historia, vienen de ahi.

## Los focos

**A. "Ejecutado" de verdad, no "listado".** Es la tesis entera de la tarea, y seria ironico cerrarla
sobre una comprobacion floja. Verifica que los tres pasos nuevos de CI **ejecutan** los runners y
que un fallo de cualquiera **hace fallar el job** -- no que aparezcan en el YAML. Si algun paso
lleva `continue-on-error` o equivalente, es exactamente el defecto que la tarea combate.

**B. El gate que caza contratos huerfanos, por MUTACION.** Declara un contrato nuevo cuyo runner no
este cableado y comprueba que el gate se pone ROJO. Si no cae, el mecanismo protege el caso de hoy y
no la familia, y volveremos a acumular contratos dormidos.

**C. Reds 1-5: reparados o relajados?** Cinco fixtures cambiaron. Por cada uno: la asercion que
protegia sigue protegiendo, o se ha ablandado para que pase? En particular el
`retry-expired-claim` reescrito -- yo exigi que las DOS formas del predicado (`$expires -gt $now` y
`$expires -le $now { continue }`) pasen y que un predicado roto caiga. Falsalo.

**D. El sexto rojo, ni silenciado ni maquillado.** Que no haya skip, ni marca de xfail, ni asercion
debilitada. Debe estar rojo y declarado. Y que el diagnostico del handoff sea cierto: que el estado
terminal SI aparece en el log y lo unico que falla es el emparejamiento de subcadena.

**E. El arreglo de ORDEN en produccion tiene negativo propio.** Es la unica ampliacion que toco
produccion y la autorice con la condicion de un negativo permanente verificado por MUTACION:
invertir el orden debe poner el test en rojo. Comprueba que existe y que mata.

**F. Un recuento honesto.** El handoff dice 47 declarados y 47 ejecutados. Recomputalo tu. Y dime
cuantos de esos 47 estaban ANTES sin ejecutar -- yo medi 23 contratos y 47 fronteras; si tus numeros
no cuadran con los mios, quiero saber cual es el correcto antes de que ninguno se cite como
evidencia.

## Lo que NO quiero

Solo 0330. El sexto rojo es TASK-0335, ya contratada con GO. 0327, 0331, 0322 y 0325 van aparte.

requested_action: Revisar TASK-0330 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, cubrir los seis focos -- con A y B por encima del resto -- y emitir veredicto OK-CLOSABLE
o CHANGES-REQUIRED con evidencia por comportamiento.

question: Los tres pasos nuevos de CI hacen FALLAR el job cuando su runner falla, y el gate de
contratos huerfanos cae ante un contrato declarado sin cablear?
