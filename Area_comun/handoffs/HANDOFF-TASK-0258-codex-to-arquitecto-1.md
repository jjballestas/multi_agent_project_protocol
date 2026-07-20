---
task_id: TASK-0258
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-20
implementation_commit: 9be450d
---

# Handoff TASK-0258

`runtime/turn_schema.json` 1.3.0 admite `obstacles` opcional como array estricto.
Cada item exige `what`, `root_cause`, `resolution` y `recurrence_risk`; el riesgo
queda limitado a `low`, `medium` o `high` y no se admiten propiedades adicionales.

La suite cubre un array poblado valido, un array vacio valido y un item incompleto
con riesgo fuera del enum como invalido.

Obstacles: ninguno funcional. Friccion operativa: un primer `scan_encoding.py`
coincidio con acceso transitorio denegado sobre un archivo ajeno; el rerun aislado
paso limpio. No se tocaron archivos ajenos.

task_id: TASK-0258
status: in_review
executive_summary: Canonical optional obstacles array delivered in turn schema 1.3.0 with strict four-field items and regression coverage.
artifacts: commit 9be450d; runtime/turn_schema.json; examples/runtime_turn_cases/run_runtime_turn_schema_cases.py; three obstacle fixtures.
gates: python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py PASS 8; semantic cases PASS 5; encoding PASS; neutrality PASS; validate PASS; drift false seq 5173.
next_recommended: Analista reviews TASK-0258 against DECISION-0103 C3 and confirms the canonical shape for TASK-0261/TASK-0262.
risks: One transient encoding-scan permission error cleared on immediate isolated rerun; no persistent product or protocol risk observed.
