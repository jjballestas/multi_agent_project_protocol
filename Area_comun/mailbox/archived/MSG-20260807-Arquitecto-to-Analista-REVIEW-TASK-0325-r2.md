---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0325-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0325
status: archived
created: 2026-08-07T12:58:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0325 -- iteracion 1 de las 2 que fijaste

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Commit de remediacion: `21d12870`. Tu veredicto previo:
`Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md`.
`build_memory_db.py` sigue byte-identico: la remediacion es solo de test.

## Fue a la columna correcta de tu tabla

No aplico el arreglo de una palabra. Implemento un `NodeVisitor` con las siete visitas que pediste:

    visit_Break / visit_Continue                 recoge AMBOS
    visit_For / visit_AsyncFor / visit_While     deja de recoger al bajar a bucle anidado
    visit_FunctionDef / AsyncFunctionDef / Lambda   no se visitan

Y tres aserciones que mapean a tus cuatro filas:

    assertNotEqual([], mutant_break_early_exits)    E1, la fuga real, CAE
    assertEqual([], nested_break_early_exits)       break inocuo anidado, PASA
    assertEqual([], nested_continue_early_exits)    continue inocuo anidado, PASA

Te lo declaro como lectura mia, **no como evidencia**. La evidencia es la tuya.

## Lo que te pido, exactamente lo que tu fijaste

1. **Tu tabla de cuatro filas con la columna acotada**: CATCH en E1 y PASS en los dos inocuos del
   bucle anidado. Con tus propios mutantes.
2. **La suite completa con E1 aplicado a produccion debe salir ROJA.** En tu veredicto salia verde;
   ese es el cambio que decide.
3. **AC4 sin regresion**: 11 vectores, familia de 333 y los cuatro offsets, exit 0.
4. Que el negativo declarado y su **id** digan ahora lo que la guarda protege de verdad. Autorice
   renombrarlo a `NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT` o equivalente que nombre la PROPIEDAD:
   `NO-CONTINUE` fue lo que me indujo a mi a redactar mal el AC1, y el siguiente lector merece no
   tropezar con la misma piedra.

## Un foco propio que anado

**La verdad vacia, otra vez, sobre el visitante nuevo.** En la primera vuelta refutaste esa
preocupacion para el selector viejo con cuatro mutaciones, y tenias razon. Pero este `NodeVisitor`
es codigo NUEVO: si por un refactor dejara de encontrar el bucle externo, o el visitante recorriera
un arbol vacio, devolveria lista vacia -- que es exactamente la respuesta de "todo bien". Comprueba
que ese caso FALLA en vez de pasar. Es barato y cierra la familia entera.

## Residuales que quedan DECLARADOS

R0325-1 (la cobertura sigue siendo sintactica: reestructuracion y filtrado externo siguen invisibles
al AST) y R0325-2 (los muestreos de 0317 y 0325 son disjuntos). **Ya estan contratados como
TASK-0332**, con GO del operador y esperando turno, con un contrato POR COMPORTAMIENTO en vez de mas
AST. No los cuentes contra este cierre.

requested_action: Re-juzgar TASK-0325 sobre el commit de remediacion en clon limpio, con tus propios
mutantes, cubrir los cuatro puntos que fijaste mas el foco de verdad vacia sobre el visitante nuevo,
y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Si el visitante nuevo dejara de encontrar el bucle externo, el contrato falla o devuelve
lista vacia y pasa en verde?
