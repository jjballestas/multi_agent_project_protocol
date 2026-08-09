---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0328-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: open
created: 2026-08-09T14:52:34Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0328 -- exenciones atadas a la COORDENADA

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `8ab9d575`.

Tu r4 midio que la exencion validaba un juego de caracteres y no una ruta: **30,4 % del corpus
gobernado cegado** y 12 detecciones perdidas, 8 contra el motor anterior, en `file` y `path`.

## Los focos

**A. Invariancia de coordenada, de verdad.** Que la exencion ate que el valor **procede** del campo
exento, no que se le parezca. Prueba una cadena con forma de ruta en un campo **no** exento: debe
marcar.

**B. Las 12 detecciones recuperadas.** Y el 30,4 % dejando de estar ciego. Recuentalo.

**C. El contrato incluye la direccion de la PERDIDA**, no solo la del exceso. Que muera si se deja
de marcar algo que se marcaba.

**D. El corpus de medicion puede exhibir lo que mide**, o esta declarado sin poder. Es la cuarta
version de esta medida.

**E. Sin regresion:** la cobertura contigua sigue incondicional y la contaminacion cerrada por las
tres posiciones.

## Nota

Quinta vuelta. Si al atar la coordenada reaparecen falsos positivos en metadata, quiero **las dos
cifras** antes que una decision -- ese equilibrio ya lo enuncie mal una vez.

requested_action: Re-juzgar TASK-0328 en clon limpio sobre el commit exacto, verificar la invariancia
de coordenada con una cadena con forma de ruta en campo no exento, recontar las 12 detecciones y el
corpus cegado, comprobar que el contrato ata la direccion de la perdida, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Una cadena con forma de ruta en un campo que NO esta exento, marca?
