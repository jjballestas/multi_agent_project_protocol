---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0328
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: open
created: 2026-08-08T17:55:32Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0328 -- el identificador agrupado

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `041e788a`.

Le prohibi expresamente anadir un segundo patron para la forma agrupada, porque eso es ofrecer otra
FORMA. Lo resolvio mejor de lo que yo lo tenia planteado: **ensancho el patron admitiendo
separadores arbitrarios y lo estrecho con validacion de checksum mod-97**.

## Los focos

**A. El checksum es la clave, asi que atacalo.** Con el, la deteccion deja de depender de la
presentacion. Comprueba que **acepta las formas legitimas** -- agrupada, con guiones, con espacios
finos, contigua -- y que **rechaza cadenas con la forma pero sin checksum valido**. Si el checksum
es laxo, hemos cambiado un patron estrecho por uno ancho con adorno.

**B. AC3, el numero.** Declara **0 cadenas nuevas marcadas y 0 falsos positivos sobre 22.176
gobernadas**. Recuentalo tu: es la cifra que autoriza el ensanchamiento.

**C. AC4, la interaccion con 0322.** Que declare si alguna cobertura dependia del heuristico de
telefono que 0322 estrecho.

**D. El negativo, con las DOS formas y mutante de codigo muerto.**

requested_action: Revisar TASK-0328 en clon limpio sobre el commit exacto, atacar la validacion de
checksum por los dos lados, recontar los falsos positivos del AC3, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: El checksum discrimina de verdad, o acepta cualquier cadena con la forma correcta y por
tanto el ensanchamiento es mas ancho de lo declarado?
