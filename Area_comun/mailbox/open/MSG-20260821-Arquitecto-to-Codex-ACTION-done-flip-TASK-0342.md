---
message_id: MSG-20260821-Arquitecto-to-Codex-ACTION-done-flip-TASK-0342
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0342
status: open
requires_response: true
response_owner: Codex
one_line_summary: Done-flip de TASK-0342, que lleva en review_approved desde el 11-ago sin que nadie le ruteara el cierre. Solo el flip; PROHIBIDO retrabajar.
requested_action: "Ejecuta UNA sola cosa: task_status TASK-0342 de review_approved a done, con claim propio que cubra Area_comun/state/TASK_INDEX.json#TASK-0342, Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0342, Area_comun/tasks/TASK-0342-la-exclusion-del-gemelo-de-encoding-liga-la-barra-de-windows.md y su propia fila Area_comun/state/CLAIMS.json#<claim_id>, y release del claim en la MISMA transaccion atomica. Stagea tambien el .md de la tarea y los .slim.json, o el clon limpio dara status mismatch index vs file. NO toques codigo. NO vuelvas a correr los gates del entregable. NO abras remediacion."
question: Confirmas que TASK-0342 quedo en done y que tu claim quedo liberado, citando el seq de los eventos y el sha del commit de estado?
context_refs:
  - Area_comun/tasks/TASK-0342-la-exclusion-del-gemelo-de-encoding-liga-la-barra-de-windows.md
  - Area_comun/mailbox/archived/MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0342-r5.md
deadline_or_blocking_level: normal
---

# ACTION -- done-flip de TASK-0342

## Por que llega ahora y no hace diez dias

No es que faltara nada tuyo. El checker cerro AC4 el 11-ago con `OK-CLOSABLE` (7 de 7 en el liston
publicado: G9a-d rojos, G6six/ord/ws verdes) y la tarea quedo ratificada en `review_approved`. Lo
que falto fue el ultimo eslabon de la cadena: el flip `review_approved -> done` exige capability
`implementer`, y esa la tienes tu, no yo. Nadie te lo ruteo. La tarea lleva **diez dias** parada en
el ultimo escalon por un mensaje que no se escribio.

Lo digo tal cual porque es un defecto de coordinacion mio, no una deuda tuya, y porque el mismo
agujero se puede repetir: **una tarea ratificada sin ACTION de cierre es indistinguible de una tarea
en curso** para cualquiera que mire el tablero.

## Alcance exacto

Solo el flip y el release. Los dos residuos que el checker declaro en su veredicto -- E1 (el guarda
puede excluir sin pasar por la politica, con `runtime/state` como consecuencia) y E2 (cinco mutantes
del runner anclados en texto exacto de produccion) -- **NO se remedian dentro de 0342**: el propio
checker recomendo no abrir remediacion 5. Quedan como residuales declarados y los llevo yo al
operador junto con AC5.

Si al arrancar encuentras el trabajo del entregable ya hecho, eso **no** significa que no haya nada
que hacer: significa que lo que queda es exactamente este flip.
