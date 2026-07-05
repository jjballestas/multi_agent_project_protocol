---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0255-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
  - Area_comun/handoffs/HANDOFF-TASK-0255-codex-to-arquitecto-1.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget
one_line_summary: "TASK-0255 in_review partial: product commit 9aff84d implements Annul_Availability_Certificate surface; live OBJECT_DEFINITION says guard THROW is 50283, not 50293."
requested_action: "Review TASK-0255 partial delivery. Decide whether the deployed active-reservation guard THROW 50283 supersedes the GO/spec expectation 50293, or whether DBA/operator must patch the proc before mutation GWT completion."
question: "Should TASK-0255 criteria be aligned to deployed THROW 50283, or should the proc be patched to emit 50293 before Codex runs the full mutation GWT evidence?"
---

task_id: TASK-0255
status: in_review
executive_summary: Product commit 9aff84d implements the C#/API/UI surface and real SQL definition-evidence harness for Budget.Annul_Availability_Certificate. Live OBJECT_DEFINITION confirms signature @availability_certificate_id bigint, @annulled_by_user_id bigint, @reason varchar(1000), @reversal_date date = NULL, @task_id varchar(100) = NULL and THROW set 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287. The active-reservation guard is 50283 in the deployed proc, not 50293.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget commit 9aff84d; Area_comun/handoffs/HANDOFF-TASK-0255-codex-to-arquitecto-1.md.
gates: PASS dotnet test NOVA.sln; PASS npm test --prefix apps/nova-web; PASS dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter AnnulAvailabilityCertificateEvidenceTests with User-scope env; drift false at seq 4201 before delivery close.
next_recommended: Review the 50283 vs 50293 mismatch and provide the authoritative next step for full mutation GWT evidence.
risks: Mutation GWTs are still pending sealed baseline case ids and the THROW mismatch decision.
