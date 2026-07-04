---
message_id: MSG-20260704-Codex-to-Arquitecto-TASK-0250-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0250-p21-read-model-parametros.md
  - Area_comun/handoffs/HANDOFF-TASK-0250-codex-to-arquitecto-1.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget commit f2be4e807a3a3579969bd02fdec9363bcb8c61c9
one_line_summary: "TASK-0250 remediation 1 delivered to in_review; request separate-session adversarial informal re-review."
requested_action: "Route the separate-session adversarial informal 12-point re-review for TASK-0250 remediation 1. If approved, ratify hub gates; if NO-GO, send Codex a concrete ACTION for fix-loop 2/2."
question: "Can you route the separate-session adversarial informal re-review for TASK-0250 remediation 1 and return GO/NO-GO?"
---

task_id: TASK-0250
status: in_review
executive_summary: Implemented the Nova-Budget budget parameters read model for accounts, funding sources, account-funding-source pairs, investment projects, and document series, then completed fix-loop 1 after the separate-session NO-GO. Production DI now registers SqlBudgetParametersGateway against ReadOnlySqlOptions.ConnectionString and canonical Budget.vw_* reads; the former in-memory production gateway was removed. The API exposes the five requested GET endpoints under /api/budget/parameters, validates tenant_id/fiscal_year_id with ProblemDetails, exposes is_active and catalog filters, and declares the vw_Document_Series gap on document-series rows. The front now calls the five API endpoints with vigencia/is_active filters and renders returned row counts. Product commit: f2be4e807a3a3579969bd02fdec9363bcb8c61c9.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Api/Program.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Application/Budget/Parameters/ParameterQueries.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Contracts/Budget/Parameters/ParameterDtos.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Infrastructure/Budget/Parameters/SqlBudgetParametersGateway.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Infrastructure/NOVA.Infrastructure.csproj; D:/Agentes/Zeus/NOVA/Nova-Budget/apps/nova-web/src/App.tsx; D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.IntegrationTests/ApiInfrastructureTests.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.UnitTests/BudgetParametersServiceTests.cs; D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.ArchitectureTests/LayeringTests.cs; Area_comun/handoffs/HANDOFF-TASK-0250-codex-to-arquitecto-1.md.
gates: PASS - clean-clone front pre-UI gate: git clone . C:/Users/johnb/AppData/Local/Temp/nova-budget-clean-7bbd86a6670e4ffa9f43434b1dfb3bec && npm ci --prefix apps/nova-web && npm test --prefix apps/nova-web. PASS - dotnet test NOVA.sln (16 tests; known NU1903 Microsoft.OpenApi 2.3.0 warning). PASS - npm test --prefix apps/nova-web (1 test). PASS - clean-clone post-fix front gate: git clone . C:/Users/johnb/AppData/Local/Temp/nova-budget-clean-17a50a83fe4c477e9d1ad0e63f47251c && npm ci --prefix apps/nova-web && npm test --prefix apps/nova-web. Earlier scaffold smoke on port 5088 passed before the SQL gateway replacement; live DB smoke was not run because no DbsFinanciero connection string/capability was available in this session.
next_recommended: Run the separate-session adversarial informal 12-point review, including live sys.columns/OBJECT_DEFINITION and SELECT count checks against DbsFinanciero for the vw_* objects, then return GO/NO-GO to Codex for fix-loop or to Arquitecto for ratification.
risks: Live parity against deployed views remains the main review risk because the maker session could not access DbsFinanciero. Cache-confound: this was run in the same Codex runtime class as recent baseline work; no separate adversarial context was used by the maker.
