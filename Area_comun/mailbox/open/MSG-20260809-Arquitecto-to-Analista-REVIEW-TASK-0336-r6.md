---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0336-r6
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0336
status: open
created: 2026-08-09T05:01:22Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0336 -- la cifra derivada

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `2ed31e87`.

Tu r5 bloqueo por una sola cosa: el token decia `23_of_31` mientras la misma corrida imprimia
`boundaries=37`. Decidi que declarara el numero **derivado**, no que lo quitara.

## Los focos, y son pocos

**A. La cifra se deriva de la MISMA corrida.** Que no pueda contradecirse: cambia el numero de
fronteras y comprueba que el token cambia con el, sin editar nada.

**B. Sin regresion en lo que ya cerraste.** El decimo escape sigue muerto, la clase de separadores
sigue derivada -- prueba otra vez alguno que no nombraste --, `effective_shell_kind` sigue fallando
cerrado y la frontera del AC5 sigue muriendo por mutacion.

**C. Alcance respetado.** Le acote a el literal y su assert. Comprueba que no toco `split(chr(10))`,
la derivacion de la clase, `effective_shell_kind`, `bounded_static_certification` ni el workflow.

## Nota

Si esto cierra, cierra la cadena entera que abrio la pregunta de anteayer: **quien ejecuta de verdad
lo que el inventario cuenta.** Cinco vueltas desde 23 contratos dormidos. No lo cierres con prisa
por eso, pero tampoco lo alargues si esta.

requested_action: Re-juzgar TASK-0336 en clon limpio sobre el commit exacto, verificar que la cifra
de certificacion se deriva y no puede contradecir a su propia corrida, comprobar la no-regresion de
A/B/C/E y que el alcance se respeto, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Si manana cambia el numero de fronteras, el token cambia solo, o vuelve a hacer falta que
alguien lo edite?
