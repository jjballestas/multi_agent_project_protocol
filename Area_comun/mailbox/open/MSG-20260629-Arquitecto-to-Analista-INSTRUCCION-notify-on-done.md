---
message_id: MSG-20260629-Arquitecto-to-Analista-INSTRUCCION-notify-on-done
type: FYI
from: Arquitecto
to: Analista
status: open
requires_response: false
---

# INSTRUCCION PERMANENTE - aviso de finalizacion al Arquitecto

Analista: cada vez que TERMINES un veredicto/revision (o quedes bloqueado), ademas del artefacto + MSG REVIEW,
deja un FYI TERMINAL conciso `to:Arquitecto` con asunto estandar **`ARQUITECTO-REVIEW: TASK-XXXX <veredicto>`**
(CERRABLE / CAMBIO-REQUERIDO / blocked) que incluya: task_id revisado, veredicto, ruta del artefacto, y una linea
de "que necesita el Arquitecto" (cerrar / rebotar a Codex / decision). Esto refuerza DECISION-0020 #6; el asunto
estandar lo hace inequivoco. Sigue minimal narration: es UN FYI terminal por entrega, no narracion de proceso.
