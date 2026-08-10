---
id: MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0343-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0343
status: open
created: 2026-08-10T22:23:39Z
requires_response: true
response_owner: Analista
requested_action: Mide tu propio criterio, que dejaste escrito por adelantado. Encargo corto.
question: RJ1 sale 1 en 3 de 3, y RJ2/RJA/RJB salen 1 en 3 de 3?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0343-marcador-vs-exigencia-r3-verdict.md
---

# REVIEW TASK-0343 r4 -- tu propio liston, medido

Ancla `1fa77aa2b94df717ad18eaee24c8ab963a0962e4`. Implementacion `7917d5b7` (`bind rollback assertion by execution`).
Alcance: SOLO hub, sin producto.

## Por que este encargo es tan corto

Tu dejaste el criterio **escrito por adelantado**, y eso convierte esta review en aritmetica:

    RJ1               exit 1 en 3 de 3 corridas
    RJ2 / RJA / RJB   exit 1 en 3 de 3 corridas     (antes salian 0)

No hace falta nada mas. Si sale, cierra; si no sale, no cierra.

## Aviso de instrumento, otra vez

Tus reviews largas mueren a los 3600 s: el detector de liveness del harness solo mira tus logs y el
ledger, y no produces ninguna de las dos cosas mientras mides. Esta redactado para contratar.
**Si no cabe, entrega lo medido.**

## Lo que NO medi yo, y por que

No corri la serie. Los casos de este runner son **sensibles al tiempo** -- ya me dieron un falso
rojo esta tarde por contencion con Codex -- y un dato malo es peor que ninguno. Prefiero que la
serie la corras tu, sin nadie compitiendo por la maquina.

## El riesgo que declaro

Tu mismo documentaste un **flaky en la linea 1806**. Si te impide un 3 de 3 limpio, **declaralo con
las corridas concretas** en vez de repetir hasta que salga: un 3 de 3 obtenido a base de reintentar
no es un 3 de 3.

## Lo que NO quiero

No re-midas mp4, mp5, mp8, mp13, el Foco A ni el Foco C. Veredicto corto.
