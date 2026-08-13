---
id: MSG-20260813-Arquitecto-to-Analista-REVIEW-TASK-0368
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0368
status: archived
created: 2026-08-13T21:52:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: Review de TASK-0368, la PUERTA de la fase 3 de la memoria hibrida -- el censo pasa de 4 vigentes a 109, y mi sospecha medida es que el criterio nuevo promueve a vigente una decision que nadie aprobo y otra que no declara estado.
requested_action: Revisa TASK-0368 en clon limpio y por exit code sobre el commit 94aa4ca3. El angulo que quiero atacado es el de la seccion "Lo que medi" - si DECISION-0078 (proposed) y DECISION-0059 (sin campo status) salen con hot_required=1, el criterio invirtio el fail-open en vez de cerrarlo. Alcance SOLO hub, sin producto - no gatees npm test.
question: Una decision `proposed` y una sin campo `status`, quedan hoy marcadas como VIGENTES por el criterio nuevo, y aceptaria el gate I4 una regla respaldada por ellas?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/artifacts/Analista-TASK-0365-spec-memoria-hibrida-review-formal-verdict.md
  - scripts/memory/build_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# REVIEW -- TASK-0368 (la puerta de F3)

Contexto que cambia el peso de esta review: el operador ha fijado **terminar la memoria hibrida**
como objetivo y ha **pre-aprobado la DECISION de activacion de F3**. Esta tarea es la puerta de esa
fase. Si pasa mal, lo siguiente que ocurre es que se enciende el enfriado de historia sobre una capa
de politica equivocada.

## Lo que el maker entrega

Sustituye la comparacion literal por la propiedad *"una decision sigue vigente hasta que declara
`superseded_by`"*, mapeada a estados de DB por la politica atestada, con el mismo predicado
compartido entre el builder y el gate rapido de I4. El negativo permanente
`NEG-MEMORY-CURRENT-DECISION-PROPERTY` deriva su poblacion del texto de citas de AGENTS.md, cubre
`accepted` mas una tercera grafia futura, mata el mutante viejo, y prueba que editar la politica sin
commitear no surte efecto.

Censo reportado: de `active=4, historical=105` a **`active=109, historical=0, superseded=1`**.

Todo eso, si es cierto, es lo que la tarea pedia. **Verificalo, no lo heredes** -- en especial que el
negativo mate de verdad y que la superficie sea la atestada.

## Lo que medi, y es el angulo que quiero atacado

Un criterio que hace vigente a **casi todo** me inquieta tanto como el que hacia vigente a casi nada.
Fui al corpus y conte:

    accepted           104
    active               4
    proposed             1     DECISION-0078-medicion-peones-ab-c-sandbox.md
    sin campo status     1     DECISION-0059-claim-grano-fino-y-serializacion-fisica.md
    -------------------------
    total              110
    superseded_by no vacio: 1  DECISION-0071 -> DECISION-0081

**110 menos 1 superseded = 109**, que es exactamente el numero de vigentes que el maker reporta. De
donde se sigue, si la aritmetica no me engana, que **DECISION-0078 -- que nadie aprobo -- y
DECISION-0059 -- que no declara estado -- han quedado marcadas como VIGENTES**.

Si eso es asi, el fail-open no se cerro: se dio la vuelta. Antes el motor archivaba lo que estaba en
vigor; ahora aceptaria como respaldo de una regla una decision que solo esta **propuesta**. Y esa es
justo la garantia que I4 existe para proteger: el gate rechaza una regla que referencia una decision
ausente o no vigente. Una decision `proposed` no esta en vigor.

**Estado epistemico de mi afirmacion, para que no la heredes**: el censo del corpus lo MEDI yo
(nombres y aritmetica, arriba). Que el motor las trate como vigentes lo INFIERO de que su cifra
coincide exactamente con mi cuenta. No lo he ejecutado. Puede que el motor las excluya por otra via y
que el 109 salga de otra composicion; si es asi, dilo y quedate con tu medicion.

La pregunta completa tiene dos mitades y quiero las dos:

1. Salen hoy con `hot_required=1`?
2. **Aceptaria el gate I4 una regla respaldada por DECISION-0078?** Es la mitad que importa, porque
   es donde la propiedad se convierte en consecuencia.

## Lo demas, por orden

- **AC1**: que el criterio nombre la propiedad y no sea una lista con un elemento mas. Parece
  cumplido; comprueba que no queda ningun literal gobernando el camino.
- **AC2**: superficie atestada. Se acredita como P9 -- editar la politica SIN commitear no surte
  efecto. El maker dice que lo prueba; reprodicelo.
- **AC3**: la poblacion del test sale del texto de AGENTS.md, no de una lista. Si esta escrita a
  mano, no acredita.
- **AC4**: supervivencia a una tercera grafia **con fallo RUIDOSO**. Es la cara que calla, y la que
  la tarea existe para cerrar.
- **AC5**: el par -- regla respaldada por decision vigente PASA, regla respaldada por ausente MUERE.
- **AC6**: censo antes y despues en las DOS direcciones, derivado de una construccion real.

Puertas del repo por exit code en clon limpio. Alcance SOLO hub.

-- Arquitecto, 2026-08-13 23:52 local (UTC+2)
