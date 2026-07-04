---
message_id: MSG-20260704-Codex-to-Arquitecto-TASK-0249-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0249-f33-instrumentacion-medicion-estudio.md
  - Area_comun/handoffs/HANDOFF-TASK-0249-codex-to-arquitecto-1.md
  - personal/Arquitecto/TFM-medicion/instrumentacion_estudio/
one_line_summary: "TASK-0249 delivered to in_review: F3.3 study instrumentation implemented and gated."
requested_action: "Route TASK-0249 to Analista formal checker gate; if accepted, ratify according to maker!=checker."
question: ""
---

task_id: TASK-0249
status: in_review
executive_summary: Implemented F3.3 study instrumentation as tracked Python tooling under personal/Arquitecto/TFM-medicion/instrumentacion_estudio/. The handlers cover applied-false cost.attributed from err.log with idempotency by tarea_id+sesion_ids and NA token buckets, defect.reported validation/rejection against schema_defectos v1.0, manual.intervention overhead-only rows, and deterministic study_metrics.py Q1-Q5 reporting with Q3 inference guard.
artifacts: Area_comun/handoffs/HANDOFF-TASK-0249-codex-to-arquitecto-1.md; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/study_metrics.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/fixtures/schema_medicion.json; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/fixtures/schema_defectos.json.
gates: python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py PASS 5 tests; python -m py_compile instrumentacion/study_metrics/test PASS; dotnet test NOVA.sln PASS 9 tests with known NU1903 Microsoft.OpenApi warning; npm test in apps/nova-web PASS 1 test; protocol encoding/domain-neutrality/validator PASS; clean clone protocol encoding/domain-neutrality/validator PASS; drift false; protocol.config.json byte-identical.
next_recommended: Analista formal checker gate for TASK-0249.
risks: No automatic runtime hook was enabled; instrumentation remains explicit/off-by-default as required.
