---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0332-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0332
status: open
created: 2026-08-09T14:58:01Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0332 -- la matriz prefijo x offset

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `3a5cc335`.

Tu r1 midio que **exhaustivo en una coordenada no es exhaustivo en la familia**: los 1.684 offsets
con las demas coordenadas congeladas, y un retorno falsy sobre otro prefijo colaba un email con la
suite verde -- con un offset DENTRO del conjunto declarado exhaustivo.

## Los focos

**A. Tus dos escapes medidos.** `2027-` y la hora en forma basica `T092823`. Los dos deben morir.

**B. Una TERCERA coordenada que no nombraste.** Si el barrido solo cubre prefijo y offset, prueba a
variar otra cosa -- separador, zona, longitud fraccionaria. Es la diferencia entre ampliar el
muestreo y cerrar la familia.

**C. No estrecho la clave.** Le prohibi anadir casos especiales; comprueba que produccion sigue sin
tocar y que no hay listas de excepciones nuevas.

**D. El coste.** La matriz puede pesar mas que el barrido lineal; mide y declara.

**E. El residual del alfabeto ASCII declarado.**

requested_action: Re-juzgar TASK-0332 en clon limpio sobre el commit exacto, falsar tus dos escapes,
probar una tercera coordenada que no nombraste, verificar que no se estrecho la clave, y emitir
OK-CLOSABLE o CHANGES-REQUIRED.

question: Variar una coordenada que TU no nombraste sigue colando algo, o la familia esta cerrada?
