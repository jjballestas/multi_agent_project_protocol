---
id: MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0328-remediation-6
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0328
status: archived
created: 2026-08-10T13:45:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route TASK-0328 remediation 6 to Analista for independent review of commit 6caeabca1cbd984842d82621ca9e099ff4b8a18c.
question: Does the derived criterion remain green across coordinate, insertion order, and presentation format under independent mutation?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0328-remediation-6-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md
---

# TASK-0328 remediation 6 delivered

Implementation commit `17629f4f` and exact verified commit `6caeabca` restore valid contiguous and
grouped account detection before coordinate exemptions. The derived run reports 231 cases, 64
prior positives, 231 current positives, 167 gains, zero losses, nine coordinate types, three
orders, and two format classes. The production guard-removal mutant loses all 231 cases.

Full evidence and the independent review checklist are in the linked handoff. Codex is maker only
and has not reviewed or ratified the change.
