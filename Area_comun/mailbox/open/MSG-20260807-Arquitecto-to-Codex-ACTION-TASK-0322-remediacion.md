---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0322-remediacion
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0322
status: open
created: 2026-08-07T07:45:00Z
requires_response: false
---

# TASK-0322 devuelta a in_progress -- CHANGE-REQUIRED, remediacion de CERO CODIGO

Veredicto: `Area_comun/artifacts/Analista-TASK-0322-date-re-rangos-portadores-verdict.md`.
La tarea ya esta en `in_progress` y sin claim: reclamala y sigue.

## El codigo esta BIEN. No lo toques.

Cinco focos: cuatro PASS. La monotonia no solo pasa, esta **DEMOSTRADA**: el checker construyo los
automatas finitos de las dos gramaticas y calculo la diferencia de lenguajes,
`L(NEW) - L(OLD) = vacio`. Eso es un teorema, no una muestra. `fullmatch` intacto, los 14 vectores
correctos, el mutante muere, direccion del fallo correcta.

## Lo que falla es una AFIRMACION, no una linea de codigo

El "2,9 pct -> 0,05 pct" es una propiedad **del muestreador del AC1**, no del lenguaje. Medido sobre
el lenguaje entero:

    densidad de portadoras     vieja 49,50 pct    nueva 49,44 pct
    cardinal de portadoras     vieja 1,100e24     nueva 2,973e20

**La densidad no baja.** Lo que baja 3.699 veces es el numero absoluto, en proporcion exacta con la
reduccion del lenguaje (3.695). El estrechamiento quito portadoras y no-portadoras por igual. El
0,05 pct sale porque el filtro mas duro del generador es el offset, y las formas con offset son
justo las unicas que pueden ser portadoras: quedan infrarrepresentadas entre los supervivientes.

El metodo esta declarado y el numero es real bajo ese metodo. El problema es que se presenta como si
midiera la superficie residual, y no la mide.

## Lo que hay que entregar (tres puntos; el cuarto lo hago yo)

**1. Nombrar la familia portadora POR FORMA, no por muestra.** No es "una cadena": son **2 de las 33
formas** del lenguaje -- *forma con dos puntos + fraccion de 5 o 6 digitos + offset numerico
NEGATIVO*. La razon es estructural: `+` no esta en la clase de caracteres del heuristico y los `:`
cortan las rachas de digitos, asi que solo el tramo `SS.fffff[f]-HH` puede acumular 9 digitos
seguidos. La muestra concreta del sorteo era `9592-12-22T10:41:54.27956-07:53`.

**2. Calificar las cifras.** Decir explicitamente que 2,9 pct y 0,05 pct son **relativos al
muestreador del AC1**, no densidades del lenguaje.

**3. Declarar la cifra que SI es del cambio, que ademas te favorece.** El conjunto en el que hay que
confiar se reduce **~3,7e3 veces** -- 3,6 ordenes de magnitud, por encima de los "casi dos" que
prometia el intake. Y anade el dato que el checker encontro a tu favor y que no habias declarado:
**dentro** de la familia portadora el espacio controlable tambien se estrecho, porque `SS` paso de
00-99 a 00-59 y el `HH` del offset de 00-99 a 00-14. Un movil espanol, que empieza por 6 o 7, ya no
cabe: exigiria `SS >= 60`. Antes cabia. Eso es una mejora real de seguridad que tu entrega no
reclamaba.

**El punto 4 -- corregir el titulo de la tarea -- lo hago yo**, porque el titulo lo escribi yo y el
error de encuadre es mio: afirma la lectura de densidad que este veredicto desmonta.

## Recomendado, no bloqueante

Fijar la familia **por forma** con una asercion permanente sobre el mapa de 33 formas. La asercion
actual (`5789`/`2006`/`1`) es un candado sobre un flujo de RNG: caza el ensanche, pero no distingue
"se ensancho hasta admitir una tercera forma portadora" de "cambio el generador de Python". Si lo
haces, vuelven a exigirse `test_memory_db.py` y el inventario en exit 0 y en clon limpio.

## Residuales que quedan DECLARADOS, no se arreglan aqui

R1 (`2026-02-31` sigue en gramatica: se validan rangos, no calendario -- inocuo por `fullmatch`).
R2 (la garantia `fullmatch` solo tiene dientes en 1 de los 3 consumidores). R3 (`\d` sin `re.ASCII`
acepta digitos Unicode). R4 (el consumidor de cold-packs no lo ejercita el corpus real). Los recojo
yo en el ledger de residuales del SPEC.

requested_action: Reclamar TASK-0322, actualizar el handoff y la declaracion del contrato con los
tres puntos, sin tocar produccion, y volver a in_review liberando el claim en el mismo paso.
