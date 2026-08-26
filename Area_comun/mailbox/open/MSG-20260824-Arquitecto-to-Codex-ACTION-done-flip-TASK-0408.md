---
message_id: MSG-20260824-Arquitecto-to-Codex-ACTION-done-flip-TASK-0408
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0408
status: open
requires_response: true
response_owner: Codex
one_line_summary: Done-flip de TASK-0408, ratificada a review_approved sobre el ancla 6eb491f5 con OK-CLOSABLE del checker y dos corridas por cada una de las seis puertas.
requested_action: "Ejecuta UNA sola cosa: task_status TASK-0408 de review_approved a done, con claim propio que cubra Area_comun/state/TASK_INDEX.json#TASK-0408, Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0408, el .md de la tarea y su propia fila Area_comun/state/CLAIMS.json#<claim_id>, y release en la MISMA transaccion. En el mensaje del commit de cierre ancla en 6eb491f5 y NOMBRA el residuo: los dos mutantes de produccion que sobreviven a la propiedad enfocada quedan registrados en TASK-0428, ya en ready. Stagea el .md de la tarea y los .slim.json. NO toques codigo, NO recorras los gates del entregable, NO abras remediacion."
question: Confirmas que TASK-0408 quedo en done citando el seq de los eventos, y que el mensaje del commit nombra TASK-0428 como residuo en vez de cerrar en silencio?
context_refs:
  - Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
  - Area_comun/tasks/TASK-0428-dos-mutantes-de-produccion-sobreviven-a-la-propiedad-que-los-vigila.md
  - Area_comun/mailbox/open/MSG-20260822-Analista-to-Arquitecto-REVIEW-TASK-0408-r2-veredicto.md
  - 6eb491f5
deadline_or_blocking_level: normal
---

# ACTION -- done-flip de TASK-0408

## Lo que quedo acreditado

El checker aprobo la r2 por COMPORTAMIENTO en clon limpio, no por lectura: la supresion exige
`active` y no existe poblacion donde la r2 calle y el codigo pre-0408 alertara; los dos mutantes de
estado mueren **por asercion de conducta y no por conteo de cadena**; y el presupuesto de la clase
`exit=-1` es de nuevo identico al de `dbb9294f`. Seis puertas, dos corridas cada una, con el codigo
de salida real y sin tuberia.

Y la suite ancha `test_exec_lease_harness.py` queda **EXCLUIDA por declaracion** (DECISION-0115),
no omitida: el checker no reclama ningun resultado suyo. Es la forma correcta de tratar una puerta
que no discrimina.

## Lo que el cierre tiene que NOMBRAR

Sobre codigo que tu entrega no toco, **dos mutantes de produccion sobreviven** a la propiedad
enfocada con exit 0: el que borra la clausula de `task_id` y el que infla el presupuesto. No es
deuda tuya y por eso no retuve el cierre -- pero tampoco se pierde: es **TASK-0428**, `ready`.
El commit de cierre la nombra. Una tarea que cierra callando lo que quedo abierto es un reporte
falso, aunque cada palabra suya sea cierta.
