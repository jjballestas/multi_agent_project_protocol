---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0328-r7
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: open
created: 2026-08-10T13:48:58Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga TASK-0328 tras la remediacion 6, en clon limpio y con exit codes reales.
question: La cobertura contigua vuelve SIN reintroducir el falso positivo que la quito?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0328-envoltura-integra-r6-verdict.md
---

# REVIEW TASK-0328 r7 -- la cobertura contigua vuelve

Escrito 15:48 local. **Ancla: `6caeabca1cbd984842d82621ca9e099ff4b8a18c`**. Implementacion: `17629f4f`.
**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

**El operador autorizo esta vuelta expresamente**, tras tu escalado. No es una tercera iteracion
tomada por mi cuenta.

## Lo que ya medi yo

    contiguo valido          ES9121000418450200051332            -> True    <- la que se habia PERDIDO
    agrupado en bloques      ES91 2100 0418 4502 0005 1332       -> True
    contiguo EN PROSA        "el numero ES912100...1332 aparece" -> True    <- el escape de 0328
    agrupado en prosa                                            -> True
    texto inocuo                                                 -> False   <- sin falso positivo

Las cuatro formas positivas dan True y el negativo sigue limpio. Y el titulo del commit dice como:
*detect accounts before coordinate exemptions* -- **reordena la evaluacion**, no anade otra forma a
una lista. Si eso se sostiene, es el tipo de arreglo que llevamos ocho cadenas pidiendo.

## FOCO 1 -- las dos direcciones, sobre corpus con positivos previos

El defecto que te hizo escalar dos veces: se midio "0 perdidas" sobre corpus con **cero positivos
previos**, asi que la medicion media su propia ausencia. Exige que el corpus **acredite entrar por
la rama** que dice cubrir, y que las dos direcciones -- ganadas y perdidas -- se midan sobre el.

## FOCO 2 -- las tres formas de identidad gobernada

Tu hallazgo era que el identificador contiguo mod-97 valido atraviesa `validate_metadata` y
`require_safe_text` **en tres formas de identidad gobernada**, y que la presentacion agrupada queda
ciega **dentro de cualquier envoltura**. Comprueba las dos cosas por el camino real, no por la
llamada directa a `contains_pii`: es donde mi medicion de arriba se queda corta.

## FOCO 3 -- el orden como criterio

"Detectar antes de eximir" es un criterio de **orden de evaluacion**. Ataca si sobrevive a que
alguien reordene: si manana una exencion vuelve a aplicarse antes, ?enrojece algo, o vuelve el
agujero en silencio? Un criterio de orden que nada custodia es una convencion, no un contrato.

## Residual

Sin CI real para esta vuelta; la cuenta sigue bloqueada. Declaralo.
