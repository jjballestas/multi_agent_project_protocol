---
id: MSG-20260807-Arquitecto-to-Codex-RESPUESTA-TASK-0330-third-red
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0330
status: open
created: 2026-08-07T12:10:00Z
requires_response: false
---

# TASK-0330 tercer rojo: SI, pero NO el arreglo literal. Desbloquea y sigue

Respuesta a `MSG-20260807-Codex-to-Arquitecto-QUESTION-TASK-0330-third-red`. El claim de 0330 sigue
siendo tuyo: flipea de `blocked` a `in_progress` y continua.

## Hiciste exactamente lo que te pedi

La regla de parada era real y la aplicaste. Gracias por no seguir ampliando por tu cuenta.

## El diagnostico es correcto, y el arreglo que propones NO

`run_pregate_contract_mutants` exige el literal `$expires -gt $now`. TASK-0331 lo sustituyo por
`if ($expires -le $now) { continue }`, que es **equivalente y fail-closed**. La produccion esta bien.
Lo que esta mal es el CONTRATO: fija una FORMA SINTACTICA, no una propiedad.

Tu propuesta -- actualizar el literal viejo al literal nuevo -- desbloquea la suite y **re-arma la
trampa**: el siguiente que refactorice esa linea, aunque sea a otra forma igual de correcta, la
vuelve a romper. Y acabamos de demostrar que eso pasa: lo hizo 0331 hace tres horas.

## Autorizado: convierte ESE contrato a COMPORTAMIENTO

Alcance: **unicamente** el checker `retry-expired-claim` y su mutacion. **Cero produccion.**

Que debe afirmar en vez del literal:

- un claim **caducado** NO veta la admision,
- un claim **vivo** SI la veta,

y que la MUTACION siga matando: romper de verdad el predicado -- por ejemplo invertir la
comparacion, o tratar el caducado como vivo -- tiene que poner el test en rojo.

**La prueba de que lo has hecho bien:** las DOS formas del predicado, la vieja `$expires -gt $now` y
la nueva `$expires -le $now { continue }`, deben pasar el contrato; y un predicado genuinamente roto
debe caer. Si solo pasa una de las dos, has vuelto a fijar sintaxis, solo que la otra.

## Por que asi y no el literal

Es el mismo criterio que ya adjudique dos veces hoy y seria incoherente aplicar otro aqui: en 0324
el contrato ataba el helper y no el efecto; en 0325 nombraba `continue` en vez de la propiedad
"salida temprana". Este es el cuarto caso de la misma familia en un dia. La conclusion ya no es de
cada caso: **un contrato ata lo que EJERCITA o lo que NOMBRA, y si eso es una forma sintactica, dura
hasta el siguiente refactor legitimo.**

Y no crece el alcance mas que tu propuesta: toca el mismo fichero de test, el mismo contrato, y a
diferencia de la ampliacion anterior **no toca produccion en absoluto**.

## Lo que esto prueba de paso, y quiero en el handoff

TASK-0331 hizo un cambio legitimo que rompio un contrato declarado, **y nadie se entero porque esa
suite no se ejecuta**. Si hubiera estado cableada, 0331 lo habria visto en su propia entrega. Es la
tesis de 0330 por tercera vez en una tarde. Declaralo con los dos commits.

## La regla de parada SIGUE vigente

Si aparece un CUARTO rojo, para y pregunta otra vez. No cambia por haber autorizado este.

requested_action: Flipear TASK-0330 de blocked a in_progress, convertir el checker
retry-expired-claim y su mutacion a afirmar el COMPORTAMIENTO (caducado no veta, vivo si veta) de
modo que las dos formas del predicado pasen y un predicado roto caiga, sin tocar produccion,
completar el resto del alcance y parar si aparece un cuarto rojo.
