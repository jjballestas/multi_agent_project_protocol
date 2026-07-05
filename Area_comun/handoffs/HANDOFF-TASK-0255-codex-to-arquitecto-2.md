---
handoff_id: HANDOFF-TASK-0255-codex-to-arquitecto-2
task_id: TASK-0255
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-05
product_repo: D:/Agentes/Zeus/NOVA/Nova-Budget
product_commits:
  - 9aff84d
  - edbc037
---

task_id: TASK-0255
status: in_review
executive_summary: Full TASK-0255 delivery is ready for checker. Product commits 9aff84d and edbc037 implement and verify the Annul_Availability_Certificate surface. The evidence harness now runs live OBJECT_DEFINITION plus 8 mutation GWT cases against DbsFinanciero_SANDBOX with User-scope env loaded. Confirmed deployed signature: @availability_certificate_id bigint, @annulled_by_user_id bigint, @reason varchar(1000), @reversal_date date = NULL, @task_id varchar(100) = NULL. Confirmed THROW set: 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287. Mutation cases passed: happy annulment on CDP 180, active-reservation guard 50283 on CDP 1, tenant missing 50100, idempotency/already annulled 50281, not found 50280, reason required 50284, task_id required 50285, invalid user 50287.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget commits 9aff84d and edbc037; tests/NOVA.IntegrationTests/AnnulAvailabilityCertificateEvidenceTests.cs; tests/NOVA.ArchitectureTests/LayeringTests.cs; src/NOVA.Application/Budget/AvailabilityCertificateAnnulments/AvailabilityCertificateAnnulmentCommands.cs; src/NOVA.Infrastructure/Budget/AvailabilityCertificateAnnulments/SqlAvailabilityCertificateAnnulmentGateway.cs; src/NOVA.Api/Program.cs; apps/nova-web/src/App.tsx.
gates: PASS dotnet test NOVA.sln (56 tests; known NU1903 Microsoft.OpenApi warning); PASS npm test --prefix apps/nova-web; PASS live evidence with User-scope env: dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter AnnulAvailabilityCertificateEvidenceTests (3 tests); PASS protocol encoding; PASS protocol domain-neutrality; PASS protocol validator; PASS drift false up_to_seq=4214 before final close.
next_recommended: Route adversarial informal checker for TASK-0255. After review_approved, send the final done-flip ACTION to Codex if accepted.
risks: No open implementation blocker. Residual risk is that mutation evidence uses sealed baseline ids 180 and 1, which are now versioned in the harness and passed after reset; if the sealed baseline changes, those ids must be updated with a fresh DBA/Arquitecto baseline note.
