---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0336-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0336
status: open
created: 2026-08-08T07:50:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0336 -- la familia C.1, cerrada

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

## Lo que veo, como lectura mia y no como evidencia

La deteccion cuenta las barras finales y comprueba **paridad** (`% 2 == 1`), no un `endswith("\\")`
ingenuo -- porque `\` es una barra escapada y no una continuacion. El detalle importa: la version
ingenua habria dado falsos positivos sobre codigo correcto.

Verificado con el escape que describiste:

    gate sobre la forma actual                      exit 0
    continuacion de linea que oculta un `|| true`   exit 1   <- antes PASABA

## Los focos

**A. AC5, que era el que no cumplia.** Si ya no queda ningun escape vivo, que la certificacion
afirmativa se sostenga tal como se emite y lo digas con lo medido. Si queda alguno, que vaya
DECLARADO como residual y la certificacion acotada. Lo que no vale es un `runners=N/N contracts=M/M`
que prometa mas de lo que el gate puede sostener.

**B. Los trece mas las fronteras nuevas, y que sigan siendo PORTANTES.** Anadir fronteras puede hacer
que alguna se esconda detras de otra; verificaste esa propiedad una a una en r1 y r2 y quiero que
aguante.

**C. AC3 por los dos lados, otra vez.** Que la deteccion de continuacion no rechace formas correctas
-- una barra escapada legitima, un bloque bash multilinea que si gatea. Una regla que caza el escape
y rompe lo bueno nos deja igual: alguien la desactivara.

**D. Sin regresion.** El cableado del job intacto -- un paso por runner con `if: always()` -- y el
shell efectivo de la vuelta anterior.

## Nota

Si esto cierra, cierra la cadena entera que abrio la pregunta de hace dos dias: quien ejecuta de
verdad lo que el inventario cuenta. Ocho niveles, cada uno destapado midiendo el anterior. Y en cada
uno hubo alguien -- yo el que mas -- dispuesto a darlo por bueno.

Por eso te lo repito: **no lo cierres con prisa por eso.** Si queda un noveno, prefiero saberlo.

requested_action: Re-juzgar TASK-0336 en clon limpio sobre el commit exacto, correr tus mutantes mas
las fronteras nuevas, verificar AC5 y que AC3 sigue siendo cierto por los dos lados, y emitir
OK-CLOSABLE o CHANGES-REQUIRED.

question: Queda algun escape vivo, o la certificacion afirmativa ya se sostiene tal como se emite?
