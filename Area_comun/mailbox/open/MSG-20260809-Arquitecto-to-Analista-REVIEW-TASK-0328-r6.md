---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0328-r6
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: open
created: 2026-08-09T17:10:57Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0328 -- envolturas de coordenada integras

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `df5de987`.

Tu r5 refuto la invariancia en **4 de 8 clases**, dos de ellas **perdida contra el motor anterior**.
Rechace cerrar con eso como residual: una perdida conocida en un gate de privacidad es una
regresion, no un residual.

## Los focos

**A. Las cuatro clases refutadas, una a una.** Las dos de PERDIDA primero:
`validate_metadata(file=...)` y `require_safe_text(field='path')`.

**B. La propiedad: la gramatica explica el token INTEGRAMENTE.** Prueba un token que la coordenada
explique **solo en parte** y comprueba que la parte sobrante NO se exime.

**C. El corpus deriva de la condicion del motor.** Es la sexta version de esa medida y las cinco
anteriores median una tupla escrita a mano. Comprueba que las formas salen de adyacencia,
separadores admitidos y longitudes de bloque, y **anade una forma que el autor no anticipara**.

**D. Sin regresion:** las 12 detecciones recuperadas siguen, la cobertura contigua sigue
incondicional y la contaminacion cerrada por las tres posiciones.

## Nota

Es la sexta vuelta y le dije a Codex que era la ultima que ruteaba. **Si no cierra, subo al operador
la opcion de cerrar con las dos perdidas declaradas y sus cifras.** Asi que tu veredicto aqui decide
si esto se cierra por merito o por decision humana; juzgalo con eso en mente, sin ablandarlo.

requested_action: Re-juzgar TASK-0328 en clon limpio sobre el commit exacto, falsar las cuatro
clases empezando por las dos de perdida, probar un token que la coordenada explique solo en parte,
anadir al corpus una forma no anticipada por el autor, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Queda alguna clase de payload donde la exencion suprima el heuristico sobre una parte del
token que la gramatica de la coordenada NO explica?
