---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0335-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0335
status: archived
created: 2026-08-08T02:30:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0335 -- dos regresiones CRUZADAS y dos inventarios

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commits: `e7eb3971` y la serie previa.

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py  ->  exit 0

## Lo que paso entre tu veredicto y este re-juicio

Tus dos puntos (igualdad exacta restaurada, AC7 con el numero medido) se hicieron enseguida. Pero al
correr el runner completo aparecieron **dos regresiones CRUZADAS**, ninguna de produccion:

**1. De TASK-0331.** Su admision fail-closed -- la que yo declare innegociable -- exige scope de
trabajo utilizable, y varios fixtures no lo declaraban.
**2. De TASK-0334.** Hizo que `Get-GitStatusPorcelainUtf8` llamara a `Get-EmbeddedRepositoryRoots` y
a `Invoke-GitStatusPorcelainUtf8`; las sondas enfocadas extraen la funcion externa **por nombre** y
no sus dependencias nuevas.

En los dos casos la produccion esta BIEN y lo obsoleto era el fixture o la sonda. Autorice absorber
las dos aqui, fixture-only, porque 0331 y 0334 estan en remediacion y reabrirlas seria peor.

**Y en los dos casos pedi INVENTARIO en vez de parche**, que es lo que funciono en 0333. Los dos
barridos cerraron su familia:

    familia 1  fixtures sin scope resoluble                     barrida y arreglada
    familia 2  sondas que extraen funciones sin sus dependencias barrida y arreglada

No aparecio una tercera, asi que la particion que tenia preparada no hizo falta.

## Los focos

**A. Los dos inventarios, verificados por ti.** Son el nucleo de esta vuelta. Que la lista de
fixtures con scope y la de sondas con dependencias esten **completas**, no que los casos que
fallaban esten arreglados. Si queda una sonda que extrae una funcion sin resolver sus dependencias,
la familia sigue abierta y volvera con el proximo refactor del harness.

**B. Que las dos regresiones cruzadas esten DECLARADAS**, no absorbidas en silencio. El radio de
impacto de la admision de 0331 y del descubrimiento de embebidos de 0334 es informacion que sus
propias reviews no cubrieron, y debe constar.

**C. Tus dos puntos originales.** Igualdad exacta restaurada -- verificaste tu que seguia verde -- y
AC7 con ocho rojos adicionales mas un endurecimiento preventivo.

**D. Produccion intacta.** Por diff. Ni 0331, ni 0334, ni el runner en su parte de produccion.

**E. AC8: el negativo del orden.** Ya confirmaste que se ejecuta y dejo de ser vacuo. Que no se haya
movido con los barridos.

## Nota

Es la iteracion 1 de las 2 que fijaste para esta ronda. Si algo queda abierto, escalas.

requested_action: Re-juzgar TASK-0335 en clon limpio sobre el commit exacto, verificar la
COMPLETITUD de los dos inventarios y no solo los casos reparados, comprobar que las dos regresiones
cruzadas estan declaradas, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Los dos inventarios estan COMPLETOS, o queda alguna sonda o fixture de la misma familia
sin declarar?
