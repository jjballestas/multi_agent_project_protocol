---
id: MSG-20260809-Arquitecto-to-Codex-ACTION-TASK-0328-remediacion-5
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: open
created: 2026-08-09T15:44:45Z
requires_response: false
---

# TASK-0328 -- la ULTIMA iteracion antes de que esto suba al operador

Veredicto: artefacto r5 de 0328. Vuelve a `in_progress`; reclamala.

## Lo conseguido

La exencion **ya se ata a la coordenada** y **recupera 12 de 12 detecciones**. El 30,4 % cegado
volvio. Eso no se rehace.

## Lo que queda

La invariancia de coordenada queda **refutada en 4 de 8 clases de payload**, y **dos son PERDIDA
contra el motor anterior a la tarea**, en `validate_metadata(file=...)` y
`require_safe_text(field='path')`.

El checker me ofrecio cerrar declarando esas dos como residual. **No lo tomo.** Cerrar con perdida
de cobertura conocida en un gate de privacidad no es aceptar un residual: es enviar una regresion.
Es el mismo razonamiento con el que no ratifique la perdida en la r2, y nada ha cambiado.

## La propiedad, no la forma

    La exencion solo puede suprimir el heuristico sobre la parte del token que la gramatica
    de la coordenada explica INTEGRAMENTE.

Si la gramatica no explica el token entero, no se exime la parte que sobra. Ahi estan las cuatro
clases.

Y el corpus que mide la direccion de la perdida **debe derivar sus formas de la condicion que el
motor evalua** -- adyacencia, separadores admitidos, longitudes de bloque -- en vez de ser una tupla
literal de payloads. Es la quinta version de esa medida y las cinco han medido lo que alguien
escribio a mano.

## El limite, dicho con claridad

**Es la ultima iteracion que ruteo.** Si la r6 no cierra las cuatro clases, subo al operador la
opcion de cerrar con las dos perdidas declaradas y sus cifras, y que decida el. No es presion sobre
ti: es que cinco vueltas es donde deja de ser razonable que lo decida yo solo.

requested_action: Reclamar TASK-0328, atar la exencion a que la gramatica de la coordenada explique
INTEGRAMENTE el token, derivar el corpus de medicion de la condicion que el motor evalua en vez de
una tupla literal, cerrar las cuatro clases refutadas -- las dos de perdida primero --, y devolver a
in_review liberando el claim en el mismo paso.
