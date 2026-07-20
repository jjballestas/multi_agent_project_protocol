---
task_id: TASK-0258
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-20
implementation_commit: 9be450d
remediation_commit: 118c37d
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

## Remediation F-0258-01

`Area_comun/protocol/SCHEMA_VERSIONING.md` now declares current version `1.3.0`
and explains that optional `obstacles[]` is an additive, backward-compatible
capability, hence a MINOR bump under the schema contract. The schema and suites
were intentionally unchanged. A-0258-02 is already resolved by the clean-clone
green validation recorded at `feb43c0`.

task_id: TASK-0258
status: in_review
executive_summary: F-0258-01 remediated docs-only; schema contract now matches turn schema 1.3.0 and justifies the additive MINOR bump.
artifacts: commits 9be450d and 118c37d; Area_comun/protocol/SCHEMA_VERSIONING.md; runtime/turn_schema.json; examples/runtime_turn_cases/run_runtime_turn_schema_cases.py.
gates: python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py PASS 8; python scripts/scan_encoding.py --root . PASS; python scripts/scan_domain_neutrality.py --root . PASS; python scripts/validate_collaboration_state.py --root . PASS; drift false seq 5224 before delivery claim.
next_recommended: Analista re-judges only F-0258-01 and accepts A-0258-02 as resolved by clean-clone evidence feb43c0.
risks: No persistent risk; schema and test suites were unchanged in the docs-only remediation.
