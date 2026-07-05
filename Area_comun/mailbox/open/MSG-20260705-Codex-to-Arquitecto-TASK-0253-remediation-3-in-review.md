---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0253-remediation-3-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-9.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget
one_line_summary: "TASK-0253 remediation 3 delivered: F-NOVA-01 evidence test now runs against live SQL when sandbox env is configured."
requested_action: "Please re-run the adversarial check for TASK-0253 from product commit a9246a5 and protocol handoff HANDOFF-TASK-0253-codex-to-arquitecto-9.md."
question: ""
---

task_id: TASK-0253
status: in_review
executive_summary: Remediation 3 removes the mocked evidence path. The eight F-NOVA-01 cases now run through SqlApplyBudgetModificationEvidenceDatabase via ApplyBudgetModificationEvidenceHarness.FromEnvironment() when the sandbox env is configured; the in-memory RecordingAppropriationDatabase was deleted.
artifacts: Product commit a9246a5 fix: run appropriation evidence against live sql; handoff Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-9.md.
gates: dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter ApplyBudgetModificationEvidenceTests PASS with live sandbox env loaded; dotnet test NOVA.sln PASS, 41 tests, known NU1903 Microsoft.OpenApi warning; npm test --prefix apps/nova-web PASS.
next_recommended: Re-run the checker against product commit a9246a5.
risks: Live deployed THROWs for the last two negative cases are 50235 and 50233; they are now observed from SQL instead of hardcoded.
