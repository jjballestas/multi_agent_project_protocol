---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-blocked
from: Codex
to: Arquitecto
type: QUESTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-4.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget
one_line_summary: "TASK-0253 F-NOVA-01 blocked: nova_budget_verifier has EXECUTE and sandbox role, but lacks VIEW DEFINITION on Budget.Apply_Budget_Modification."
requested_action: "Please grant VIEW DEFINITION on Budget.Apply_Budget_Modification to nova_budget_verifier, or provide a verifier-owned exact THROW attestation from the deployed definition, then re-route Codex to re-run F-NOVA-01."
question: "Can the DBA grant VIEW DEFINITION on Budget.Apply_Budget_Modification to nova_budget_verifier, or provide the exact deployed THROW set from OBJECT_DEFINITION/sys.sql_modules?"
---

task_id: TASK-0253
status: blocked
executive_summary: F-NOVA-01 remains blocked at the live sandbox permission gate. The Codex process can load both User-scope env vars without printing their values, reaches DbsFinanciero_SANDBOX as login nova_budget_verifier, and IS_ROLEMEMBER('budget_sandbox_verifier') returns 1. EXECUTE on Budget.Apply_Budget_Modification returns 1, but VIEW DEFINITION returns 0 and OBJECT_DEFINITION length is NULL, so the required exact THROW re-verification via deployed definition cannot be completed. Non-blocking hallazgo #5 was remediated in product commit 7cc845e by renaming ReadOnlySqlOptions to BudgetSqlOptions and switching the config section to BudgetSql.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget commit 7cc845e; Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-4.md.
gates: Product live probe: db=DbsFinanciero_SANDBOX, login=nova_budget_verifier, role_member=1, exec_perm=1, view_def=0, definition_len=NULL. dotnet test NOVA.sln PASS 35 tests with known NU1903 Microsoft.OpenApi warning. npm test --prefix apps/nova-web PASS. node --check apps\nova-web\src\main.js NOT APPLICABLE/FAIL because the app entrypoint is TypeScript main.tsx, not main.js.
next_recommended: Grant VIEW DEFINITION on Budget.Apply_Budget_Modification to nova_budget_verifier or provide a verifier-owned exact THROW attestation from sys.sql_modules/OBJECT_DEFINITION, then re-run F-NOVA-01 before moving TASK-0253 to in_review.
risks: The 8 live Given/When/Then criteria cannot be accepted without F-NOVA-01 because hard-coded THROW expectations would be unverifiable against the deployed proc.
