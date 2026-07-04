---
handoff_id: HANDOFF-TASK-0249-codex-to-arquitecto-3
task_id: TASK-0249
from: Codex
to: Arquitecto
created_at: 2026-07-04
status: in_review
related_message: MSG-20260704-Arquitecto-to-Codex-ACTION-TASK-0249-remediacion-2
---

# HANDOFF TASK-0249 - remediation 2

TASK-0249 fix-loop 2 remediates the two Analista blockers from re-judgement 1:

- F-0249-02: `read_errlog_tokens` now only accepts explicit cumulative fields:
  `tokens_total_atribuibles`, `tokens_total`, `cumulative_tokens`, or `total_tokens_cumulative`.
  Partial-only err.log payloads such as `prompt_tokens=100 completion_tokens=50` fail closed and do not
  write a measurement row.
- F-0249-03: Q3 paired deltas are now computed by arm as `gobernado - baseline`, not by physical CSV row
  order. Reversing the row order for the same pair preserves the delta sign.

Changed files:

- `personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py`
- `personal/Arquitecto/TFM-medicion/instrumentacion_estudio/study_metrics.py`
- `personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py`

Evidence:

- `python personal\Arquitecto\TFM-medicion\instrumentacion_estudio\test_instrumentacion.py` PASS,
  7 tests.
- `python -m py_compile personal\Arquitecto\TFM-medicion\instrumentacion_estudio\instrumentacion.py
  personal\Arquitecto\TFM-medicion\instrumentacion_estudio\study_metrics.py
  personal\Arquitecto\TFM-medicion\instrumentacion_estudio\test_instrumentacion.py` PASS.
- `dotnet test NOVA.sln` in `D:\Agentes\Zeus\NOVA\Nova-Budget` PASS, 9 tests; known NU1903
  `Microsoft.OpenApi` warning persists.
- `npm test` in `D:\Agentes\Zeus\NOVA\Nova-Budget\apps\nova-web` PASS, 1 test.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` initially reports only the expected active
  remediation claim while this handoff is being prepared; final delivery re-runs after release.

Requested next step: route formal re-judgement 2/2 to Analista for TASK-0249.

task_id: TASK-0249
status: in_review
executive_summary: "Remediated F-0249-02 and F-0249-03: err.log partial-only token fields fail closed, and Q3 deltas are arm-based/order-invariant."
artifacts: "personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/study_metrics.py; personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py; Area_comun/handoffs/HANDOFF-TASK-0249-codex-to-arquitecto-3.md"
gates: "test_instrumentacion PASS 7; py_compile PASS; Nova-Budget dotnet test PASS 9 with known NU1903; nova-web npm test PASS 1; encoding PASS; domain PASS; final validate/drift/byte-identical pending after claim release"
next_recommended: "Arquitecto routes TASK-0249 formal re-judgement 2/2 to Analista."
risks: "Known NU1903 Microsoft.OpenApi warning remains unrelated; this is fix-loop 2/2, so a surviving same-class finding should escalate to operator."
