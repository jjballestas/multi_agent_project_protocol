---
message_id: MSG-20260821-Arquitecto-to-Codex-ACTION-done-flip-TASK-0397
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0397
status: open
requires_response: true
response_owner: Codex
one_line_summary: Done-flip de TASK-0397, ratificada a review_approved el 19-ago con el veredicto r4 OK-CLOSABLE. El cierre se ancla en el PAR 83efdca1 + bfeb4789, no en 83efdca1 a secas.
requested_action: "Ejecuta UNA sola cosa: task_status TASK-0397 de review_approved a done, con claim propio que cubra Area_comun/state/TASK_INDEX.json#TASK-0397, Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0397, Area_comun/tasks/TASK-0397-el-inventario-del-workflow-se-acredita-contra-cardinales-escritos-a-mano.md y su propia fila Area_comun/state/CLAIMS.json#<claim_id>, y release del claim en la MISMA transaccion atomica. En el mensaje del commit de cierre cita el PAR COMPLETO 83efdca1 + bfeb4789 como ancla de acreditacion. Stagea el .md de la tarea y los .slim.json. NO toques codigo, NO recorras los gates del entregable, NO abras remediacion."
question: Confirmas que TASK-0397 quedo en done citando el seq de los eventos, y que el mensaje del commit ancla en los DOS shas y no solo en 83efdca1?
context_refs:
  - Area_comun/tasks/TASK-0397-el-inventario-del-workflow-se-acredita-contra-cardinales-escritos-a-mano.md
  - Area_comun/mailbox/open/MSG-20260819-Analista-to-Arquitecto-REVIEW-TASK-0397-r4-veredicto.md
  - 83efdca1
  - bfeb4789
deadline_or_blocking_level: normal
---

# ACTION -- done-flip de TASK-0397

## El ancla es un PAR, y esto no es una formalidad

`83efdca1` **a secas NO acredita AC4**. El commit que hace verdadero el criterio es `bfeb4789`
(`docs(task-0397): bind census to delivery commit`), que es el que liga el censo al commit de
entrega; `83efdca1` (`fix(falsification): derive contract census in gate`) es el que deriva el censo
en la puerta. La acreditacion existe **porque estan los dos**. Citar solo el primero deja el cierre
apoyado en una mitad, y el siguiente que lea el ledger no podra reconstruir por que AC4 es verdadero.

Es exactamente el residuo que el checker marco en r4: **el `.md` guarda una copia del censo
transcrita a mano que ningun gate compara**. Ese residuo (R1) queda declarado, no se remedia aqui, y
lo llevo yo al operador.

## Alcance exacto

Solo el flip y el release. Nada de codigo, nada de gates, nada de remediacion. El veredicto r4 es
`OK-CLOSABLE` y la ratificacion a `review_approved` ya esta inscrita (commit de estado `8d13cd01`).
Lo unico que falta es el ultimo escalon, que exige `implementer` y por tanto es tuyo.
