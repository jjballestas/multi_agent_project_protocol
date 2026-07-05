---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-retry-2-blocked
from: Codex
to: Arquitecto
type: QUESTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-5.md
one_line_summary: "TASK-0253 F-NOVA-01 retry-2 blocked: proc definition visible, but Budget.Budget_Modification_Line_List denies TVP execution."
requested_action: "Please grant the permission required to instantiate Budget.Budget_Modification_Line_List to budget_sandbox_verifier/nova_budget_verifier, then re-route Codex to re-run F-NOVA-01."
question: "Can the DBA grant EXECUTE/REFERENCES as required for Budget.Budget_Modification_Line_List to the verifier login or role?"
---

task_id: TASK-0253
status: blocked
executive_summary: F-NOVA-01 advanced past VIEW DEFINITION but is blocked at the next live sandbox permission gate. The deployed proc definition is visible: DbsFinanciero_SANDBOX, role_member=1, view_def=1, exec_perm=1, proc_len=9412. Exact THROW set found in Budget.Apply_Budget_Modification is 50230,50231,50232,50233,50234,50235,50236,50237,50238,50239,50240,50241,50242,50243. Trigger scan found Budget.trg_budget_adjustment__validate_open_year with 50212; no visible definition found for 50065. The first live GWT execution cannot declare the TVP because SQL Server returns permission denied on object Budget_Modification_Line_List.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget commit 75913aa; Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-5.md.
gates: Live probe PASS for env presence, sandbox DB, role membership, EXECUTE on proc, VIEW DEFINITION on proc, and exact proc THROW extraction. Live GWT BLOCKED by SQL error 229: EXECUTE permission denied on Budget.Budget_Modification_Line_List. Earlier product gates remain dotnet test NOVA.sln PASS 35 tests with known NU1903 warning and npm test --prefix apps/nova-web PASS. Protocol gates are pending after this handoff.
next_recommended: Grant EXECUTE/REFERENCES as required by SQL Server for Budget.Budget_Modification_Line_List to budget_sandbox_verifier/nova_budget_verifier, then re-run F-NOVA-01 retry-3.
risks: Without permission to instantiate the TVP, no live Apply_Budget_Modification criteria can execute, so TASK-0253 cannot move to in_review.
