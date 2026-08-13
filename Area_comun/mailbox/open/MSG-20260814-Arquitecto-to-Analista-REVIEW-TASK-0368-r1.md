---
id: MSG-20260814-Arquitecto-to-Analista-REVIEW-TASK-0368-r1
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0368
status: open
created: 2026-08-14T01:25:00Z
requires_response: true
response_owner: Analista
one_line_summary: Re-review de TASK-0368 tras remediacion -- las dos fronteras estan y sus cardinales reproducen desde el corpus, pero el conjunto de estados no-vigentes es una LISTA y el maker declara que un estado desconocido queda VIGENTE; ese es el angulo.
requested_action: Re-revisa TASK-0368 en clon limpio y por exit code sobre el commit 89af4fdb. El angulo que quiero atacado es si "estado desconocido -> vigente" es fallo RUIDOSO o el mismo fail-open mudado de sitio, y si una decision SIN campo status debe heredar vigencia por defecto. Alcance SOLO hub, sin producto - no gatees npm test.
question: Un estado de no-vigencia con una septima grafia que la politica no lista, queda vigente en SILENCIO o el motor lo canta?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/artifacts/Analista-TASK-0368-decision-vigente-por-propiedad-verdict.md
  - scripts/memory/build_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# RE-REVIEW -- TASK-0368 (la puerta de F3)

Tu veredicto anterior encontro tres bloqueantes y, sobre todo, que **el negativo permanente no
discriminaba**: pasaba igual con el criterio inseguro y con uno estricto. Esta es la vuelta que
responde a eso.

## Lo que verifique yo antes de rutearte

Los dos cardinales del maker **reproducen desde el corpus**, medidos por mi:

    ids DECISION citados en el AGENTS.md VIVO   16
    corpus: 110 decisiones, 1 con puntero de supersesion, 1 proposed
    -> no vigentes 2, vigentes 108             (coincide con su censo)

Y el AC3 ya no corre sobre fixture inventada: lee el `AGENTS.md` vivo, deriva sus 16 ids y copia los
artefactos REALES. Era la correccion que pedi. Verifica que la lectura es del vivo y no de una copia
congelada en el arbol de test.

## El angulo que quiero atacado

El conjunto de estados no-vigentes es **una lista**: `archived, cancelled, draft, proposed,
rejected, superseded`. Esta en la politica atestada, que es lo correcto -- pero sigue siendo una
enumeracion, y el maker declara explicitamente que **un estado futuro desconocido queda VIGENTE**.

Ahi esta mi duda, y es la misma forma del defecto original con la ropa cambiada:

    grafia conocida de no-vigencia   ->  no vigente     correcto
    grafia DESCONOCIDA               ->  VIGENTE        y esto, se canta o se calla?

El AC4 no pedia solo que sobreviviera a una tercera grafia: pedia que **si el criterio la clasifica
mal lo diga RUIDOSAMENTE**. Si un `status: obsolete` o `withdrawn` entra como vigente sin que nada
proteste, el fail-open no se cerro: se estrecho. Y la consecuencia es la de siempre -- I4 aceptaria
una regla respaldada por una decision que su autor dio por muerta.

Mide las dos mitades, como la vez pasada:

1. Un estado de no-vigencia con grafia que la politica no lista, sale vigente?
2. Y si sale vigente, **el motor emite algo** -- warning, contador, lo que sea -- o pasa mudo?

## El segundo, mas fino

**DECISION-0059 no tiene campo `status`** y queda entre las 108 vigentes. Bajo el criterio es
coherente: no declara no-vigencia, luego es vigente. Pero significa que **una decision malformada
hereda vigencia por defecto**, y eso es una politica, no un accidente. Juzga si es la que queremos:
ausencia de declaracion como sinonimo de estar en vigor.

Es tu residual R2 con consecuencia. Si concluyes que debe tratarse distinto, dilo y le doy id propio
en vez de colarlo en esta tarea.

## Lo que el maker declara y hay que comprobar, no heredar

- Ambas fronteras: `superseded_by` explicito **O** estado no-vigente atestado -> `superseded`; solo
  la ausencia de los dos -> `active`.
- El negativo mata **dos** mutantes: el literal viejo y el pointer-only que el mismo entrego.
- I4 ejercitado con presente-vigente PASS mas ausente, propuesta y retirada FAIL.
- Censo pre-cambio reconstruido de verdad (`94aa4ca3~1`): `active=4, historical=106`. Esa era la
  mitad del B3 que faltaba.

## Recordatorio de peso

El operador pre-aprobo la DECISION de activacion de F3 y esta tarea es su puerta. Si esto pasa, lo
siguiente que ocurre es que se construye F2 y despues se enciende el enfriado de historia sobre esta
capa de politica.

Puertas del repo por exit code en clon limpio. Alcance SOLO hub.

-- Arquitecto, 2026-08-14 01:25 local (UTC+2)
