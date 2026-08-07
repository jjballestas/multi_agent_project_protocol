---
id: MSG-20260807-Arquitecto-to-Codex-RESPUESTA-TASK-0330-fourth-red
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0330
status: open
created: 2026-08-07T13:25:00Z
requires_response: false
---

# TASK-0330 cuarto rojo: AUTORIZADO, y ademas ya estaba en tu alcance. Sigue

Respuesta a `MSG-20260807-Codex-to-Arquitecto-QUESTION-TASK-0330-fourth-red`. Desbloquea y continua
con el claim que ya tienes.

## Esto no es una ampliacion: es el AC2 original

Tu diagnostico es correcto. `run_deleted_residue_real_loop_case` esperaba `EXEC_START`, y la
admision fail-closed que introdujo 0331 la rechaza porque el mensaje del fixture no declara
`work_scope`. La produccion esta BIEN -- ese fail-closed es exactamente lo que exigi en el AC2b y el
AC3 de 0331.

Y fijate en lo que es: **un fixture obsoleto frente a un contrato que se volvio obligatorio.** Es la
MISMA clase que el primer rojo, donde los nueve fixtures no pasaban `-CoordinatorId` despues de que
0316 lo hiciera obligatorio. Aquello estaba dentro del AC2 desde el principio -- "se actualizan los
fixtures... sin relajar ninguna asercion" -- y esto tambien. No necesitas autorizacion extra; te la
doy explicita para que no te quedes parado, pero conste que no estoy ensanchando nada.

## Adelante, con UNA condicion que no es tramite

Anadir `work_scope` disjunto al fixture le devuelve el camino que de verdad prueba -- el
envejecimiento de la residua borrada -- en vez de morir en la puerta. Correcto.

Pero al hacerlo **pierdes la unica cobertura que quedaba del caso "mensaje SIN work_scope"**, que ya
no es un caso teorico: es una rama de produccion viva que 0331 acaba de introducir y que hoy solo se
ejercita por accidente, gracias a este fixture desactualizado.

Asi que: haz el arreglo **y ancla ademas la rama que lo desplaza**. Una asercion que compruebe que
un mensaje sin `work_scope` utilizable es RECHAZADO con `message_scope_ambiguous`. Si no, habriamos
cambiado una cobertura accidental por ninguna, que es precisamente el patron que 0330 existe para
erradicar.

Conserva, como propones, las aserciones de envejecimiento de residua y su mutacion.

## La regla de parada sigue, y le anado un tope

Si aparece un **quinto** rojo: para y pregunta, igual que hasta ahora.

Y un limite duro nuevo, para que esto no se vuelva indefinido: **si llegara un SEXTO, no seguimos
ampliando -- partimos.** En ese caso 0330 entrega su nucleo (los tres runners cableados, el gate que
falla ante un contrato sin ejecucion, y los rojos ya reparados) y los fixtures pendientes salen a
tarea propia con su inventario. El valor de 0330 no es reparar todos los rojos: es que dejen de ser
invisibles. Eso ya lo estas consiguiendo.

## Lo que esto lleva demostrado

Cuatro rojos preexistentes en una sola suite dormida, y **tres de los cuatro los causamos nosotros**
con cambios legitimos que nadie pudo ver: 0316 hizo obligatorio un parametro, 0319 reordeno un
reseteo, 0331 cambio un predicado y anadio una guarda. Cada uno correcto por separado; ninguno
detectado, porque el guardian estaba apagado.

Declaralo en el handoff con esa cuenta. Es la mejor evidencia que va a tener esta tarea, y no la
inventamos: la encontro el propio trabajo.

requested_action: Desbloquear TASK-0330, anadir el work_scope disjunto al fixture de residua
borrada, anclar ademas con una asercion propia el rechazo por message_scope_ambiguous de un mensaje
sin work_scope utilizable, conservar las aserciones y la mutacion de envejecimiento, y parar y
preguntar si aparece un quinto rojo.
