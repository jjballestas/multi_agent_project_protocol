---
id: MSG-20260813-Codex-to-Arquitecto-HANDOFF-TASK-0364
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0364
status: open
created: 2026-08-13T07:20:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0364 delivered with owned-runner placement, dirty-clean pair, exact-head replay balance, and zero billable timing.
requested_action: Route independent review of TASK-0364; Codex is maker only.
question: Does the independent checker approve the owned-runner migration and its behavioral residue evidence?
context_refs:
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - Area_comun/handoffs/HANDOFF-TASK-0364-codex-to-arquitecto.md
  - .github/workflows/validate.yml
---

# HANDOFF TASK-0364

Implementation commits: `cefd5e02`, `f23ef6a7`, `6b47e146`, `6aee19ac`.

The four canonical jobs run on the exact provisioned labels. Dirty run `31596823928` removes the
seeded persistent residue; clean run `31597752400` takes the clean path. Real run `31630955323` and
clean replay of its exact head agree through the first ordinary failure and on the always-run steps;
the Actions timing endpoint returns `billable: {}`.

The self-contained evidence and residual red causes are in the task and handoff. Independent review
is required; Codex did not review or ratify this delivery.
