---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0353
status: open
created: 2026-08-10T06:12:35Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga TASK-0353 tras la remediacion 2 (salida A), en clon limpio y con exit codes reales.
question: La equivalencia entre la declaracion de produccion y el conjunto derivado cierra la clase, o queda un eje mas?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r2-tercera-ancla-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353-remediation-2.md
---

# REVIEW TASK-0353 r3 -- eligio la salida A y ato la declaracion a una derivacion

Escrito 08:12 local. **Ancla: `897b9767ce794b4df7a51256d0851330fe68fe64`**. Implementacion: `897b9767`.
**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Iteracion 2 de 2: la siguiente escala al operador.

## La forma de la solucion, que es lo que quiero que juzgues

Produccion mantiene una **declaracion** y el contrato la ata a una **derivacion**:

    orchestrator.py     SEMANTIC_REQUIRED_TURN_KEYS   (declaracion)
                        si el esquema de la raiz enrutada omite alguna -> ValueError ruidoso

    contrato            semantic_required_keys = required_keys - set(base_schema["required"])
                        assert semantic_required_keys == set(SEMANTIC_REQUIRED_TURN_KEYS)

El conjunto derivado sale **por comportamiento**: quitar cada clave de un turno valido y ver que
exige la validacion, menos lo que el esquema ya marca como `required` incondicional. Y se exige
**igualdad exacta**, no inclusion. Si manana una regla semantica exige una clave nueva y nadie la
declara, el contrato enrojece; si alguien declara una que no se exige, tambien.

Es la primera vez en esta cadena que un cierre ata **una declaracion a una derivacion** en vez de
ensanchar una forma. Por eso quiero tu lectura y no la mia.

## FOCO 1 -- ?cierra la clase, o queda un eje?

La pregunta no es si funciona hoy con `obstacles`. Es si la **igualdad exacta** es el predicado
correcto y si el conjunto derivado se obtiene de una fuente que no puede quedarse corta. Dos
hipotesis concretas que valen la pena atacar:

- El derivador quita claves **de nivel superior** de un turno valido. ?Que pasa con una exigencia
  semantica que no dependa de la presencia de una clave de nivel superior -- por ejemplo, sobre el
  contenido de una anidada? Si esa clase existe, la igualdad no la cubre y hay que declararlo.
- El turno base del que deriva: si es una copia del hub, ?ejerce las ramas condicionales que hacen
  aparecer las exigencias, o solo el camino feliz? Es el corolario de alcance que tu misma fijaste
  en TASK-0328: un corpus debe acreditar que entra por la rama que dice cubrir.

## FOCO 2 -- el diagnostico que dejo de mentir

La entrega afirma que la cadena falsa (`delivery turn is missing the obstacles block`) **se asierta
ausente** y que en su lugar sale:

    ValueError: routed schema omits top-level keys required by orchestrator semantic validation: obstacles

Compruebalo **por el proceso real**, como hiciste en la sonda C, no por la llamada directa. Y
verifica que la entrega ordinaria enrutada **sigue aceptandose**: un guard que revienta siempre no
es un guard.

## FOCO 3 -- el saldo, tercera vez que lo pido

El AC6 cayo **dos veces seguidas** por transcribir. Tu medida en `d2871436` fue **63/6/8** con
fallos {36, 43, 50, 53, 58, 59}. Si esta entrega declara otra cosa, exige la salida del replicador
pegada. Y confirma que ninguno de los seis restantes es nuevo.

## FOCO 4 -- R4

Quedaba pendiente completar la declaracion de la instantanea historica: **por que** se conserva, y
el matiz de que dos contratos si la leen como gemelo para OTRAS propiedades. Comprueba si esta.

## Residual

Sin CI real; la cuenta sigue bloqueada por decision del operador hasta cerrar la cascada en local.
Todo, lo tuyo incluido, es local. Declaralo.
