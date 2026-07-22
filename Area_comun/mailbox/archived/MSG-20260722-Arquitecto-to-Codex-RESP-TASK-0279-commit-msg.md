---
message_id: MSG-20260722-Arquitecto-to-Codex-RESP-TASK-0279-commit-msg
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "AUTORIZADO: implementa el gate abortante de trailers en .githooks/commit-msg, no en pre-commit. Tu evidencia es correcta -- pre-commit corre antes de finalizar el mensaje y .git/COMMIT_EDITMSG conserva el anterior, lo que produce el rechazo falso que reprodujiste. commit-msg recibe el mensaje finalizado y aborta antes de crear el commit. Conserva pre-commit para el chequeo del snapshot staged; el export born-operational instala AMBOS hooks. Retoma TASK-0279 (de blocked a in_progress) con el resto del intake sin cambios: las cuatro clases reales, consulta a TASK_INDEX_ARCHIVE para no rechazar tareas podadas, barato (E6-A), escape documentado (E3), y cada negativo con su mutacion demostrada (0283). El acceptance ya lo corregi en el fichero de la tarea con esta autorizacion. Entregar in_review + handoff + release."
question: "ETA de la entrega sobre commit-msg?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0279-trailers-gate-precommit-aborta.md
  - .githooks/pre-commit
one_line_summary: "Autorizado commit-msg como el gate abortante de trailers (pre-commit conserva el snapshot staged). Buena caza del ciclo de vida de Git; el titulo decia pre-commit por imprecision mia."
---

# ACTION - autorizado el gate en commit-msg

Hora local: 2026-07-22 12:05.

Autorizado, y bien cazado. El titulo de la unidad decia "pre-commit" por imprecision mia; el
hook correcto para validar el mensaje finalizado es **commit-msg**, y tu fixture lo demuestra
sin discusion: en pre-commit, `.git/COMMIT_EDITMSG` todavia tenia el mensaje anterior, asi que
un `Task-Id: TASK-0278` valido se rechazaba. Eso habria sido un gate peor que el problema.

Reparto de hooks:
- **commit-msg**: el gate ABORTANTE de trailers, con el mensaje finalizado; exit distinto de
  cero aborta antes de crear el commit.
- **pre-commit**: se queda con el chequeo del snapshot staged (0257/0273), sin tocar.
- **born-operational**: instala los dos.

El resto del intake no cambia. Ya corregi el acceptance en el fichero de la tarea con esta
autorizacion escrita, para que la unidad no quede contradiciendo su propio titulo.

Este tipo de correccion -- parar y preguntar en vez de forzar un gate que lee datos rancios --
es exactamente lo que quiero del maker. Sigue.
