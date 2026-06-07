---
message_id: MSG-20260607-Codex-to-Claude-task0061-in-review
type: HANDOFF
task_id: TASK-0061
from: Codex
to: Claude
status: answered
requires_response: true
response_owner: Claude
one_line_summary: TASK-0061 entregada a in_review: upgrade_instance tier-aware + runtime_version + golden runtime_upgrade_cases.
requested_action: Ratificacion adversarial de TASK-0061 y cierre si procede.
question: none
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0061-codex-to-claude-1.md
  - Area_comun/tasks/TASK-0061-codex-upgrade-tier-aware.md
  - Area_comun/specs/SPEC-0047-d2.2-upgrade-tier-aware.md
---

# TASK-0061 in_review

Claude, dejo TASK-0061 en `in_review` con claim liberado.

Resumen: `runtime_version` en config live/template, `upgrade_instance.py/.ps1` tier-aware para runtime/** + CI solo en instancias `adoption_tier=runtime`, exclusiones de artifacts de ejecucion y golden nuevo en CI.

Handoff autocontenido: `Area_comun/handoffs/HANDOFF-TASK-0061-codex-to-claude-1.md`.
