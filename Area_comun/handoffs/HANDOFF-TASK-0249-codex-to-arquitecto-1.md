---
handoff_id: HANDOFF-TASK-0249-codex-to-arquitecto-1
task_id: TASK-0249
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-04
---

task_id: TASK-0249
status: in_review
executive_summary: Implemented F3.3 study instrumentation as tracked Python tooling under personal/Arquitecto/TFM-medicion/instrumentacion_estudio/. The handlers cover applied-false cost.attributed from err.log with idempotency by tarea_id+sesion_ids and NA token buckets, defect.reported validation/rejection against schema_defectos v1.0, manual.intervention overhead-only rows, and deterministic study_metrics.py Q1-Q5 reporting with Q3 inference guard.
artifacts: personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/study_metrics.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/fixtures/schema_medicion.json; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/fixtures/schema_defectos.json; SPEC sha256 97B76B1DDC9FA47DDA0C8D8B01E618547BE3BFCF9F0566C60D5FD342F49D2CAD.
gates: python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py PASS 5 tests; python -m py_compile instrumentacion/study_metrics/test PASS; dotnet test NOVA.sln PASS 9 tests with known NU1903 Microsoft.OpenApi warning; npm test in apps/nova-web PASS 1 test; python scripts/scan_encoding.py --root . PASS; python scripts/scan_domain_neutrality.py --root . PASS; python scripts/validate_collaboration_state.py --root . PASS; clean clone protocol encoding/domain-neutrality/validator PASS; drift false up_to_seq=3859 before clean-clone fix claim; protocol.config.json byte-identical.
next_recommended: Analista formal checker gate for TASK-0249, then Arquitecto ratification if accepted.
risks: Implementation writes study CSV artifacts only when explicitly invoked; no automatic runtime hook was enabled, preserving off-by-default and byte-equivalent protocol event log when inactive.
