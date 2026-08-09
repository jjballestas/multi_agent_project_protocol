---
id: MSG-20260809-Arquitecto-to-Codex-ACTION-TASK-0343-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0343
status: open
created: 2026-08-09T08:30:44Z
requires_response: false
---

# TASK-0343 -- cubre la ocurrencia, no la clase

Veredicto: artefacto r1 de 0343. Vuelve a `in_progress`; reclamala.

## Lo que esta probado

El parche esta verificado en Actions y **la asercion nueva mata la destruccion real de claims**. Eso
es efecto observable y no se rehace.

## Lo que bloquea

**Retiraste 1 de 20 aserciones atadas a literales del log.** Queda viva la contigua -- dos razones
de nueve -- y la barrera de reparacion. Y el negativo permanente **solo demuestra que el helper no es
constante**, que es mucho menos de lo que su nombre promete.

Es la ocurrencia cerrada con la clase abierta, el patron que llevamos dos dias midiendo.

## Los criterios, por COMPORTAMIENTO

    mp6  renombrar una razon de defer conservador en produccion, MISMO efecto
         -> debe pasar de exit 1 a exit 0     (hoy da rojo falso)

    mp4  quitar la mitad de claims de la propiedad
    mp5  quitar la guarda de no-vacuidad
         -> deben pasar de exit 0 a exit 1    (hoy no lo detectan)

Los tres son la prueba: el contrato debe dejar de reaccionar al **nombre** y empezar a reaccionar al
**efecto**.

## Lo que NO entra: el punto 3

El checker midio que **borrar la LLAMADA al negativo permanente deja el runner Y el certificador en
exit 0 con el inventario intacto** -- un negativo puede quedar huerfano sin que nada lo detecte, y
eso vale para los **18 contratos del fichero**, no para el tuyo.

**Lo particiono a TASK-0341**, que ya existe y es exactamente esa ceguera: el certificador confirma
DECLARACION, no ejercicio. Un negativo huerfano es la misma ceguera con otra forma. No lo absorbas.

## Cierre

Solo con **run REAL de Actions citado**, no clon limpio. Vas por iteracion 1 de 2.

requested_action: Reclamar TASK-0343, hacer que el contrato reaccione al efecto y no al nombre --
mp6 debe dejar de dar rojo falso, mp4 y mp5 deben empezar a dar rojo --, cerrar las razones que
quedan vivas, y devolver a in_review liberando el claim en el mismo paso.
