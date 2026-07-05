---
handoff_id: HANDOFF-TASK-0252-codex-to-arquitecto-2
task_id: TASK-0252
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-05
product_commit: 5ccb82c
protocol_commit: pending
fixes:
  - F-0252-01
  - F-0252-02
  - F-0252-03
---

# Handoff TASK-0252 remediation 1

task_id: TASK-0252
status: in_review
executive_summary: Product commit 5ccb82c hardens the Nova-Budget parity harness. It now validates the SQL execution context before reset/exec/endpoint work: `DB_NAME()` must equal `DbsFinanciero_SANDBOX`, and `IS_ROLEMEMBER('budget_sandbox_verifier')` must return 1. It also documents the reproducible clean-clone front gate as `npm ci --prefix apps/nova-web` followed by `npm test --prefix apps/nova-web`.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.IntegrationTests/BudgetParityHarnessTests.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/docs/budget-parity-harness.md; product commit 5ccb82c; clean clone C:/Users/johnb/AppData/Local/Temp/nova-budget-clean-0252-20260705021414
gates: `dotnet test NOVA.sln` PASS 29 tests with known NU1903 Microsoft.OpenApi warning; `npm ci --prefix apps/nova-web` PASS; `npm test --prefix apps/nova-web` PASS 1 test; clean clone at 5ccb82c PASS for `dotnet test NOVA.sln`, `npm ci --prefix apps/nova-web`, and `npm test --prefix apps/nova-web`; live SQL parity remains NA because secrets were not provided.
next_recommended: Arquitecto should request Analista re-judgement for TASK-0252 remediation 1 against F-0252-01, F-0252-02 and F-0252-03.
risks: D:/Agentes/Zeus/NOVA/Nova-Budget/docs/budget-parity-harness.md had pre-existing uncommitted edits in the worktree; only the safety-context and clean-clone gate hunks were staged into product commit 5ccb82c. Live SQL against `DbsFinanciero_SANDBOX` is still pending until `NOVA_BUDGET_PARITY_CONNECTION_STRING` and `NOVA_BUDGET_SANDBOX_RESET_SQL` are available.
