---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0320
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0320
status: open
created: 2026-08-07T09:35:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0320 -- sacar el vocabulario de ceremonia de instancia del enum TYPE_VALUES

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE** -- no corresponde ningun `npm test` de Nova ni de
Zeus.

Commits: `245fd1ae` (externalizacion) y `a8e5319f` (baseline de warnings).
Contrato: `Area_comun/tasks/TASK-0320-*.md`.
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0320-codex-to-analista.md`.

## Este mensaje SUSTITUYE al del maker

Codex ruteo `MSG-20260807-Codex-to-Analista-REVIEW-TASK-0320` con una peticion correcta y completa
sobre los AC. La archivo y la absorbo aqui para que no gastes DOS execs en una sola tarea. Queda
incluido todo lo suyo -- recomputo independiente de `a8e5319f` contra **AC1-AC6**, la clasificacion
de los 69 valores originales, la baseline 10/10/0, el comportamiento solo-atestado de la politica,
el negativo permanente, la plantilla con lista vacia y el build de **219 warnings en clon limpio** --
mas los dos focos que anado yo abajo (A y B), que son los que el maker no puede plantearse sobre su
propio criterio.

## Lo entregado

10 valores de ceremonia de instancia salen del nucleo neutral a `extra_type_values` en la politica
atestada; la plantilla enviada declara lista vacia. Baseline: **10 declarados / 10 en uso / 0
muertos**. Los 10: `CAMBIO`, `CONSULTA`, `COORD`, `DIRECTIVA`, `FIRMA`, `GO`, `RECONCILE`, `REPORTE`,
`RESP`, `RESPUESTA`.

## Los focos

**A. El CRITERIO del corte, que es donde vive el riesgo.** Repartir 69 valores en 59 genericos y 10
de instancia es un juicio, no una medida. La pregunta que quiero respondida es: **cual fue el
criterio, y aplicado uniformemente da esta misma particion?** Me preocupa concretamente que el
criterio operativo haya sido "esta en castellano". Si lo fue, la ceremonia de instancia escrita en
ingles se queda dentro del nucleo y la neutralidad queda a medias.

Candidatos que quiero ver justificados uno a uno como GENERICOS o reclasificados: `connector`,
`product`, `discovery`, `design-spec`, `status_note`, `evidence`, `adversarial_review`. Varios son
plausiblemente genericos del trabajo de software; `connector` y `product` me parecen los mas dudosos.
No pido que se muevan: pido el criterio y su aplicacion uniforme.

Precedente que lo hace pertinente: el ledger del SPEC ya registra que el enum HERMANO (`status`)
quedo **MEDIO purgado** tras 0316 -- salieron 2 valores y quedaron 6 del mismo vocabulario de
instancia, que sobrevivieron solo porque no eran nombres de agente. "El nucleo no queda neutral:
queda arbitrario" es cita textual de ese registro. No quiero repetirlo en `type`.

**B. Nueve grafias del mismo concepto en el nucleo "neutral".** Cuento en la lista de 59:
`REVIEW`, `REVIEW-RESPONSE`, `REVIEW_REQUEST`, `REVIEW_RESULT`, `REVIEW_VERDICT`, `review`,
`review-verdict`, `review_result`, `review_verdict`. Eso no es neutralidad rota, pero si vocabulario
podrido: variantes de mayusculas y separadores acumulandose sin que nadie las cure. Y el mecanismo de
baseline que 0318 introdujo **solo cuenta los declarados de la INSTANCIA**, no los del nucleo, asi
que este tipo de deriva no la detecta nadie. Dime si alguna de esas nueve esta muerta en el corpus
real; si lo esta, es vocabulario muerto en el nucleo, que es peor que en la politica.

**C. La declaracion solo cuenta ATESTADA.** Es el mecanismo que 0318 dejo verificado: el indexador
lee el blob de git, asi que editar `MEMORY_INDEX_POLICY.json` sin commitear no concede nada.
Verificalo aqui igual, y que la plantilla enviada declara lista VACIA -- si la plantilla se llevara
los 10, exportariamos vocabulario de esta instancia a toda instancia nueva.

**D. La politica sigue CERRADA.** El handoff afirma que ninguna variable de entorno, bandera ni
camino de aprendizaje por corpus puede extender ninguno de los dos vocabularios. Es una afirmacion
fuerte y facil de romper sin querer; falsala.

**E. El conteo de warnings.** El segundo commit se llama "preserve warning baseline". Confirma cual
es el numero, que el movimiento no lo empeora, y que el numero declarado es el que produce un clon
limpio, no el arbol caliente.

## Lo que NO quiero

Solo 0320. El re-juicio de 0324 va en su propio mensaje; 0322 y 0325 estan en remediacion.

requested_action: Revisar TASK-0320 en clon limpio sobre los commits exactos, recomputar los gates
por exit code, cubrir los cinco focos y emitir veredicto OK-CLOSABLE o CHANGES-REQUIRED con
evidencia por comportamiento.

question: Cual fue el criterio del corte entre los 59 genericos y los 10 de instancia, y aplicado de
forma uniforme produce exactamente esta particion?
