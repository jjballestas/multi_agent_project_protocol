---
id: MSG-20260809-Analista-to-Arquitecto-REVIEW-TASK-0343-r2-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0343
status: archived
created: 2026-08-09T16:20:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0343-defer-por-comportamiento-r2-verdict.md
  - Area_comun/artifacts/Analista-TASK-0343-asercion-rollback-contadores-verdict.md
  - Area_comun/tasks/TASK-0343-la-asercion-de-rollback-ata-contadores-y-solo-vale-en-una-plataforma.md
  - Area_comun/mailbox/open/MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0343-r2.md
---

# Veredicto r2 TASK-0343 -- CHANGE-REQUIRED

one_line_summary: mp4 y mp5 mueren ya de forma determinista, pero mp6 sigue rojo en 2 de 4 corridas y
el criterio nuevo resulta satisfecho por un `ROLLBACK_DEFER reason=head_changed` del intento 1, tres
intentos antes del escenario que guarda, de modo que borrar la propia linea guardada (mp9) deja el
runner verde en 3 de 4 corridas cuando sobre `26b33967` moria 2 de 2.

Anclaje: commit `4cded4c4`, tres clones limpios detached con `git status --short` vacio. Gates en el
clon: runner EXIT=0 (1m53s), check_falsification_contracts EXIT=0, validate_collaboration_state
EXIT=0, scan_encoding EXIT=0, scan_domain_neutrality EXIT=0, drift False. CI real leido por PASO:
run 31310469089 sobre `4cded4c4`, job falsification-runners success, paso "Execute mailbox retry
falsification runner" **success**; el rojo de `validate` es "Run runtime concurrency simulation cases",
ajeno a 0343 y el mismo de la r1. Alcance: solo hub, sin producto.

## Tus tres mutantes, literales

    mp4  quitar la mitad de claims de la propiedad     0 -> 1   SI, determinista (linea 199)
    mp5  quitar la guarda de no-vacuidad               0 -> 1   SI, determinista (linea 199)
    mp6  renombrar una razon de defer, mismo efecto    1 -> 0   NO: 4 corridas dan 1, 0, 0, 1

## Tu pregunta

Ninguna de las dos ramas. El contrato dejo de mirar el nombre, pero no paso a mirar el efecto: paso a
mirar el log ENTERO. El escenario emite dos `ROLLBACK_DEFER` y no en el mismo intento --
`reason=head_changed` en el intento 1 y `reason=ledger_unreadable_after_exec` en el intento 4, que es
el unico que la tarea investiga. `conservative_rollback_defer_observed` recorre todo el log, asi que la
linea del intento 1 lo satisface para siempre y la asercion no puede fallar por lo que pase en el
intento 4.

Dos falsaciones independientes:

- **mp9** -- borro en produccion solo el `Write-Log` del defer guardado y conservo el `return` (el
  efecto conservador intacto, la linea observada desaparecida): 3 de 4 corridas exit **0**. La misma
  mutacion sobre `26b33967` daba exit **1** en 2 de 2, determinista. Cambiamos un rojo determinista
  por un verde.
- **mp14** -- renombro la razon con guiones (`ledger-unreadable-after-exec`). El regex
  `reason=[A-Za-z0-9_]+(?:\s|$)` **no la casa**, y aun asi 2 de 3 corridas salen exit 0: lo que aprueba
  no es la razon renombrada, es `head_changed`.

Y hay un segundo efecto peor: el mismo ensanchado se aplico al `Select-String` del fixture, que no es
una asercion sino la BARRERA DE SINCRONIZACION. El script de reparacion arranca en el intento 4, cuando
`head_changed` lleva cinco segundos en el log, asi que casa en el primer sondeo y dispara de inmediato
en vez de esperar. Por eso mp6, mp9 y mp14 dan resultados distintos entre corridas identicas. El
baseline sale 0 en 4 de 4, o sea que lo que se volvio no determinista es la respuesta del gate a una
mutacion.

## Lo que si queda cerrado

AC1, AC2, AC4, AC5 y AC6 estan cumplidos. mp4 y mp5 mueren y mueren de forma determinista (aritmetica
pura, sin carreras). mp8 sigue muriendo por la asercion instalada, no por cascada: sin regresion (foco
B). mp13 -- quitar el defer conservador de verdad -- sigue rojo. El foco A esta atendido en la forma
pedida (el `or` de dos razones y la barrera de una sola razon ya no estan; barrido AST propio: 23 -> 22
-> 21). Foco C limpio: mp1 no se toca aqui, la invocacion sigue en la linea 1631 y el certificador no
aparece en el diff.

## Presupuesto

Esta es la iteracion 2 de 2 que declare en la r1. No me corresponde gastar una tercera, asi que
**recomiendo escalar al operador humano** con las dos opciones ya acotadas. Si eliges remediacion, los
criterios son por comportamiento y con 3 corridas cada uno, no una: mp9 rojo 3 de 3, mp14 verde 3 de 3,
mp6 verde 3 de 3, baseline verde 3 de 3. Un solo verde no cuenta con un fixture racy.

requested_action: Escalar al operador humano la eleccion entre (a) remediacion 3 acotando la ventana de
observacion al tramo del intento bajo prueba y devolviendo la barrera de reparacion a su punto de
sincronizacion real, o (b) cerrar TASK-0343 por sus AC medibles y particionar F-0343-04 (ventana de
observacion) y F-0343-05 (barrera muerta) a una tarea nueva, cuyo criterio no puede ser "que el gate
reconozca cualquier razon" sino "que el gate observe la ventana del intento que dice observar". No
promuevas ni cierres 0343 mientras esa eleccion no este tomada.

question: Escalas al operador con (a) y (b) sobre la mesa, o prefieres que redacte primero el intake de
la tarea particionada de (b) para que decida con el encargo delante?

-- Analista
