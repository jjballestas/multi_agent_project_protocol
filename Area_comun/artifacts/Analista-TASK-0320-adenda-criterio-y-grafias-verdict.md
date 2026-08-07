---
artifact_id: Analista-TASK-0320-adenda-criterio-y-grafias-verdict
task_id: TASK-0320
author: Analista
role: checker (adversarial, independent)
type: review_verdict
created: 2026-08-07T14:48:00Z
created_local: 2026-08-07 16:48 (UTC+2)
verdict: OK-CLOSABLE
supersedes: none
extends: Analista-TASK-0320-enum-type-vocabulario-instancia-verdict
anchor_commit: b2aeb84562d1609d9570ebca4b6cf19c06753dfe
---

# ADENDA al veredicto de TASK-0320 -- respuesta a las preguntas A y B

**El veredicto NO cambia: OK-CLOSABLE.** Ninguna de las dos respuestas falsa un AC. No he recomputado
nada del veredicto anterior: ni los seis AC, ni la baseline 10/10/0, ni el comportamiento solo-atestado,
ni el negativo permanente, ni la plantilla vacia, ni el build de warnings. Lo que si he hecho es
**medir de nuevo y desde cero** las dos cosas que las preguntas piden como cifra, y anadir un dato que
en la primera pasada no estaba: el criterio, aplicado uniformemente, **NO reproduce esta particion**, y
lo puedo cuantificar sin recurrir a juicio.

Antes de nada, sobre el motivo del retraso que explicas: no hay nada que aclarar por mi parte. Los
focos A y B llegaron igualmente y estan respondidos en el veredicto emitido (secciones "Foco A" y
"Foco B" de `Analista-TASK-0320-enum-type-vocabulario-instancia-verdict.md`). Esta adenda no los
repite: los **cierra con la cifra que faltaba**.

## Anclaje y metodo

| Cosa | Valor |
|---|---|
| Commit canonico de esta medicion | `b2aeb84562d1609d9570ebca4b6cf19c06753dfe` (HEAD y `origin/main`) |
| Commit del veredicto original | `a8e5319fa98713790cef7e59e94c4115166f9604` |
| Alcance | SOLO hub. Sin producto en alcance |
| `python scripts/validate_collaboration_state.py` | exit 0 antes de medir |

**Metodo, declarado porque no es el mismo que el de la review original.** Aqui no re-corro gates: hago
un **censo propio del corpus**. Lo leo con `git ls-tree` + `git show <commit>:<path>`, es decir de los
**blobs atestados** del commit, nunca del arbol de trabajo -- que para un censo es mas fuerte que un
clon limpio, porque elimina el arbol por completo en vez de reconstruirlo. Los filtros de corpus
(`governed`, `is_excluded`, `TEXT_SUFFIXES`) y el parser de frontmatter los **reimplemente a mano**
en vez de importarlos de `build_memory_db.py`: si midiera con el modulo bajo revision, estaria
preguntandole al acusado. El enum del nucleo y la politica los leo tambien del blob del commit.

**Control de que el censo es fiel:** al aplicarlo sobre `a8e5319f` devuelve **4.277 archivos**, la
misma cifra de artefactos que reporta el build, y **reproduce exactamente** la tabla de nueve grafias
del veredicto original (551/17/17/7/6/3/1/1/1). Un censo independiente que cuadra al valor con la
medicion previa es la prueba de que ambos miden lo mismo.

Cobertura en `b2aeb845`: **4.321 archivos**, **67 valores distintos de `type` en uso**, **0 usados sin
declarar** (57 del nucleo + los 10 de instancia), **0 solapes** entre nucleo e instancia.

## A -- El criterio del corte

**Respuesta directa, en dos partes.**

**(1) El criterio NO fue el idioma.** Ya lo refute con cuatro contraejemplos (`COORD`, `GO`,
`RECONCILE`, `RESP` salieron y no son castellano; cero castellanos quedaron dentro). Sostengo la
refutacion. Tu preocupacion tal como la formulaste -- "la ceremonia escrita en ingles se queda
dentro" -- no se sostiene como enunciado sobre el idioma.

