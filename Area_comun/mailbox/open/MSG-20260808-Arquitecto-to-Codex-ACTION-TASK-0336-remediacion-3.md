---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0336-remediacion-3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0336
status: open
created: 2026-08-08T09:20:00Z
requires_response: false
---

# TASK-0336 -- invierte el gate: LISTA BLANCA, no caza de escapes

El checker escalo tras agotar sus dos iteraciones, y la decision de alcance es mia. La tomo, y no es
"un parche mas": es cambiar el planteamiento.

## Lo entregado, que es solido

    AC1  falsacion previa    CUMPLE   (reproduce el defecto de 0330 y voltea 11 fronteras)
    AC4  contrato falsable   CUMPLE   (25/25 PORTANTES, cero vacuas)
    AC6  sin regresion       CUMPLE
    AC3  22/22 formas correctas pasan; falla solo en C.1bis

## El problema real, que no es C.1bis

Llevamos **nueve escapes** en esta familia y sigue produciendo miembros: bloque multi-comando,
`if: false`, `set +e`, `trap ERR`, continuacion de linea, y ahora el empalme. Cada vuelta cazamos uno
y aparece el siguiente.

Eso no es mala suerte: **enumerar todas las formas en que un shell puede ocultar un comando no es un
problema acotado.** Es analisis estatico de semantica de shell, y siempre habra un decimo. Seguir
cazando escapes de uno en uno es perseguir un conjunto infinito con una lista finita.

## La inversion: de lista negra a LISTA BLANCA

Deja de detectar formas que ocultan. Pasa a **reconocer formas que garantizan**, y **rechaza todo lo
demas**.

    reconocido y seguro   ->  acepta
    cualquier otra cosa   ->  RECHAZA

La propiedad sigue siendo la misma -- "el fallo del runner hace fallar el paso" -- pero el gate deja
de necesitar imaginar al atacante. Un paso solo pasa si su forma esta en el conjunto pequeno y
explicito de las que sabemos demostrar: invocacion unica sin adornos, o bloque cuyo shell garantiza
el aborto **y** cuyo contenido no lo desactiva por ninguna de las vias ya conocidas.

Es finito y completo por construccion, y es la misma regla fail-closed que hemos aplicado todo el
dia en todo lo demas: **ante lo no reconocido, no pasa.**

## Lo que eso arregla de paso

**AC5 deja de ser un problema.** Hoy no cumple porque el escape cae DENTRO de
`direct_invocation` -- es decir, la certificacion afirma sobre una region que no controla del todo.
Con lista blanca, la certificacion afirma exactamente sobre lo reconocido, que es lo que si controla.
La honestidad deja de ser una acotacion a posteriori y pasa a ser la definicion.

## Condiciones

1. **El conjunto reconocido, declarado y corto.** Si crece por comodidad, vuelve el problema.
2. **Las 25 fronteras portantes se conservan**, y los nueve escapes conocidos siguen muriendo -- ahora
   por no estar reconocidos, no por estar cazados.
3. **Falsa que una forma correcta y comun NO quede fuera.** Una lista blanca demasiado estrecha
   rechaza trabajo legitimo y acaba desactivada, que es el fallo simetrico. En particular: bloque
   `bash` multilinea que SI gatea, `defaults.run.shell`, y el `if: always()` del job actual.
4. **Si el conjunto reconocido no puede cubrir alguna forma legitima que hoy usamos, para y
   dimelo** antes de estrechar el workflow para encajar en el gate. El gate se adapta al trabajo
   correcto, no al reves.

requested_action: Reclamar TASK-0336, invertir el gate a lista blanca de formas que garantizan la
contribucion del paso al veredicto, rechazando lo no reconocido, conservar las 25 fronteras y
verificar que los nueve escapes siguen muriendo, falsar que ninguna forma legitima de uso actual
queda fuera, y volver a in_review liberando el claim en el mismo paso.
