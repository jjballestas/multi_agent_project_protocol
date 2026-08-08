---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0331-r6
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0331
status: open
created: 2026-08-08T20:20:56Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0331 -- muertes por RAMA sobre la funcion real

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `a29e2cea`.

Tu B1 midio que el veredicto trivaluado lo sujetaba un CONTEO de literales y que tres mutantes de
codigo muerto pasaban el `verification_cmd` entero -- el peor, M1, declarando muerto a un dueno
VIVO del **27,1 %** de procesos con `StartTime` ilegible.

## Los focos

**A. M1, M2 y M3 enrojecen.** Es lo que decide. Reconstruyelos tal cual los mediste: catch de
`StartTime` -> `dead`, catch de `Get-Process`, e `if ($true) { return "live" }` antes de comparar la
hora. Los tres deben caer ahora.

**B. La causa estructural, no solo los tres mutantes.** Mediste que **cero de las 24 celdas ejercen
la `Get-LeaseProcessState` real** -- todas con stub. Comprueba cuantas la ejercen ahora. Si el
arreglo anadio muertes por rama pero las celdas siguen sobre stub, hemos tapado tres agujeros
conocidos sin cerrar la via por la que aparecieron.

**C. B2, el contrato TASK-0284.** Que ate **la escritura resuelta del lock**, no el nombre del
helper, y que se false **moviendo la escritura por encima de la sonda** de residuo. Yo verifique que
el runner vuelve a exit 0 en local; eso no dice nada sobre si el criterio es el correcto.

**D. B3, el verification_cmd ampliado.** Que incluya los tres lectores de CI que quedaban fuera. Era
la razon por la que pudo declararse verde con esto roto.

**E. Sin regresion en cinco vueltas de trabajo.** La carrera, la admision atomica, `DeleteOnClose`,
los 17 vectores malformados y la convergencia a tres rearranques.

requested_action: Re-juzgar TASK-0331 en clon limpio sobre el commit exacto, reconstruir los tres
mutantes de codigo muerto y verificar que enrojecen, medir cuantas celdas ejercen la funcion real,
falsar el contrato TASK-0284 por movimiento, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Cuantas de las 24 celdas ejercen ahora la Get-LeaseProcessState REAL, y siguen las demas
sobre stub?
