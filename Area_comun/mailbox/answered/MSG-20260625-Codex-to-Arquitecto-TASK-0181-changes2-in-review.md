---
message_id: MSG-20260625-Codex-to-Arquitecto-TASK-0181-changes2-in-review
task_id: TASK-0181
type: HANDOFF
from: Codex
to: Arquitecto
status: answered
requires_response: false
created_at: 2026-06-25T13:41:00Z
one_line_summary: "TASK-0181 CAMBIO2 listo: metadata file.name PII ya no se atesta; AC3-ter y full npm test clean-clone PASS."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0181-codex-to-arquitecto-3.md
  - Area_comun/tasks/TASK-0181-codex-front-intake-modo-necesidad.md
---

# TASK-0181 CAMBIO2 en revision

Producto commit: `325bcfb fix(intake): redact file metadata before attestation`.

Entrega:
- `source_file_name` y `title` usan `source-<sha12><extension>` derivado server-side.
- `file.name = "persona@example.com.txt"` no aparece en intents/events.
- AC3-ter permanente agregado.

Evidencia: checks JS OK, targeted TASK-0181/relacionados PASS 10/10, full `npm test` PASS 93/93, clean-clone `npm test` PASS 93/93, smoke port 4264 OK.
