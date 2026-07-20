---
message_id: MSG-20260720-Codex-to-Operador-REPORTE-TASK-0269-umbral-E6
from: Codex
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0269-materializacion-parcial.md
one_line_summary: "E6 measurement: valid hot 108.199s exceeds 15s; sealed rule selects permanent E6-A pending checker reproduction."
---

task_id: TASK-0269
status: in_review
executive_summary: The valid measured hot full-hook time is 108.199s, above the sealed 15s threshold; permanent E6-A is the resulting branch pending checker reproduction.
artifacts: commit 07fad8a; Area_comun/handoffs/HANDOFF-TASK-0269-materializacion-parcial.md
gates: partial-total parity suite PASS; four protocol gates PASS; drift false seq 5197
next_recommended: Use the checker-owned warm rerun as the final number and retain E6-A if it remains above 15s.
risks: Shared-host load affects wall time, but the observed margin over 15s is large.
