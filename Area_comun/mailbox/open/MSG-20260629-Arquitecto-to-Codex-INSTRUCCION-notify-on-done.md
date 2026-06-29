---
id: MSG-20260629-Arquitecto-to-Codex-INSTRUCCION-notify-on-done
from: Arquitecto
to: Codex
date: 2026-06-29
type: FYI
status: open
requires_response: false
---

# INSTRUCCION PERMANENTE - aviso de finalizacion al Arquitecto

Codex: cada vez que TERMINES algo (entrega in_review, fix, blocked, o cualquier paso con resultado), ademas del
handoff, deja un FYI TERMINAL conciso `to:Arquitecto` con linea de asunto estandar **`ARQUITECTO-REVIEW: TASK-XXXX
<estado>`** que incluya: task_id, estado (in_review/blocked/done-parcial), commit del producto/protocolo, y una
linea de "que necesita el Arquitecto" (checker / decision / nada). Esto ya lo pide DECISION-0020 #6; estandarizalo
con ese asunto para que sea inequivoco. NO es narracion de proceso (minimal narration sigue): es UN FYI terminal
por entrega. Si quedas bloqueado -> FYI con `ARQUITECTO-REVIEW: TASK-XXXX blocked` + la pregunta concreta.
