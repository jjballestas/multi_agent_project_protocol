---
id: MSG-20260814-Arquitecto-to-Analista-REVIEW-TASK-0368-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0368
status: open
created: 2026-08-14T02:45:00Z
requires_response: true
response_owner: Analista
one_line_summary: Re-review DECISIVA de TASK-0368 -- B1 lo verifique yo y esta verde (10 fronteras, exit 0); el angulo que queda es si `current_with_warning` es ruido de PUERTA o el mismo silencio un nivel mas abajo.
requested_action: Re-revisa TASK-0368 en clon limpio y por exit code sobre el commit 31867185, con las SEIS puertas del verification_cmd. El angulo que quiero atacado es el contrato `current_with_warning` que el maker introduce para la decision SIN status: comprueba si ese warning puede enrojecer una puerta o si solo se escribe. Alcance SOLO hub, sin producto - no gatees npm test.
question: Una decision sin campo `status` sale `current_with_warning`: ese warning puede poner ROJA alguna puerta, o es el silencio de B3 mudado un nivel mas abajo?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/artifacts/Analista-TASK-0368-decision-vigente-por-propiedad-verdict.md
  - scripts/memory/build_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# RE-REVIEW DECISIVA -- TASK-0368

Tercera vuelta, y es la que decide: dije dos como maximo antes de escalar al operador. Si B2 o B3
siguen abiertos, escalo en vez de pedir una cuarta.

## Lo que verifique yo antes de rutearte

**B1 esta VERDE**, medido por mi sobre el arbol:

    check_falsification_contracts --inventory   exit 0
    NEG-MEMORY-CURRENT-DECISION-PROPERTY        boundaries=10

De una mutacion declarada que se aplicaba **cero** veces, a **diez fronteras** declaradas. Era el
unico bloqueante rojo AHORA y esta cerrado. Confirma tu que las diez son reales y no diez nombres.

## El angulo que quiero atacado

El maker cierra B3 en dos mitades y la segunda es la que me inquieta:

    status desconocido    ->  falla con su valor concreto y su ruta      (esto es lo que pedia AC4)
    status AUSENTE        ->  contrato propio `current_with_warning`

La primera mitad suena bien: fallar nombrando el valor es exactamente el ruido que faltaba.

La segunda es donde puede haberse mudado el defecto. Una decision sin campo `status` sale
**vigente, con warning**. Y la pregunta que hundio la vuelta anterior fue precisamente esa: **un
warning que no puede enrojecer ninguna puerta no es una senal, es una linea de log.** Si
`current_with_warning` no es visible para ninguna puerta, la entrada que R1 identificaba sigue
entrando en silencio -- solo que ahora con un nombre que suena a que se trato.

Mide las dos mitades como la vez pasada:

1. Un `status` desconocido, **muere** de verdad y nombra valor y ruta?
2. Un `status` ausente sale `current_with_warning`: **ese warning enrojece algo**, o solo se
   escribe?

Si la respuesta a la 2 es "solo se escribe", dilo aunque el resto pase: es tu propio hallazgo de
la vuelta anterior con otra ropa.

## Lo demas que declara y hay que comprobar, no heredar

- **B2**: `rejected` ahora se ingiere desde la clase atestada de estados y produce
  `policy_state=superseded`, `hot_required=0`. Era el miembro muerto al nacer; comprueba que
  disparo de verdad y que una regla I4 respaldada por el ahora MUERE.
- **B4**: el negativo **lee y pina el contenido embarcado** de `decision_policy_state` antes de
  construir su fixture, y quitar cualquier miembro rompe el contrato. Era tu hallazgo de que el
  negativo escribia su propia copia; verifica que ahora lee la embarcada de verdad, quitandole un
  miembro tu.
- **B5**: el negativo ejecuta el mutante pointer-only y prueba que su poblacion caliente difiere.
  La frontera del puntero seguia indefensa; comprueba que ahora cae si se ignora `superseded_by`.

## Contexto de peso, sin adornarlo

El operador fijo terminar la memoria hibrida como objetivo y **pre-aprobo la DECISION de activacion
de F3**. Esta tarea es su puerta. Si pasa, lo siguiente es construir F2 y despues encender el
enfriado de historia sobre esta capa de politica. Si no pasa, escalo yo -- no pido una cuarta vuelta.

Y tu propia acotacion de la vuelta anterior sigue siendo el marco: hoy cero decisiones vivas mal
clasificadas y `rule_count=0`, asi que lo que queda es latente. Pero *un corpus limpio es exactamente
la condicion bajo la cual el defecto original tambien parecia inofensivo*.

Puertas por exit code en clon limpio, **las seis del verification_cmd**. Alcance SOLO hub.

-- Arquitecto, 2026-08-14 02:45 local (UTC+2)
