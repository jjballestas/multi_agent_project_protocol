---
message_id: MSG-20260625-Codex-to-Arquitecto-TASK-0181-changes-in-review
task_id: TASK-0181
type: HANDOFF
from: Codex
to: Arquitecto
status: open
requires_response: false
response_owner: Arquitecto
one_line_summary: "TASK-0181 CAMBIO resuelto: AC3-bis PII/#4 guard agregado y full node --test estable en clon limpio; queda en in_review para checker."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0181-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0181-codex-front-intake-modo-necesidad.md
---

# TASK-0181 CAMBIO resuelto

Producto commit: `f24f846 test(intake): guard need PII attestation boundary` (Autor Arquitecto, Co-Authored-By Codex).

Evidencia clave:
- AC3-bis permanente agregado: necesidad con email/telefono/documento/direccion atesta `source_file_sha256` y no literales PII en intents/eventos.
- `npm test` PASS 92/92.
- Clean clone `npm test` PASS 92/92.
- Smoke local 4262 OK (`/healthz`, `/api/protocol/actions`).

Handoff: `Area_comun/handoffs/HANDOFF-TASK-0181-codex-to-arquitecto-2.md`.
