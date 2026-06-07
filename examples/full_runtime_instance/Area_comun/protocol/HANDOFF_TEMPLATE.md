# HANDOFF_TEMPLATE.md - Self-contained Delivery Template

Save as `Area_comun/handoffs/HANDOFF-<TASKID>-<from>-to-<to>-<n>.md`.

Compact (DECISION-0005): short summary, exact paths, referenced decisions/specs, validations run,
residual risks and a single `requested_action`. Reference artifacts by ID/path; **do not copy long
content that already lives in files** — link it instead.

```markdown
---
handoff_id: HANDOFF-TASK-XXXX-<from>-to-<to>-01
task_id: TASK-XXXX
spec_id: Area_comun/specs/SPEC-XXXX-short-name.md | none
from: Claude | Codex | operador humano
to: Claude | Codex | operador humano
date: YYYY-MM-DD
status: for_review | for_implementation | for_decision | blocked
requires_response: no
response_owner: Claude | Codex | operador humano | none
acceptance_criteria_verified: yes | no | partial
tests_run:
  - command or verification
spec_deviations:
  - none
decisions_referenced:
  - DECISION-XXXX
---

# Handoff: <title>

## 1. Minimal Context
What this is, what problem it solves and which spec governed the work.

## 2. What Was Done
Files created or changed and why.

## 3. What Was Not Done
Explicit limits of the work.

## 4. Acceptance Criteria Verified
Map each acceptance criterion to evidence.

| Criterion | Evidence | Status |
|-----------|----------|--------|
| <criterion> | <file, command, output, review note> | met | partial | not met |

## 5. Tests Run
Commands, fixtures or manual checks from the `test_plan`, with results.

## 6. Spec Deviations
Any deviation from `spec_id`, why it happened and whether a decision or follow-up task is needed.
Use `none` when there are no deviations.

## 7. Requested Action
Exactly what the receiver should do.

## 8. Risks and Assumptions
Known residual risks and assumptions.

## 9. Open Questions / BLOCKED
Concrete pending questions.

## 10. Pointers
Task, spec, decisions and deliverables.
```
