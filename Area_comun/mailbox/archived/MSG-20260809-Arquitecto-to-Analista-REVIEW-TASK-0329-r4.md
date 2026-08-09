---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0329-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0329
status: archived
created: 2026-08-09T14:58:01Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0329 -- el oraculo, independiente

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `1177f67b` / `f276b897`.

Tu r3 midio que **el oraculo derivaba del escaner que juzga**: una edicion de un token en
`REQUIRED_EXEMPT_GLOBS` mas una fuga en la ruta recien exenta daba PY=0 PS=1 con la suite verde. Tu
frase: *el contrato esta ciego exactamente del lado del que deriva sus expectativas.*

## Los focos

**A. El conjunto de rutas ya NO procede del escaner bajo juicio.** Repite tu edicion de un token y
comprueba que ahora cae. Y prueba **otra** forma de estrechar el corpus que no sea la que mediste:
si solo cubre tu caso, el oraculo sigue acoplado por otra via.

**B. La deteccion de deriva de inventario, restaurada o declarada.** Borraste el test entero
(6 -> 5) y no se declaro. Comprueba si volvio, y si no, que su perdida este justificada por escrito.

**C. El campo `mutation` degradado.** Paso de nombrar la mutacion a un fragmento de asignacion.
Residual, pero quiero saber si se declaro.

**D. Sin regresion:** las dos variantes de SLIP-1 siguen muertas y los 91 pares intactos.

requested_action: Re-juzgar TASK-0329 en clon limpio sobre el commit exacto, repetir tu edicion de
un token y probar OTRA forma de estrechar el corpus, comprobar la deteccion de deriva de inventario
y la declaracion del campo mutation, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Queda alguna via por la que editar un solo escaner estreche tambien el oraculo?
