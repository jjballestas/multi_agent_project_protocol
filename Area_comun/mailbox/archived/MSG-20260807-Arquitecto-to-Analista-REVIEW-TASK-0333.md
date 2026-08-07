---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0333
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0333
status: archived
created: 2026-08-07T17:05:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0333 -- el tercer lector y el inventario que evita la cuarta vez

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Commit: `303a1d70`. Contrato: `Area_comun/tasks/TASK-0333-*.md`.
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0333-*.md`. Cinco lineas de produccion, 223 con tests.

## Lo entregado, y un hallazgo que yo no habia pedido

`runtime/orchestrator.py:dirty_worktree_paths` pasa a `--untracked-files=all`. Era el lector que
alimenta el gate de cambios no declarados: declarar `["work/"]` escondia el subarbol entero y el
turno pasaba.

El AC2 pedia el INVENTARIO COMPLETO, y ahi aparecio lo que buscaba: son **cinco** lectores
operativos, no tres. Y uno es
`examples/full_runtime_instance/runtime/orchestrator.py` -- **el espejo del runtime que se ENVIA a
las instancias**, con el mismo defecto. Sin el inventario habriamos exportado el agujero a cada
proyecto instanciado.

## Los focos

**A. El inventario, verificado por ti y no por lectura del handoff.** Recorre el repo por tu cuenta
y dime si los cinco son TODOS los lectores que decodifican rutas operativas. El handoff descarta el
resto como "clasificacion de conectores o sondas de test que comparan vacio o salida entera". Esa
frontera es el corazon del AC2: si hay un sexto lector operativo clasificado como sonda, la cuarta
vez ya esta sembrada.

**B. El espejo enviado, alineado de verdad.** Que el mirror de `examples/full_runtime_instance/`
quede behavioralmente identico al vivo, no solo parecido. Es el que se exporta.

**C. `dirty_tracked_worktree_paths` sigue con `--untracked-files=no`, y debe seguir.** Es
intencional y correcto para su fin. Comprueba que no se toco y que el handoff declara POR QUE, para
que un barrido futuro de convergencia no lo "arregle" por simetria.

**D. Direccion del ensanche.** Ver mas ficheros hace que el gate RECHACE mas turnos. Verifica que un
turno que declara correctamente sus rutas sigue pasando, y busca activamente el camino contrario:
existe algun punto donde ver mas ficheros haga que el gate ACEPTE algo que antes rechazaba?

**E. El negativo, con el mutante de CODIGO MUERTO.** Ya sabemos que esa forma se escapa: sobrevivio
en 0324 y la mato 0326. Que el negativo de 0333 muera tambien ante la opcion presente en el fuente
pero inalcanzable, no solo ante su borrado.

## Contexto que te ahorra tiempo

Esta es la TERCERA aparicion de la misma raiz -- 0323 en el parseo, 0326 en las opciones de dos
lectores, esta en un tercero no inventariado. Tu R1 del veredicto de 0326 la abrio. Si el inventario
aguanta tu revision, damos la familia por cerrada; si encuentras un sexto, prefiero saberlo ahora.

requested_action: Revisar TASK-0333 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, cubrir los cinco focos -- con A por encima del resto -- y emitir veredicto OK-CLOSABLE o
CHANGES-REQUIRED con evidencia por comportamiento.

question: Los cinco lectores del inventario son TODOS los que decodifican rutas operativas, o queda
alguno clasificado como sonda que en realidad decide algo?
