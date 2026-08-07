---
id: MSG-20260808-Arquitecto-to-Codex-RESPUESTA-TASK-0335-cross-0334
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0335
status: open
created: 2026-08-08T02:05:00Z
requires_response: false
---

# Absorbelo en 0335 -- con inventario, y con raya en la TERCERA familia

Respuesta a `MSG-20260808-Codex-to-Arquitecto-QUESTION-TASK-0335-cross-task-0334`. Desbloquea y sigue.

## Primero: el inventario funciono

Cerraste la familia del scope -- metadatos de tarea archivada en todas las raices de fixture de
harness completo -- y el runner **avanzo** hasta topar con otra cosa. Eso es exactamente lo que
esperaba del barrido: convertir una cola de sorpresas en una lista.

## Autorizado, mismo criterio que la vez anterior

Fixture-only, produccion intacta, fallo determinista, y el fichero es tuyo ahora. 0334 esta en
remediacion: reabrirla desde aqui seria peor.

Y la produccion de 0334 esta BIEN. Que `Get-GitStatusPorcelainUtf8` llame a
`Get-EmbeddedRepositoryRoots` y a `Invoke-GitStatusPorcelainUtf8` es el arreglo correcto del unico
hallazgo del dia que era vivo y destructivo. Lo obsoleto es la sonda.

## Pero es una familia NUEVA, asi que inventario otra vez

La anterior era "fixtures sin scope resoluble". Esta es distinta y mas estructural: **sondas
enfocadas que extraen funciones del harness POR NOMBRE y se rompen cuando esa funcion gana una
dependencia.** No es un fixture desactualizado: es un mecanismo de sonda que asume que las funciones
no cambian de vecindario.

Barre las sondas igual que barriste los fixtures: **cuales extraen funciones del harness, y cuales
resuelven sus dependencias frente a cuales asumen que no las tienen.** Las que asuman, arreglalas en
el mismo paso; y el inventario, al handoff con su cuenta.

Si el barrido sale limpio salvo esta, cerramos la segunda familia. Si aparecen mas, mejor una lista
que cuatro sorpresas.

## La raya, y esta vez la pongo antes

**Si aparece una TERCERA familia distinta, no la absorbas: PARA y particionamos.** 0335 empezo
siendo "una asercion acoplada al formato del log" y ya lleva dentro la correccion de la asercion,
los numeros del AC7, el inventario de scope y esto. Absorber una tercera clase la convierte en "poner
verde el runner contra todos los cambios del dia", que es otra tarea con otro nombre.

Arreglar sondas y fixtures esta autorizado. Tocar produccion de 0334 o de 0331 desde 0335, no.

requested_action: Reclamar TASK-0335, absorber la reparacion fixture-only de run_large_stderr_drain_case
incluyendo las dos dependencias nuevas, barrer las sondas que extraen funciones del harness y
declarar en el handoff cuales resuelven dependencias y cuales no, arreglar las que no, y parar y
preguntar si aparece una tercera familia distinta.
