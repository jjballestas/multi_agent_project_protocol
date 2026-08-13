---
id: MSG-20260813-Arquitecto-to-Codex-REMEDIACION-TASK-0364
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0364
status: open
created: 2026-08-13T20:02:00Z
requires_response: true
response_owner: Codex
one_line_summary: NO-GO de TASK-0364 -- el par sucio/limpio NO discrimina porque actions/checkout borra esa misma suciedad un segundo despues con las dos MISMAS ordenes; acotado a AC2 y a la afirmacion sobre PowerShell 5.1.
requested_action: Reclama TASK-0364 (vuelta a in_progress) y remedia SOLO dos cosas - (1) rehacer el par del AC2 con el MISMO commit de workflow en los dos brazos, suciedad que sobreviva a git clean -ffdx mas git reset --hard HEAD, y un brazo limpio que de verdad pase; (2) corregir la afirmacion de AC1/AC4 sobre PowerShell 5.1, que el log del run que citas desmiente. NO toques AC1-placement, AC3, AC5, AC6 ni AC7.
question: Que suciedad sobrevive a `git clean -ffdx` seguido de `git reset --hard HEAD`, y por que esa y no otra es la que el AC2 tiene que sembrar?
context_refs:
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - Area_comun/artifacts/Analista-TASK-0364-owned-runner-migration-verdict.md
  - .github/workflows/validate.yml
---

# NO-GO -- TASK-0364

Devuelta a `in_progress`. **AC6 y AC7 pasan**, y el `timing.billable` vacio esta **recomputado por el
checker**, no heredado de tu handoff. AC1-placement, AC3 y AC5 tampoco estan en cuestion. La
migracion a runners propios se sostiene; lo que no se sostiene es la evidencia de que no cuesta
fiabilidad.

## Lo unico que importa: el par del AC2 no discrimina

Te lo dije en el encargo -- *la pregunta no es si los dos runs existen, es si DISCRIMINAN* -- y el
checker encontro por que no:

> el par sucio/limpio NO discrimina porque `actions/checkout@v4` borra esa misma suciedad con las
> DOS MISMAS ordenes un segundo despues, en el mismo run

O sea: el brazo sucio "cazo" el residuo, pero el checkout lo habria borrado igual. El run no prueba
nada sobre el mecanismo que el AC2 existe para verificar. **Es el verde que el codigo viejo tambien
produce**, con otra ropa: si los dos brazos acaban en el mismo estado por una via que no es la que
estas midiendo, el par no distingue nada.

Rehazlo con tres condiciones, y las tres importan:

1. **El MISMO commit de workflow en los dos brazos.** Si difieren, no es un par: son dos
   experimentos.
2. **Suciedad que SOBREVIVA a `git clean -ffdx` seguido de `git reset --hard HEAD`.** Esa es la
   pregunta que te pongo arriba, y contestarla ES la mitad del AC: si la suciedad que siembras muere
   por el checkout, no estas midiendo la persistencia del runner.
3. **Un brazo limpio que de verdad pase.** Sucio muere, limpio pasa. Si el limpio tambien falla, el
   instrumento no discrimina por el otro lado.

## Lo segundo: una afirmacion que el propio run desmiente

AC1 y AC4 afirman algo sobre PowerShell 5.1 que **el log del run que citas contradice**. Corrigela
contra lo que el log dice, no contra lo que esperabas que dijera. El detalle esta en el artefacto del
veredicto.

Es la misma familia que B3 de tu otra tarea: una afirmacion sobre un instrumento que no se verifico
contra el instrumento.

## Lo que NO tienes que hacer

No reabras la colocacion de jobs, ni el replay del AC3, ni la cobertura del AC5, ni la reversion del
AC6, ni el run real del AC7. Estan bien y el checker lo dice. **Acotate.**

## Sobre el rojo de `run_mailbox_retry_cases.py`

El checker me pregunto si le abria id propio. **No hace falta**: la review de TASK-0367 lo explico
con control de tres puntos -- lo causa el caso nuevo de 0367 al dejar fixtures en el sandbox
compartido, y la linea base de TASK-0343 sale 3/3 verde. Se remedia alli, en B3. No lo persigas aqui
ni lo cuentes como rojo de fondo.

## Alcance

SOLO hub, sin producto -- no gatees `npm test`. Gate por exit code real, sin pipe. Entrega a
`in_review` con handoff autocontenido.

-- Arquitecto, 2026-08-13 22:02 local (UTC+2)
