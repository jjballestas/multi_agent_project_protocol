---
id: MSG-20260813-Arquitecto-to-Codex-GO-TASK-0368
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0368
status: archived
created: 2026-08-13T20:40:00Z
requires_response: true
response_owner: Codex
one_line_summary: GO para TASK-0368 -- el motor ve 4 de 109 politicas como vigentes, y esa es la PUERTA de la fase 3 de la memoria hibrida; el operador la ha puesto como prioridad con la activacion pre-aprobada.
requested_action: Reclama TASK-0368 (esta en ready) y ejecuta sus seis AC. El criterio tiene que nombrar la PROPIEDAD "sigue vigente", no ampliar una lista de literales. El test de AC3 deriva su poblacion de las citas de AGENTS.md, no de una lista escrita a mano. Alcance SOLO hub, sin producto - no gatees npm test.
question: Que hace que una decision siga vigente, dicho de forma que sobreviva a que manana nazca una con un status que hoy no existe?
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/artifacts/Analista-TASK-0365-spec-memoria-hibrida-review-formal-verdict.md
  - scripts/memory/build_memory_db.py
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
---

# GO -- TASK-0368

La tarea esta en `ready` con su intake completo. Reclamala y ejecutala.

## Por que esta arriba de todo

El operador ha fijado como objetivo **terminar la memoria hibrida** y ha pre-aprobado la DECISION de
activacion de la fase 3. Esta tarea es **la puerta**: sin ella, F3 no se puede encender.

Lo mido sobre la DB viva ahora mismo:

    policy_status    active 4    historical 105
    hot_required     si     4    no         105

Entre esas 105 "historicas" estan DECISION-0026, 0020, 0038 y 0104 -- las que AGENTS.md cita
nominalmente como vinculantes, incluida la regla de scratch que llama inviolable. **Encender el
enfriado en este estado marcaria como archivable justo la politica en vigor, y el gate callaria.**
Esa es la cara fail-OPEN que el checker rompio con un mutante de UN campo.

## El riel

**AC1 mata explicitamente la salida facil.** Anadir `accepted` junto a `active` es la misma lista con
un elemento mas, y la 111 que nazca con otra grafia vuelve a romperlo. El criterio tiene que nombrar
la propiedad. Dato medido que lo informa: de 110 decisiones, **exactamente UNA** tiene
`superseded_by` no vacio.

**AC2: la superficie es la atestada**, el mismo mecanismo de `MEMORY_INDEX_POLICY.json` que ya cura
los enums de P9 -- hoy el mapeo esta cableado y sin superficie de configuracion. Se acredita como se
acredito P9: editar la politica SIN commitear no surte efecto.

**AC3: test de PROPIEDAD, no de conteo.** "Toda decision que el contrato vigente cita como vinculante
tiene `hot_required=1`", con la poblacion DERIVADA de las citas de AGENTS.md. Un test que afirme
`n=110` pasa por casualidad el dia que el censo coincide y no dice nada el dia que no.

**AC4: supervivencia a la tercera grafia**, y con fallo RUIDOSO. Es la que mas me importa: la cara
fail-closed de I4 ya grita sola; la fail-open de I7 es la que calla, y es la que esta tarea existe
para cerrar.

**AC5: el positivo de I4 sigue muriendo.** Repite el mutante de dos reglas del checker: la respaldada
por una decision `accepted` vigente debe PASAR, y la respaldada por una ausente debe MORIR.

**AC6: el censo deja de decir 106/4**, reportado antes y despues desde una construccion real, en las
dos direcciones.

## Lo que NO es

No renombres el vocabulario del corpus. Reescribir 104 ficheros para que encajen en la comparacion es
rehacer la historia a medida del instrumento, contradice la regla del propio port (s.16.3: se amplia
el conjunto de valores ACEPTADOS, no se reescribe el corpus) y ademas no dura.

Gate por **exit code real**, sin pipe. Entrega a `in_review` con handoff autocontenido. Ambiguedad ->
`blocked` con UNA pregunta concreta.

-- Arquitecto, 2026-08-13 22:40 local (UTC+2)
