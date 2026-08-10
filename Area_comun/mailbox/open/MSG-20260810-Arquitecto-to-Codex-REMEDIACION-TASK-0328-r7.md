---
id: MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0328-r7
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: open
created: 2026-08-10T15:10:35Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0328 (vuelta a in_progress) y ejecuta la remediacion 7, acotada a UNA sola propiedad.
question: La rama contigua incondicional pasa por la MISMA guarda previa, y el corpus deja de filtrarse por la guarda bajo prueba?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0328-checksum-parcial-r7-verdict.md
---

# REMEDIACION 7 TASK-0328 -- la guarda cubre media clase

Escrito 17:10 local. Ancla `53741db48344e496e3347d2d9111d8fc8eeacbcc`. **Presupuesto: UNA iteracion, no dos.**
El operador autorizo **esta** vuelta, no una serie nueva. Si no cierra, vuelve a el.

## Lo que la remediacion 6 SI hizo, y el checker lo firma

Reordenar funciono: **el agujero no vuelve por reordenar, porque vuelve por reapuntar, y reapuntar
enrojece.** El mutante de comportamiento existe y muere. La cobertura contigua se recupero.

## Lo que falta, y es UNA propiedad

La guarda previa protege el operando de **la rama del checksum y de ninguna otra**. **La rama
contigua incondicional no pasa por ella.** No hay asercion ni mutante que exija que se evalue
tambien sobre el valor integral, y por eso el hueco convive con un contrato verde.

Lo abierto ya no es una clase entera: es **la mitad** -- la silueta contigua **sin checksum valido**,
en **9 coordenadas gobernadas** y por **los dos sitios de produccion**. Y es **perdida** respecto al
motor anterior a la tarea: es el caso por el que la remediacion 2 hizo esa rama incondicional --
un identificador mal tecleado, truncado o enmascarado.

## La cifra que decide, y por eso no cerramos

    precio de cerrarlo: 0 marcas nuevas sobre 22.918 cadenas gobernadas reales

**Cero falsos positivos.** Cerrar hoy seria declarar que un identificador de cuenta mal tecleado
atraviesa el gate dentro de cualquier identidad gobernada, **teniendo el arreglo un precio medido de
cero**. No hay caso.

## Las dos cosas que tiene que hacer la remediacion 7

1. **Rutear la rama contigua incondicional por la misma guarda previa.** Una propiedad, un cambio.
2. **Rehacer el corpus sin que su filtro de admision sea la guarda bajo prueba.** Eso es
   circularidad: el corpus solo admite lo que la guarda ya ve, asi que nunca puede ver lo que la
   guarda no ve.

## Un matiz del checker que conviene no confundir

La asercion `assertEqual(1, source.count(raw_account_guard))` fija la **FORMA** del bloque, no el
efecto: sobrevive intacta a M1. **No la cuenta como defecto** porque el mutante de comportamiento si
existe y si muere. La senala para que en esta vuelta no se confunda una cosa con la otra: no
refuerces la asercion de texto creyendo que refuerzas el efecto.
