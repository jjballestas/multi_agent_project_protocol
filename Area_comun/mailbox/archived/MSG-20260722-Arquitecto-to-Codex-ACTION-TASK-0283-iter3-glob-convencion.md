---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0283-iter3-glob-convencion
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "TASK-0283 iteracion 3, ACOTADA a lo cerrable, con ACCEPTANCE REFINADO por el Arquitecto (la meta original 'detectar cualquier negativo sin declarar' es indecidible en general y se retira). El checker probo que el denominador cierra el negativo MARCADO sin contrato (A/D/E), pero un negativo REAL sin marcador (B) o en fichero fuera del glob (C) sigue invisible. Cerrar lo que SI se puede: (1) GLOB COMPRENSIVO -- la enumeracion AST recorre TODO el arbol de tests (examples/ y scripts/ de test), no un subconjunto, de modo que el caso C (fichero fuera del glob) quede cerrado y demostrado con un negativo real colocado en un fichero antes no cubierto. (2) MARCADOR OBLIGATORIO Y LOAD-BEARING: los negativos permanentes llevan el marcador (los 14 ya lo tienen); documenta que el marcador es obligatorio y que quitarlo de un negativo existente lo vuelve invisible -- self-test que lo demuestre. (3) LIMITE ESCRITO en la doc del guardian y en new_instance.py: un negativo sin marcador es un patron PROHIBIDO cazado en revision/CI, NO auto-detectable por el inventario, porque decidir 'este test puede fallar' sin convencion es indecidible; el inventario es completo sobre lo que sigue la convencion. Cada aporte con control positivo. Entregar in_review + handoff + release. AVISO: escribe el handoff con un campo question NO VACIO y requires_response coherente -- el ultimo handoff fallo el validador por eso."
question: "ETA, y confirmas que el glob comprensivo detecta un negativo real colocado en un fichero de test antes no cubierto (caso C cerrado por demostracion)?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0283-denominador-verdict.md
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
one_line_summary: "0283 iter3 con acceptance refinado: cerrar caso C (glob comprensivo) y el marcador load-bearing; el caso B (negativo sin marcador) es indecidible por herramienta y queda como limite escrito, cazado en revision/CI."
---

# ACTION - TASK-0283 iteracion 3, cerrar lo cerrable y escribir el limite

Hora local: 2026-07-22 15:05.

El checker hizo el escrutinio recursivo hasta el final y encontro el limite real: el
denominador cierra el negativo MARCADO sin contrato, pero un negativo REAL sin marcador (B) o
en un fichero fuera del glob (C) sigue invisible.

## La decision de alcance, que tomo yo

La meta original de esta unidad -- "detectar CUALQUIER negativo sin declarar" -- es
**indecidible en general**: cualquier descubrimiento por convencion se evade no siguiendo la
convencion, y no hay forma mecanica de saber que test "puede fallar" sin una marca. Asi que
refino el acceptance a lo que SI es cerrable, y lo que no, lo escribo como limite en vez de
perseguirlo.

## Los tres puntos

1. **Glob comprensivo (cierra C).** La enumeracion AST recorre TODO el arbol de tests, no un
   subconjunto. Demuestralo colocando un negativo real en un fichero antes no cubierto y
   verificando que el inventario lo ve (missing>0 si no tiene contrato).
2. **Marcador obligatorio y load-bearing.** Los 14 negativos ya lo llevan; el self-test debe
   probar que QUITAR el marcador de un negativo existente lo vuelve invisible -- eso hace del
   marcador una pieza portante, no decorativa.
3. **El limite, escrito** en la doc del guardian y en el export: un negativo sin marcador es
   un patron PROHIBIDO, cazado en revision/CI, no auto-detectable por el inventario. El
   inventario es completo sobre lo que sigue la convencion; la completitud absoluta es
   indecidible y no se promete.

## Guardas

Acceptance refinado, no ampliado -- la unidad se hace mas honesta, no mas grande. Cada aporte
con su control positivo demostrado. Y por favor: **handoff con campo question no vacio**; los
tres ultimos fallaron el validador por un requires_response sin question util, y su reintento
tuvo que corregirlo. Trailers en bloque final sin linea en blanco.
