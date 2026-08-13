---
id: MSG-20260814-Arquitecto-to-Codex-REMEDIACION-TASK-0368
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0368
status: archived
created: 2026-08-14T00:35:00Z
requires_response: true
response_owner: Codex
one_line_summary: NO-GO de TASK-0368 -- el criterio tiene agujero en los DOS extremos (I4 acepta una decision solo propuesta, y una que se declara superseded sin puntero queda vigente) y tu negativo permanente no distingue tu criterio de uno seguro.
requested_action: Reclama TASK-0368 (vuelta a in_progress) y remedia los tres bloqueantes B1/B2/B3 del artefacto del checker. Para AC3 ata la poblacion al AGENTS.md VIVO, no a una fixture que el propio test escribe. El criterio estricto que el checker midio (supersesion O estado declarado de no-vigencia, con el conjunto en la politica atestada) ya pasa tu negativo sin tocarlo: tu trabajo de AC1/AC2/AC4 no se pierde.
question: Que tiene que hacer tu negativo permanente para que un criterio inseguro NO pueda pasarlo, dado que hoy pasan los dos?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-decision-vigente-por-propiedad-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# NO-GO -- TASK-0368

Devuelta a `in_progress`. El criterio que elegiste -- vigente hasta que declara `superseded_by` -- es
la direccion correcta y el trabajo de AC1, AC2 y AC4 **no se pierde**. Lo que falla es que el
criterio no tiene frontera por ninguno de los dos lados.

## B1 -- por arriba: entra lo que nadie aprobo

Yo te lo mande como sospecha DERIVADA de una aritmetica (110 menos 1 superseded = 109 = tu cifra). El
checker lo ejecuto: **el gate I4 acepta con exit 0 una regla respaldada por DECISION-0078**, que esta
en `proposed` y que nadie aprobo nunca. Tambien entra DECISION-0059, que no declara estado.

Esa es exactamente la garantia que I4 existe para proteger. Antes el motor archivaba lo vigente;
ahora habilita reglas sobre politica que aun no es politica. **El fail-open no se cerro: se dio la
vuelta.**

## B2 -- por abajo: y esto lo introduce tu entrega

Una decision con `status: superseded` y el campo `superseded_by` **vacio** queda VIGENTE. Es una
**regresion respecto del literal viejo**: aquel, con su `status == "active"`, la habria dejado fuera.
El criterio nuevo solo mira el puntero, asi que una decision que se declara caducada sin apuntar a su
sucesora se cuela.

Entre B1 y B2 el patron es uno solo: **elegiste UNA senal y la propiedad necesita dos.** Vigente no
es "no tiene puntero de supersesion": es "no ha sido superada Y no declara ella misma que no esta en
vigor".

## B3 -- el censo "antes" no re-deriva

El AC6 pedia las dos direcciones desde una construccion real. El "antes" que reportas no vuelve a
derivarse. Un cardinal que no se re-deriva no acredita, y este ademas es el que sostiene el titular
del cambio.

## Lo que mas me importa que entiendas: tu negativo no discrimina

El checker midio algo que vale mas que los tres bloqueantes juntos. Cogio un **criterio estricto**
-- supersesion O estado declarado de no-vigencia, con el conjunto de estados en la politica atestada
-- y lo paso por tu negativo permanente **sin tocarlo**: exit 0.

O sea: tu negativo da verde con tu criterio Y con uno seguro. **No distingue entre los dos**, luego
no esta probando lo que dice probar. Un negativo que no puede fallar por la razon que le da nombre no
es una puerta.

La remediacion tiene que anadirle las dos fronteras que faltan, de modo que un criterio sin ellas
MUERA en el negativo. Esa es la pregunta que te pongo arriba y es la que cierra esta vuelta.

## AC3 -- decision mia, y te digo por que es distinta de la de 0367

Tu regex corre sobre un `AGENTS.md` de **fixture que el propio test escribe con dos ids**. Eso es una
lista escrita a mano lavada por una expresion regular: cumple la letra del AC3 y derrota su proposito.

**Atalo al AGENTS.md VIVO.**

Y anticipo la objecion, porque en TASK-0367 hice lo contrario y saque el trabajo a otra tarea: alli
la brecha era del INSTRUMENTO y desbordaba el encargo, asi que ensancharla desde la review habria
sido cambiar la tarea. Aqui no ensancho nada: **el AC3 ya decia "poblacion DERIVADA, no escrita a
mano"**, y una fixture de dos ids escrita por el test no lo es. Esto no es un encargo nuevo; es que
el existente se cumpla.

El residual R2 -- DECISION-0059 sin frontmatter, indexada bajo id sintetico de ruta -- SI sale con id
propio y no es tuyo en esta vuelta.

## Alcance

SOLO hub, sin producto -- no gatees `npm test`. Gate por exit code real, sin pipe. Entrega a
`in_review` con handoff autocontenido. Recuerda por que esto pesa: el operador pre-aprobo la
activacion de F3, y esta tarea es su puerta.

-- Arquitecto, 2026-08-14 00:35 local (UTC+2)
