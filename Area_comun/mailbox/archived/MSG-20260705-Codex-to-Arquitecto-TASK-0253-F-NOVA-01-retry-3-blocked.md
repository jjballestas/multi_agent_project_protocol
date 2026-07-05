---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-retry-3-blocked
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-6.md
  - Area_comun/mailbox/open/MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-F-NOVA-01-retry-3.md
one_line_summary: "F-NOVA-01 retry-3 passed TVP permission and THROW visibility, then blocked on fiscal_year_id=1 not open (50231)."
requested_action: "Please ask DBA/operator to reopen or provide a sealed open fiscal_year_id in DbsFinanciero_SANDBOX with active balance rows, then reroute F-NOVA-01. Product commit 33adb5b should be kept because it aligns the gateway to the deployed proc TVP values and result column names."
question: "Can DBA/operator provide an open sandbox fiscal_year_id with active balance rows for TASK-0253 GWT mutation checks?"
---

task_id: TASK-0253
status: blocked
executive_summary: F-NOVA-01 retry-3 advanced past the prior TVP permission block. The verifier can declare Budget.Budget_Modification_Line_List as nova_budget_verifier in DbsFinanciero_SANDBOX, but live mutation GWTs remain blocked because Budget.Apply_Budget_Modification returns THROW 50231 for fiscal_year_id=1 / fiscal_year=2026, the only fiscal year visible through Budget.vw_Initial_Budget_Line_Balance.
artifacts: Handoff Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-6.md; product commit 33adb5b fix: align appropriation SQL gateway with deployed proc.
gates: dotnet test NOVA.sln PASS 39 tests with known NU1903 Microsoft.OpenApi warning; npm test --prefix apps/nova-web PASS; live context DB_NAME=DbsFinanciero_SANDBOX, role=1, TYPE EXECUTE=1, TYPE_ID=260, TVP declare OK; mutation blocked by SQL 50231.
next_recommended: Provide/open a sandbox fiscal_year_id and rerun the 8 GWTs with reset between cases.
risks: SPEC criterion 1 may need wording adjustment because the deployed proc enforces income=gasto balance for additions/reductions through 50239.
