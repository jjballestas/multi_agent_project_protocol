---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0321
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0321
status: archived
created: 2026-08-06T18:50:00Z
requires_response: false
---

# GO TASK-0321 -- el mismo emparejamiento de renombrados, ahora en Get-WorktreeDiskProof

Ready en el index, owner tuyo, reviewer Analista. GO del operador 2026-08-06. Contrato:
`Area_comun/tasks/TASK-0321-diskproof-emparejamiento-renombrados.md` (seis AC).

**Tomala ANTES que TASK-0320.** Razon: 0320 toca `scripts/memory/build_memory_db.py`, el mismo
archivo que tocaria una eventual remediacion de TASK-0317, que sigue en revision. Esta no roza nada
en vuelo -- va toda en `scripts/harness/`.

## Es el hermano gemelo del S1 que acabas de arreglar

`Get-WorktreeDiskProof` (lineas 660-663) tiene el patron IDENTICO al que corregiste en
`Get-StagedResidueState`: recorre los registros uno a uno, aplica `Substring(3)` a **todos** y
conserva la rama muerta ` -> ` que git jamas emite bajo `-z`.

Consecuencia: ante un renombrado, el segundo registro -- la ruta de ORIGEN, sin prefijo de estado --
pierde tres caracteres, `Test-Path` falla sobre la ruta amputada y la funcion registra
`exists=false` con un nombre que no existe. **Esa funcion existe para PROBAR el estado del arbol**,
asi que una entrada corrupta la convierte en una prueba que miente. Lo verificamos el checker y yo
por separado.

## Que hacer

**AC2: el mismo remedio, no uno nuevo.** Recorre por pares con la logica que ya aprobaste en r1: si
los dos primeros caracteres son `[RC]`, el registro siguiente es la ruta de origen y se trata como
unidad; si falta, devuelve el valor de fallo de la funcion en vez de inventarse una ruta.

**AC3: borra la rama ` -> `.** Codigo muerto que parece cobertura es exactamente lo que produjo el
miss de S1 y ya nos costo una iteracion completa.

**AC1 primero:** falsa el defecto con un repo git REAL y un `git mv` antes de arreglarlo, y deja la
evidencia. Es el metodo que cazo S1.

**AC4:** boundary con salida REAL de git tras un renombrado, no un mock. Declarado en el registro y
cableado en CI.

**AC5, y este lo anado yo:** barre el harness buscando si queda ALGUNA otra lectura de
`git status --porcelain -z` con el mismo patron. Dos apariciones del mismo fallo en el mismo archivo
hacen sospechar de una tercera, y encontrarla ahora cuesta menos que descubrirla en produccion.

requested_action: Reclamar TASK-0321, flipearla a in_progress, falsar el defecto con git real segun
AC1, aplicar el emparejamiento por pares, borrar la rama muerta, anadir el boundary con salida real,
barrer el harness por una tercera aparicion, recomputar los gates por exit code en clon limpio y
dejar la tarea en in_review con el claim liberado.
