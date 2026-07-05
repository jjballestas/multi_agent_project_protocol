---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0253-remediation-1-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-2.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget
one_line_summary: "TASK-0253 remediation 1 code is committed; F-NOVA-01 live sandbox evidence is blocked on credentials."
requested_action: "Provide NOVA_BUDGET_PARITY_CONNECTION_STRING and NOVA_BUDGET_SANDBOX_RESET_SQL, or run the mandatory F-NOVA-01 sandbox verification from an environment with budget_sandbox_verifier access. Code fixes for NO-GO items 2, 3, 4 and minor TASK-0251 copy-paste are in product commit 00a3f47."
question: "Can Arquitecto provide the secret-backed sandbox connection/reset inputs or run the mandatory F-NOVA-01 sandbox verification from an environment with budget_sandbox_verifier access?"
---

task_id: TASK-0253
status: blocked
executive_summary: Remediation 1 delivered in Nova-Budget commit 00a3f47. The code now queries Budget.vw_Initial_Budget_Line_Balance for preview/result balances, maps documented SQL THROW numbers to specific ProblemDetails business rules, adds API coverage for the mapping, adds unit coverage for unbalanced transfer classification, and replaces the fixed UI payload with operator-editable inputs.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget commit 00a3f47; Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-2.md.
gates: dotnet test NOVA.sln PASS 35 tests with known NU1903; npm test --prefix apps/nova-web PASS; sqlcmd localhost sandbox probe FAIL with SSPI credential error; sandbox env vars absent.
next_recommended: Provide/run the required live F-NOVA-01 sandbox verification, then return TASK-0253 to in_progress for final re-delivery.
risks: Mandatory live sandbox criteria remain unproven by Codex in this session due missing credentials.
