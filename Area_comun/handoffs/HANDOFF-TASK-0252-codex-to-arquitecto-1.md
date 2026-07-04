# HANDOFF TASK-0252 - Codex to Arquitecto

task_id: TASK-0252
status: in_review
executive_summary: Product commit dc04bd8 adds the Nova-Budget parity harness for exec-vs-endpoint checks against the sandbox verifier path. The harness uses role marker budget_sandbox_verifier, refuses non-SANDBOX databases, returns paridad_exec_vs_endpoint as pass/fail/NA, and resets the sealed sandbox baseline before each arm. It does not include Annul_Availability_Certificate or Annul_Commitment. DBA hardening relay is documented: keep IF DB_NAME() NOT LIKE '%SANDBOX%' THROW in source SQL.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.IntegrationTests/BudgetParityHarnessTests.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/docs/budget-parity-harness.md; product commit dc04bd8 test: add budget parity harness
gates: dotnet test NOVA.sln PASS (26 tests; known NU1903 Microsoft.OpenApi warning); npm test --prefix apps/nova-web PASS (typecheck + Vitest 1 test); live SQL parity returned NA by design unless NOVA_BUDGET_PARITY_CONNECTION_STRING and NOVA_BUDGET_SANDBOX_RESET_SQL are provided from secret store.
next_recommended: Analista formal gate should inspect the harness contract and, when secrets/reset SQL are available, run the live parity path against DbsFinanciero_SANDBOX with nova_budget_verifier.
risks: Live parity was not executed in this session because no secret-backed connection string or sealed-baseline reset SQL was present in the environment. The product worktree still has unrelated untracked docs/documentacion-tecnica/ left untouched.
