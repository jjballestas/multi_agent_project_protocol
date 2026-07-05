---
handoff_id: HANDOFF-TASK-0254-codex-to-arquitecto-2
task_id: TASK-0254
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-05
product_repo: D:/Agentes/Zeus/NOVA/Nova-Budget
product_commit: 02e67d8
---

# TASK-0254 retry delivery

The DBA SELECT grant removed the live blocker. Product commit remains
`02e67d8 feat: add availability adjustment baseline`; no product code change was required in this retry.

Evidence:
- `tests/NOVA.IntegrationTests/ApplyAvailabilityAdjustmentEvidenceTests.cs` runs the real SQL gateway
  `SqlApplyAvailabilityAdjustmentGateway` through `ApplyAvailabilityAdjustmentEvidenceHarness.FromEnvironment()`.
- Live sandbox gate passed: `dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter ApplyAvailabilityAdjustmentEvidenceTests`
  PASS, 2 tests, 0 skipped.
- The evidence harness covers the 8 GWT cases from SPEC-NOVA-P4-002 s.7, including GWT3 contracredit 09
  over the real floor returning 50261, and asserts real balance provenance
  `Budget.vw_Commitment_Availability_Validation` for successful cases.
- Prior THROW reconfirmation remains: 50083, 50084, 50250, 50251, 50252, 50253, 50254, 50255, 50256,
  50257, 50258, 50260, 50261; 50259 absent.

Gates:
- `dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter ApplyAvailabilityAdjustmentEvidenceTests`
  PASS: 2 tests, 0 skipped.
- `dotnet test NOVA.sln` PASS: 49 tests, with known NU1903 Microsoft.OpenApi warning.
- `npm test --prefix apps/nova-web` PASS: typecheck + 1 Vitest test.

Measurement:
- CLOSE measurement was not written by Codex because it lives under `personal/Arquitecto/TFM-medicion/`.
  Requested close command for Arquitecto:
  `python personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_ledger.py cerrar-fila --corpus personal/Arquitecto/TFM-medicion/corpus/medicion --clave TASK-0254`

task_id: TASK-0254
status: in_review
executive_summary: TASK-0254 live F-NOVA-01 retry passed after DBA granted SELECT on Budget.Budget_Adjustment; product commit remains 02e67d8.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget@02e67d8; tests/NOVA.IntegrationTests/ApplyAvailabilityAdjustmentEvidenceTests.cs; Area_comun/handoffs/HANDOFF-TASK-0254-codex-to-arquitecto-2.md
gates: dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter ApplyAvailabilityAdjustmentEvidenceTests PASS 2 tests; dotnet test NOVA.sln PASS 49 tests; npm test --prefix apps/nova-web PASS
next_recommended: Arquitecto/checker performs adversarial review, including real-sandbox provenance and PAR-1 isolation, then ratifies or returns findings.
risks: CLOSE measurement row remains pending under personal/Arquitecto/TFM-medicion; known NU1903 Microsoft.OpenApi warning remains unchanged.
