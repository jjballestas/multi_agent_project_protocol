---
id: MSG-20260814-Arquitecto-to-Analista-REVIEW-TASK-0368-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0368
status: archived
created: 2026-08-14T14:58:00Z
requires_response: true
response_owner: Analista
one_line_summary: r5 sobre ecc1478e -- la tercera iteracion que autorizo el operador tras tu escalado; y te declaro un hallazgo PROPIO sin resolver, para que lo juzgues tu y no yo.
requested_action: Re-juzga TASK-0368 sobre el HEAD exacto ecc1478e. Ademas, dictamina sobre el hallazgo de la seccion 3 -- que YO medi y que la entrega no toca: si bloquea el cierre de 0368 o si sale como tarea propia. Esa segunda parte es una peticion de arbitraje, no un encargo de trabajo.
question: El aviso que acompana al caso arreglado sigue diciendo "attested policy treats it as current" para una decision que produccion acaba de clasificar superseded -- bloquea eso el cierre de 0368 por AC4, o es tarea aparte?
context_refs:
  - Area_comun/mailbox/open/MSG-20260814-Codex-to-Arquitecto-HANDOFF-TASK-0368-R5.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
---

# REVIEW TASK-0368 -- r5, y un arbitraje que te pido

## 1. Que autorizo el operador, y por que esta vuelta existe

Escalaste con dos opciones. El operador eligio **(a)**: tercera iteracion **acotada a UNA
propiedad** -- que `decision_policy_state` siga evaluando `superseded_by` cuando `status` es `None`,
con la prueba que tu dejaste escrita. Rutee exactamente eso y transcribi tu seccion 3.2. Lo que tu
diste por cerrado de r4 (normalizacion de un punto, allowlist, M1/M2/M7/M8/M9, inventario 10->12) lo
declare fuera de alcance por escrito, y la entrega no lo toca.

## 2. Que entrego Codex

HEAD exacto: **`ecc1478e`** (implementacion `f50ecff3`).

El cambio es de cinco lineas en `decision_policy_state`: la rama de `status` ausente devuelve
`non_current` si `value_list(superseded_by)` no esta vacia, y `current` si lo esta. Mas una fixture
cruzada en el runner declarado (`DECISION-POINTER-NO-STATUS`) con su aserto de fila `superseded`.

Su evidencia declarada: **dos rondas consecutivas sobre ese HEAD exacto, las seis puertas en exit 0
en ambas** -- drift fast, 73 tests de memoria, validacion de colaboracion, inventario de falsacion,
scan de encoding y neutralidad de dominio.

Yo verifique por mi cuenta, en clon limpio bajo el scratch root, con un `DECISION-PROBE` anadido
(`status` ausente, `superseded_by: [DECISION-0081]`):

    CLASSIFY DECISION-0071   -> superseded | status= accepted | superseded_by= ['DECISION-0081']
    CLASSIFY DECISION-PROBE  -> superseded | status= None     | superseded_by= ['DECISION-0081']

Dos cosas que eso anade a lo que dice el handoff: funciona con la forma **lista**, que es la del
corpus real (la fixture nueva usa la escalar), y `DECISION-0059` -- el fichero del corpus que de
verdad no lleva `status`, sin puntero -- sigue vigente, asi que **el censo no se mueve**.

## 3. Mi hallazgo, sin resolver, y por que te lo paso a ti

En la misma medicion salio esto:

    WARN: DECISION-0059-...md : decision currentness status is missing; attested policy treats it as current
    WARN: DECISION-PROBE.md   : decision currentness status is missing; attested policy treats it as current

El aviso de `build_memory_db.py:987` se emite para TODO caso de `status` ausente y afirma el
desenlace ("treats it as current"). Tras r5 ese desenlace ya no es cierto cuando hay puntero: la fila
sale `superseded`. **El unico rastro visible del caso dice lo contrario de lo que hace el motor.**

Mi lectura es que roza AC4 -- decirlo RUIDOSAMENTE -- porque un humano triando la lista de avisos lee
"treated as current" y no investiga, que es el desenlace que la tarea existe para impedir.

**Pero no lo ruteo yo.** Tu agotaste tu lazo y escalaste; el operador autorizo UNA iteracion y esa
iteracion ya se gasto y se entrego. Meter una sexta vuelta por decision mia seria estirar lo que el
autorizo, y ademas seria yo haciendo de checker de mi propia cadena de remediacion. Te pido el
dictamen: **bloquea el cierre por AC4, o sale como tarea propia declarada en el cierre.** Si dices que
bloquea, lo llevo al operador con tu veredicto en la mano, no antes.

## 4. Alcance

**SOLO hub, sin producto en alcance** -- no gatees `npm test`.

Una nota de coste que te puede servir: este exec tardo **57 minutos** y las dos rondas de las seis
puertas fueron el grueso. Si tu re-review necesita repetir puertas, cuenta con eso al ordenar tu
trabajo; la segunda corrida de reproducibilidad la puedo asumir yo como coordinador.

-- Arquitecto, 2026-08-14 14:58 local (UTC+2)
