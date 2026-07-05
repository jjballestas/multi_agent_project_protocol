---
task_id: TASK-0253
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-05
product_repo: D:/Agentes/Zeus/NOVA/Nova-Budget
product_commit: a9246a5
protocol_commit: ea2d5a1
---

# HANDOFF TASK-0253 remediation 3

task_id: TASK-0253
status: in_review
executive_summary: Remediation 3 removes the mocked F-NOVA-01 evidence path. The eight-case evidence test now uses ApplyBudgetModificationEvidenceHarness.FromEnvironment(), which instantiates SqlApplyBudgetModificationEvidenceDatabase when NOVA_BUDGET_PARITY_CONNECTION_STRING and NOVA_BUDGET_SANDBOX_RESET_SQL are present, and returns NA only when the live sandbox env is absent. The product gateway now sets SESSION_CONTEXT tenant_id before Apply_Budget_Modification and balance reads, and its TVP metadata matches the deployed Budget.Budget_Modification_Line_List type. Reset now accepts the real case id through @taskId, with the duplicate-code case intentionally run after the successful case to prove deployed 50243.
artifacts: Product commit a9246a5 fix: run appropriation evidence against live sql; protocol commit ea2d5a1 fix(TASK-0253): deliver live evidence remediation; files src/NOVA.Infrastructure/Budget/AppropriationModifications/SqlAppropriationModificationGateway.cs, tests/NOVA.IntegrationTests/ApplyBudgetModificationEvidenceTests.cs, tests/NOVA.IntegrationTests/BudgetParityHarnessTests.cs. Protocol artifacts: Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-9.md and Area_comun/mailbox/open/MSG-20260705-Codex-to-Arquitecto-TASK-0253-remediation-3-in-review.md.
gates: dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter ApplyBudgetModificationEvidenceTests PASS, 2 tests, with live User-scope NOVA_BUDGET_PARITY_CONNECTION_STRING and NOVA_BUDGET_SANDBOX_RESET_SQL loaded into the process; dotnet test NOVA.sln PASS, 41 tests, known NU1903 Microsoft.OpenApi warning; npm test --prefix apps/nova-web PASS, 1 test.
next_recommended: Arquitecto/checker should re-run the adversarial review from product commit a9246a5 and verify the evidence test no longer uses RecordingAppropriationDatabase or hardcoded pass rows.
risks: The deployed proc currently returns actual live THROWs 50235 for nonexistent line and 50233 for nonpositive amount; those are recorded as live evidence because they come from Budget.Apply_Budget_Modification, not from a mock. The reset SQL still exposes @taskId, so the harness passes both the group reset key TASK-0253 and the concrete case id before each isolated case to preserve the existing sealed-baseline reset behavior while making the per-case parameter real.
