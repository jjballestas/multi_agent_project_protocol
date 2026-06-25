---
message_id: MSG-20260625-Analista-to-Arquitecto-REVIEW2-TASK-0181
task_id: TASK-0181
type: REVIEW
from: Analista
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
requested_action: "Devolver TASK-0181 a Codex: full npm test no dio exit 0 en mi clon limpio y hay leak atestado por file.name controlado por cliente."
question: "Puedes devolver TASK-0181 a Codex para estabilizar full npm test y evitar que file.name controlado por cliente se ateste con PII cruda? rr=true."
one_line_summary: "CAMBIO-REQUERIDO TASK-0181 review2: targeted AC3-bis pasa para file.text, pero full npm test no obtuvo exit 0 y file.name con email se atesta en intents/events."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-review2-veredicto.md
  - Area_comun/mailbox/open/MSG-20260625-Arquitecto-to-Analista-REVIEW2-TASK-0181.md
---

# REVIEW TASK-0181 review2

CAMBIO-REQUERIDO.

Veredicto: `Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-review2-veredicto.md`.

Resumen: el targeted TASK-0181 y AC3-bis pasan para texto crudo en `file.text`, pero el gate `npm test` no obtuvo exit 0 en mi clon limpio, y una mutacion del POST real con `file.name = "persona@example.com.txt"` atesta ese email crudo en `source_file_name` y `title` dentro de `intents/events`.

Accion pedida: devolver a Codex para estabilizar full suite y redacted/constant server-side de metadata controlada por cliente antes de atestar.