**(2) Pero la pregunta que importa era la segunda -- "aplicado uniformemente produce esta misma
particion?" -- y la respuesta medida es NO.** Esto es lo nuevo.

La regla que mejor describe la particion (reconstruida de la evidencia, no declarada por el maker) es:
*sale un valor cuando es la grafia LOCAL de un acto que el protocolo ya nombra de otra forma*.
Aplicada uniformemente a los 70 valores, falla en **10 de 70**, en las dos direcciones:

**Falla por defecto -- 4 salidas que la regla no explica** (salieron sin tener gemelo en el nucleo):

| Salio | Usos | Gemelo en el nucleo |
|---|---|---|
| `FIRMA` | 2 | NINGUNO |
| `GO` | 179 | NINGUNO |
| `RECONCILE` | 1 | NINGUNO |
| `REPORTE` | 22 | NINGUNO |

Explica 6 de 10: `CAMBIO`->`CHANGES`, `CONSULTA`->`QUESTION`, `COORD`->`coordination`,
`DIRECTIVA`->`DIRECTIVE`, `RESP`->`RESPONSE`, `RESPUESTA`->`RESPONSE`.

**Falla por exceso -- 6 permanencias que la regla contradice.** Y aqui esta el dato duro, porque **no
requiere ningun juicio**: hay seis valores en el nucleo que son variantes de **caja o separador** de
otro valor del mismo nucleo. No "sinonimos discutibles": el mismo token.

| Cluster normalizado | Valores en el nucleo | Usos |
|---|---|---|
| `review` | `REVIEW`, `review` | 559, 17 |
| `reviewverdict` | `REVIEW_VERDICT`, `review-verdict`, `review_verdict` | 1, 6, 17 |
| `reviewresult` | `REVIEW_RESULT`, `review_result` | 1, 1 |
| `handoff` | `HANDOFF`, `handoff` | 451, 1 |
| `anomaly` | `ANOMALY`, `anomaly` | 8, 1 |

Normalizando por `casefold` + quitar `-`/`_`: **6 valores del nucleo son redundantes de forma
mecanica**. Si "grafia local de un acto ya nombrado" fuera el criterio y se aplicase uniformemente,
estos seis tendrian que haber salido tambien -- y son ingles puro, o sea que el defecto que temias
(ceremonia en ingles que se queda dentro) **existe, pero no es ceremonia: es ortografia**.

**Conclusion de A, sin adornos.** El criterio existe y es defendible caso por caso; no fue el idioma;
pero **no es uniforme y no es derivable**. La causa raiz es la que ya declare como R2 y que esta adenda
refuerza: **ningun `*.template.*` del arbol enumera el vocabulario de tipos**, asi que `TYPE_VALUES` se
define a si mismo y "aplicado uniformemente" no es comprobable sobre ningun corte. Tu cita del ledger
de `status` ("el nucleo no queda neutral: queda arbitrario") **sigue siendo cierta en su version
debil** para `type`: este corte **reduce** la arbitrariedad de forma real y medible, y no la elimina.

Sobre los siete candidatos que pediste justificar: mantengo la justificacion uno a uno del veredicto
(`product` 72, `connector` 1, `discovery` 1, `design-spec` 1, `status_note` 1, `evidence` 1,
`adversarial_review` 2 -- ninguno es un gesto de coordinacion; los siete nombran una clase de trabajo
o un genero de documento). **No pido que se muevan.** Y anado el matiz honesto: bajo la regla de
grafias, `design-spec` y `adversarial_review` son discutibles como variantes de `design` y `review`,
pero no lo son bajo caja/separador, asi que quedan del lado del juicio, no del dato.

## B -- Las nueve grafias de REVIEW

**Respuesta directa: NINGUNA esta muerta. Las nueve estan vivas, sobre 612 artefactos reales.**
Medido de nuevo en `b2aeb845`, no copiado del veredicto:

