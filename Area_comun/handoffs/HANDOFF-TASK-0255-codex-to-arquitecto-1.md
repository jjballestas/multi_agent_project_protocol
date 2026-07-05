---
handoff_id: HANDOFF-TASK-0255-codex-to-arquitecto-1
task_id: TASK-0255
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-05
product_repo: D:/Agentes/Zeus/NOVA/Nova-Budget
product_commit: 9aff84d
---

task_id: TASK-0255
status: in_review
executive_summary: Product commit 9aff84d implements the baseline C#/API/UI surface for Budget.Annul_Availability_Certificate: Application contracts/service, typed SQL gateway, POST /api/budget/availability-certificates/{id}/annul, GET annul-preview, UI annulment flow, ProblemDetails mapping, provenance evidence harness, and PAR-2 isolation architecture test. The deployed proc definition was re-verified via OBJECT_DEFINITION in the live sandbox with VIEW DEFINITION available. Actual signature: @availability_certificate_id bigint, @annulled_by_user_id bigint, @reason varchar(1000), @reversal_date date = NULL, @task_id varchar(100) = NULL. Actual THROW set found: 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287. Note: the deployed active-reservation guard is 50283, not the 50293 expected in the GO/spec text.
artifacts: Product commit 9aff84d; src/NOVA.Application/Budget/AvailabilityCertificateAnnulments/AvailabilityCertificateAnnulmentCommands.cs; src/NOVA.Contracts/Budget/AvailabilityCertificateAnnulments/AvailabilityCertificateAnnulmentDtos.cs; src/NOVA.Infrastructure/Budget/AvailabilityCertificateAnnulments/SqlAvailabilityCertificateAnnulmentGateway.cs; src/NOVA.Api/Program.cs; apps/nova-web/src/App.tsx; tests/NOVA.IntegrationTests/AnnulAvailabilityCertificateEvidenceTests.cs; tests/NOVA.UnitTests/AvailabilityCertificateAnnulmentServiceTests.cs; tests/NOVA.ArchitectureTests/LayeringTests.cs.
gates: PASS dotnet test NOVA.sln (55 tests; known NU1903 Microsoft.OpenApi warning); PASS npm test --prefix apps/nova-web; PASS live definition evidence with User-scope env: dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter AnnulAvailabilityCertificateEvidenceTests (2 tests); PASS drift before delivery claim seq 4201.
next_recommended: Checker should review as partial in_review, then decide whether to update the spec/GO expectation from 50293 to the deployed 50283 or ask DBA/operator whether the proc must be patched to 50293 before mutation GWTs. Mutation GWT cases still need sealed baseline case ids for happy path, active reservation, already annulled, not found, and audit-row verification.
risks: F-NOVA-01 definition evidence is real and live, but the 8 mutation GWT criteria are not completed in this delivery because the executable baseline case ids were not provided in the hub. The main actionable mismatch is deployed THROW 50283 vs expected 50293 for the active-reservation guard.
