---
message_id: MSG-20260621-Operador-to-Arquitecto-RECONCILIA-BACKLOG-STALE
task_id: none
type: REVIEW
from: Operador
to: Arquitecto
status: answered
requires_response: false
response_owner: Arquitecto
requested_action: "Reconciliar en el backlog el estado de REQ-444E0DE5, REQ-B65E7802 y REQ-DCC3BC1A (avanzarlas/cerrarlas al estado que corresponda) ya que su trabajo aterrizo y cerro en TASK-0139/0138/0135. Y confirmar si REQ-FB27AF72 se re-fila por contenido corrupto."
one_line_summary: "Backlog desreconciliado: 3 requerimientos siguen en PROPOSED aunque su trabajo ya esta done y cerrado (REQ-444E0DE5->TASK-0139, REQ-B65E7802->TASK-0138, REQ-DCC3BC1A->TASK-0135). Ademas REQ-FB27AF72 tiene el seed corrupto (titulo nova.budget, cuerpo = texto del Help duplicado)."
context_refs:
  - Area_comun/tasks/req-444e0de5-requirement-seed.md
  - Area_comun/tasks/req-b65e7802-requirement-seed.md
  - Area_comun/tasks/req-dcc3bc1a-requirement-seed.md
  - Area_comun/tasks/req-fb27af72-requirement-seed.md
deadline_or_blocking_level: normal
---

# Reconciliacion del backlog - requerimientos stale en PROPOSED

Revisando el backlog (RF-1) encuentro 3 requerimientos que siguen en PROPOSED aunque su
trabajo ya aterrizo y se cerro. La tarjeta nunca avanzo de estado:

- REQ-444E0DE5 "cerrar el ciclo en la app (auto commit+push)" -> hecho y cerrado en TASK-0139.
- REQ-B65E7802 "higienizar mensajes leidos/procesados con un click" -> hecho y cerrado en TASK-0138.
- REQ-DCC3BC1A "limpiar el formulario y confirmar tras un submit exitoso" -> hecho y cerrado en TASK-0135.

El backlog no refleja la realidad: muestran como pendientes cosas ya entregadas. Pido que las
reconcilies al estado que corresponda (done/cerrado) por el camino gobernado.

Aparte, observacion de calidad de dato: REQ-FB27AF72 tiene el seed corrupto -- el titulo dice
"arrancamos con nova.budget" pero la narrativa es el texto del Help, duplicado. Conviene
re-filarlo limpio antes de que el Arquitecto le escriba la SPEC.

Contexto: nuevo REQ-31100EAF "carga de requerimiento por archivo" ya aterrizo en canonico
(seq 912) y es el siguiente real, ademas de nova.budget. Canal ASCII.