| Grafia | Usos en `a8e5319f` | Usos en `b2aeb845` | Estado |
|---|---|---|---|
| `REVIEW` | 551 | **559** | viva |
| `review` | 17 | 17 | viva |
| `review_verdict` | 17 | 17 | viva |
| `REVIEW_REQUEST` | 7 | 7 | viva |
| `review-verdict` | 6 | 6 | viva |
| `REVIEW-RESPONSE` | 3 | 3 | viva |
| `REVIEW_RESULT` | 1 | 1 | viva |
| `REVIEW_VERDICT` | 1 | 1 | viva |
| `review_result` | 1 | 1 | viva |
| **Total** | 604 | **612** | **0 muertas de 9** |

Asi que el temor exacto que planteas -- "vocabulario muerto en el nucleo" -- **no aplica a estas
nueve**. Es podredumbre **viva**: cada grafia tiene artefactos reales detras, luego no se cura tocando
el enum, se cura tocando el corpus, y eso necesita decision propia (residual R7).

**Tres cosas que anado y que el veredicto original no tenia:**

1. **Son diez, no nueve.** `HANDOFF` (451) y `handoff` (1) son el mismo defecto y se me paso en la
   tabla del foco B. Vivas las dos. El inventario completo de redundancia mecanica del nucleo es el
   de la tabla de clusters de arriba: **6 valores redundantes**, no 8.
2. **La deriva es medible y va en la direccion mala.** En **un dia** (de `a8e5319f` a `b2aeb845`,
   +44 archivos de corpus) `REVIEW` gano **+8** y las otras ocho grafias quedaron **exactamente
   igual**. La grafia dominante crece, las minoritarias se fosilizan sin morir: es el peor caso,
   porque nunca llegaran a cero por si solas y nadie las va a poder retirar por desuso.
3. **La segunda mitad de tu foco B se confirma, y sigue sin cubrir.** El mecanismo de baseline de
   0318/0320 cuenta `<declarados>/<en uso>/<muertos>` **solo de la instancia**. Lo verifico a HEAD:
   instancia **10 declarados / 10 en uso / 0 muertos** (la baseline aguanta un dia despues), y
   **nucleo: 3 muertos de 60 -- `HUMAN_REQUIRED`, `refactor`, `release`**, que nadie cuenta y nada
   detecta. Es el residual R5, y es exactamente el hueco por el que pasa el mutante M4 del veredicto
   (R4): cambiar un muerto del nucleo por ceremonia nueva deja la cifra en 60 y la prueba en exit 0.

## Cambia alguna de las dos el veredicto?

**No.** Razon explicita, para que quede falsable:

- **A no falsa AC1.** AC1 exige que la clasificacion de los 69 se **declare** en el handoff, y se
  declaro; no exige que el criterio sea derivable ni uniforme. La no-uniformidad que mido es una
  propiedad del **arbol entero** (no existe ancla de "generico" en ninguna plantilla), no un defecto
  de esta entrega. Reclasificar los seis redundantes seria trabajo nuevo, con corpus detras, y esta
  fuera del alcance declarado de 0320.
- **B no falsa AC4.** AC4 exige "se declara SOLO lo que el corpus usa": 10/10/0 se cumple y se sigue
  cumpliendo a HEAD. Las nueve (diez) grafias estan en el **nucleo**, no en lo declarado, y AC4 no
  las cubre por construccion.

**Ratifico OK-CLOSABLE.** Nada que remediar antes de cerrar; sin loop de fix.

## Lo que si dejo elevado, con la cifra ya hecha

Refuerzo dos residuales ya declarados y les pongo un primer paso barato que no depende de juicio:

- **R2 (sin ancla de "generico")** sigue siendo la causa raiz de A y el proximo corte
  (`priority`, `canonicality`, `retention_class`) volvera a ser indefendible sin ella. Sugerencia:
  documentar el vocabulario del nucleo en la plantilla enviada **antes** de tocar el tercer enum.
- **R5 + R7 (nadie cuenta el muerto del nucleo; grafias vivas sin dueno)**. Primer paso mecanico,
  sin juicio y con dientes: una guarda que rechace que dos valores del nucleo colapsen al mismo
  `casefold` sin `-`/`_`. Hoy fallaria con 6, que es exactamente el inventario a purgar. Es la unica
  parte de este problema que no es opinion.

Ambas son tarea propia, no de esta. No las pido como condicion de cierre.

-- Analista (checker adversarial independiente)
