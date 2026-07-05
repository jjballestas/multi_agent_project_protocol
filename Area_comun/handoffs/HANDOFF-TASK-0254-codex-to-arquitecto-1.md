---
handoff_id: HANDOFF-TASK-0254-codex-to-arquitecto-1
task_id: TASK-0254
from: Codex
to: Arquitecto
status: blocked
created_at: 2026-07-05
product_repo: D:/Agentes/Zeus/NOVA/Nova-Budget
product_commit: 02e67d8
---

# TASK-0254 blocked handoff

Implemented the P4.2 Apply_Availability_Adjustment baseline in Nova-Budget and committed product code:
`02e67d8 feat: add availability adjustment baseline`.

Artifacts:
- Application/Contracts/Infrastructure: `src/NOVA.Application/Budget/AvailabilityAdjustments/`,
  `src/NOVA.Contracts/Budget/AvailabilityAdjustments/`,
  `src/NOVA.Infrastructure/Budget/AvailabilityAdjustments/SqlAvailabilityAdjustmentGateway.cs`.
- API: `POST /api/budget/availability-certificates/{availabilityCertificateId}/adjustments/validate`
  and `POST /api/budget/availability-certificates/{availabilityCertificateId}/adjustments`.
- UI: `apps/nova-web/src/App.tsx` adds the CDP adjustment form and preview against
  `Budget.vw_Commitment_Availability_Validation`.
- Evidence harness: `tests/NOVA.IntegrationTests/ApplyAvailabilityAdjustmentEvidenceTests.cs` uses the real SQL
  gateway when `NOVA_BUDGET_PARITY_CONNECTION_STRING` and `NOVA_BUDGET_SANDBOX_RESET_SQL` are configured; no
  in-memory recording substitute is used.

Gates:
- `dotnet test NOVA.sln` PASS: 49 tests, with known NU1903 Microsoft.OpenApi warning.
- `npm test --prefix apps/nova-web` PASS: typecheck + 1 Vitest test.
- `dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter ApplyAvailabilityAdjustmentEvidenceTests`
  FAILS against live sandbox: `SELECT permission was denied on the object 'Budget_Adjustment', database
  'DbsFinanciero_SANDBOX', schema 'Budget'`.
- Re-confirmed deployed THROW set through `OBJECT_DEFINITION`: 50083, 50084, 50250, 50251, 50252, 50253, 50254,
  50255, 50256, 50257, 50258, 50260, 50261. 50259 absent.

Blocker:
The verifier can execute far enough to reach the deployed proc, but live F-NOVA-01 cannot pass because the proc path
raises SQL 229 on `Budget.Budget_Adjustment`. Operator/DBA must grant or correct the sandbox execution context so
`budget_sandbox_verifier` can complete `Budget.Apply_Availability_Adjustment` without direct table SELECT denial.

task_id: TASK-0254
status: blocked
executive_summary: Product baseline committed, but live sandbox evidence is blocked by SQL 229 on Budget.Budget_Adjustment.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget@02e67d8; Area_comun/handoffs/HANDOFF-TASK-0254-codex-to-arquitecto-1.md
gates: dotnet test NOVA.sln PASS; npm test --prefix apps/nova-web PASS; live ApplyAvailabilityAdjustmentEvidenceTests FAIL SQL 229; THROW reconfirm PASS
next_recommended: DBA/operator fixes sandbox permission or proc ownership-chain issue for Budget.Apply_Availability_Adjustment, then Codex reruns live evidence and moves TASK-0254 to in_review.
risks: TASK-0254 cannot satisfy F-NOVA-01 until the live sandbox permission failure is removed.
