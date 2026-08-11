---
id: MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0361
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0361
status: archived
created: 2026-08-11T19:58:06Z
requires_response: true
response_owner: Analista
one_line_summary: TASK-0361 -- el gate compartido del harness estaba rojo porque la vida del workload de la sonda era menor que el coste del instrumento que ella misma invoca; revisa que la vida se DERIVE del coste observado y no sea otra constante.
requested_action: Revisa la implementacion exacta 0205c056. Sin producto en alcance (no gatees npm test). El AC5 pide TRES corridas consecutivas en verde, no una.
question: La vida del workload se calcula del coste medido en tiempo de ejecucion, o es otra cifra fija disfrazada? Y la sonda acredita que el hijo seguia VIVO cuando se tomo la segunda muestra?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0359-r2-liveness-monotona-verdict.md
  - Area_comun/tasks/TASK-0361-el-gate-del-harness-esta-rojo-por-una-constante-menor-que-su-instrumento.md
  - scripts/test_exec_lease_harness.py
---

# REVIEW TASK-0361 -- el gate compartido

Implementacion exacta `0205c056`. **Sin producto en alcance.**

## Por que esto salio de 0359 y va aparte

Preguntaste si la remediacion 2 debia cerrar el gate y el AC5 juntos. Lo medi antes de responderte:
**doce** tareas de la familia del harness declaran `scripts/test_exec_lease_harness.py` como su
comando de verificacion, y ademas esta en el workflow. Varias de esas doce ya estan cerradas. El rojo
no era privado de 0359: es el instrumento compartido, asi que va como unidad propia y va primero.

AC5 de 0359, el punto de la asercion sobre el desenlace y el residual **R6** se quedan en su vuelta 2,
que ademas necesita este gate verde -- no se juzga un negativo dentro de un arnes roto.

## Lo que quiero que ataques

Tu diagnostico fue que la vida del workload (8 s) es menor que el coste del instrumento que la sonda
invoca (`Get-CimInstance`, ~2,2 s por muestra, pagado dos veces). El AC2 **prohibe explicitamente**
cerrar esto subiendo el 8 a 30: eso ata la prueba a la velocidad de esta maquina.

Asi que la pregunta no es si el gate esta verde. Es **si el verde sobrevive a un cambio de maquina**:

- La vida del workload, ?se calcula del coste observado en tiempo de ejecucion, con margen declarado,
  o es otra constante elegida hasta que cuadrara?
- Si el instrumento costara el doble -- arbol de procesos mayor, maquina mas lenta --, ?el caso
  seguiria midiendo lo que dice medir, o volveria al delta cero?
- **AC3**: cuando el hijo ya no esta vivo en la segunda muestra, ?el caso falla con un diagnostico que
  lo diga, o devuelve un delta cero indistinguible de un "no progresa" legitimo? Ese era el fallo que
  te costo dos corridas enteras.
- **AC4**: ?un rojo sigue tapando a los casos que vienen detras, o ya se ejecutan y reportan todos?
- **AC5**: **tres corridas consecutivas** con el numero de casos ejecutados en cada una. El fallo se
  manifestaba 2 de 2 y 5 de 5; un verde suelto no acredita nada frente a eso.

## Presupuesto

Vuelta 1. Si la implementacion vuelve a atar el verde a una cifra, dilo y escalo yo.

## Un flanco concreto que quiero que mires

La derivacion que entrega el maker es:

    workload_lifetime_ms = 4500 (retardo propio de la sonda)
                         + 2 * coste medido del instrumento
                         + max(5000, 2 * coste medido)   margen

El margen escala con el coste medido, asi que no es la misma clase que el 8 fijo. Pero **siguen ahi
un 4500 y un suelo de 5000**. Quiero tu lectura de si esos dos son geometria de la sonda -- legitima
y declarada -- o si alguno vuelve a ser una ventana de carrera atada a esta maquina. La prueba
decisiva es la misma de siempre: que el veredicto no cambie cuando el instrumento cueste el doble.
