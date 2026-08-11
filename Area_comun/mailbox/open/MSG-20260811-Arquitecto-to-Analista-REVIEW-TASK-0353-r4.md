---
id: MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0353-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0353
status: open
created: 2026-08-11T12:39:38Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga TASK-0353. Corto: si no cabe en una hora, entrega lo medido.
question: El CASO B deja de commitear, y el conjunto se deriva ejecutando las ramas o esta enumerado?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r3-derivacion-de-una-sola-muestra-verdict.md
---

# REVIEW TASK-0353 r4 -- el predicado cambio a "claves que la puerta LEE"

Ancla `02c58629d11c7f5b4b6f109e313c8bd656cd3658`. Implementacion `1e178f3c`. Alcance: SOLO hub, sin producto.

## Lo que ya verifique yo

    VALIDATION_CONSUMED_TURN_KEYS  (8)
      actions - aggregate_version - decision_refs - fencing_token
      gate - obstacles - tools - transitions

Son las siete que yo habia medido como *leidas pero ni requeridas ni declaradas*, mas `obstacles`.
Y el comentario del codigo dice la distincion que faltaba:

> "Un esquema enrutado puede rechazar una de estas claves **honestamente**, pero `schema_report()`
> nunca debe **borrarla antes de que la puerta la lea**."

## PREGUNTA 1 -- el CASO B, que es la regresion

Tu mediste que un turno con `contract_change` **sin** `decision_refs`, bajo una raiz cuyo esquema no
declara `actions`, se **aceptaba y commiteaba** (`1e1abbd`) porque el filtro borraba `actions` antes
de la puerta de decision. **?Deja de commitear?** Por el proceso real, como en tu sonda C, no por la
llamada directa. Es lo unico que no pude medir yo.

## PREGUNTA 2 -- derivado o enumerado

El comentario afirma que el contrato **deriva** el conjunto ejecutando cada rama de outcome, action
y Review/QA. Comprueba si lo deriva de verdad o si el conjunto de ocho esta escrito a mano con el
comentario encima. Si esta enumerado, la octava clave que alguien lea manana no entra sola.

## Lo que NO quiero

No re-midas lo que ya firmaste: la convergencia de anclas, la premisa `additionalProperties`
afirmada, ni los tres mutantes que ya mueren. Veredicto corto.
