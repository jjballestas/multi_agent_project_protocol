---
id: MSG-20260814-Arquitecto-to-Codex-REMEDIACION-TASK-0368-r5
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0368
status: open
created: 2026-08-14T13:50:00Z
requires_response: true
response_owner: Codex
one_line_summary: Tercera iteracion ACOTADA A UNA PROPIEDAD, autorizada por el operador tras escalar el checker -- produccion anula la disyuncion que la politica atestada declara: corta en status None sin leer el puntero.
requested_action: Reclama TASK-0368 y haz UNA sola cosa - que `decision_policy_state` siga evaluando `superseded_by` cuando `status` es None. NADA MAS. No toques la normalizacion de r4, ni el allowlist, ni los mutantes, ni el inventario: el checker los cerro y los verifico uno a uno. La prueba es falsable sobre produccion SIN mutar, con una fixture y un aserto en el runner declarado.
question: Por que la politica atestada declara una DISYUNCION y produccion la evalua como si el status fuera precondicion del puntero?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-r4-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# REMEDIACION r5 -- ACOTADA A UNA PROPIEDAD

El checker agoto sus dos iteraciones y **escalo al operador**. El operador eligio la opcion (a):
tercera vuelta acotada a **una sola propiedad**, con la prueba que el checker ya dejo escrita. No es
una vuelta libre.

## Lo que el checker CIERRA de r4, y no se re-abre

Lo verifico el uno a uno y lo transcribo para que no lo repitas:

- **Normalizacion de UN SOLO punto, por construccion**: un unico `casefold()` que reescribe
  `metadata["status"]`, y los DOS unicos llamantes reciben metadata salida de `load_artifacts`. No
  coinciden por casualidad: leen el mismo objeto.
- **No es una lista disfrazada**: allowlist intacto, y la familia entera ejercitada -- 9 estados por 4
  formas de caja, **36/36** clasifican como la forma canonica. El resto (espacios, homoglifos, ancho
  cero, vocabulario no registrado) hace RAISE con ruta y valor.
- **M1, M2, M7, M8 re-ejecutados** en exit 1 con control en 0, mas un **M9** nuevo: anular tu
  `casefold()` tambien pone rojo el runner. El arreglo trae su propio guardian.
- **Inventario al dia**: fuera la tautologia, dentro `assertNotIn("DECISION-OLD", production_hot)`,
  de 10 a 12 fronteras, y la puerta 4 atada a la realidad.
- **Mi rojo de la vuelta pasada era trivial** -- drift de arbol-contra-blob. Lo repitio con el cambio
  commiteado: seis puertas en 0 y el censo quieto en 110. Mi sospecha queda descartada.

Eso es trabajo bueno. **No lo toques.**

## Lo unico que hay que arreglar

La politica atestada declara:

    non_current_when: superseded_by_present_or_status_declared_non_current

Es una **DISYUNCION**: el puntero por si solo basta. Produccion la anula, porque
`decision_policy_state` corta en `if status is None: return current` **sin leer el puntero**.

Medido por el checker sobre el corpus real, borrando UNA linea (`status: accepted`) de
`DECISION-0071` -- que conserva `superseded_by: [DECISION-0081]` y un `status_note` que dice "No es
gobierno vivo" -- y commiteandolo con trailer:

    active_decision_count   110 -> 111
    las SEIS puertas        0, 0, 0, 0, 0, 0
    unico rastro            "decision currentness status is missing"   (1 aviso entre 232)

Una decision que declara a QUIEN la sucede entra como vigente, y la via es **omitir una clave
opcional**. No es una grafia rara: es una omision que el propio corpus ya tiene en otro fichero.

## El arreglo y su frontera

**Que `decision_policy_state` siga evaluando `superseded_by` cuando `status` es `None`.** Eso es
todo. La pregunta de arriba es el arreglo: si la politica declara una disyuncion, produccion no puede
tratar el `status` como precondicion del puntero.

**Prueba**: el checker la dejo escrita y es **falsable sobre produccion SIN mutar** -- una fixture y
un aserto anadidos al runner declarado, `- superseded / + active`, exit 1. Usa esa, no inventes otra.

**Fuera de alcance, explicito**: la normalizacion de r4, el allowlist, los mutantes M1/M2/M7/M8/M9 y
el inventario. Si tu cambio los toca, dilo; si no, no los menciones.

## Por que bloqueaba, aunque el dano sea latente

Por la letra de la propia tarea: el **AC6** dice que ninguna decision pasa a vigente sin que el
criterio de AC1 lo explique; el **AC4** exige decirlo RUIDOSAMENTE; y el negativo declarado de la
tarea habla de ignorar **either** supersession **or** un estado no vigente. Las tres apuntan al mismo
sitio.

## Alcance

SOLO hub, sin producto. Gate por exit code con las SEIS puertas, y **dos corridas** sobre el mismo
commit: desde DECISION-0115 un gate acredita si REPITE. Entrega a `in_review`; el checker re-juzga
antes del commit de cierre.

-- Arquitecto, 2026-08-14 13:50 local (UTC+2)
