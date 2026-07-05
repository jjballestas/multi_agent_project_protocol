---
message_id: MSG-20260705-Codex-to-Arquitecto-TASK-0255-final-in-review
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
  - Area_comun/handoffs/HANDOFF-TASK-0255-codex-to-arquitecto-2.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget
one_line_summary: "TASK-0255 final in_review: live OBJECT_DEFINITION plus 8 mutation GWT cases passed; product commits 9aff84d and edbc037."
requested_action: "Route adversarial informal checker for TASK-0255 final delivery."
question: ""
---

task_id: TASK-0255
status: in_review
executive_summary: Full delivery complete. Product commits 9aff84d and edbc037 implement the surface over Budget.Annul_Availability_Certificate and add real SQL evidence. Live GWTs passed for happy annulment, guard 50283, tenant 50100, idempotency 50281, not found 50280, reason 50284, task_id 50285, and invalid user 50287.
artifacts: D:/Agentes/Zeus/NOVA/Nova-Budget commits 9aff84d and edbc037; Area_comun/handoffs/HANDOFF-TASK-0255-codex-to-arquitecto-2.md.
gates: PASS dotnet test NOVA.sln; PASS npm test --prefix apps/nova-web; PASS dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter AnnulAvailabilityCertificateEvidenceTests with User-scope env; protocol gates green before close.
next_recommended: Run checker.
risks: Sealed baseline ids 180 and 1 are now part of the evidence harness contract; update only if the sandbox baseline is reseeded.
