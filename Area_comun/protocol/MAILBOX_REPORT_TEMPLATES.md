# Mailbox report templates

These templates cover the session-lane assignment and delivery reports defined by
DECISION-0103 C2/C4. Copy a complete example and replace placeholders without changing the
shape of `obstacles`.

## Common rules

- Use ASCII only in `Area_comun/mailbox/`.
- Every new `REPORTE` MUST declare at least one adoption anchor: `date`, `created_at`, or
  `report_schema_version: "1.0"`. The templates use `report_schema_version`; do not remove it.
  Without any anchor, the compatibility rule treats the message as historical.
- `friction_count` is a non-negative integer. Use `0` only when `obstacles: []`. A positive
  count requires a non-empty list.
- Each obstacle has exactly `what`, `root_cause`, `resolution`, and `recurrence_risk`.
  `recurrence_risk` is one of `low`, `medium`, or `high`. This is the same shape and enum as
  `runtime/turn_schema.json`; do not rename, add, or omit fields.
- Set `requires_response: true` only when an answer is required. Then include
  `response_owner`, `requested_action`, and one concrete `question`.

## Assignment report template

The assignment report exposes existing `routing_decision` data. `required_capability` comes
from `routing_decision.required_capability`; `candidate_agents`, `candidates`, `filtered`, and
`selected` come from `routing_decision.explanation`. The report does not introduce a new
runtime field. The `rationale` body line is a compact rendering of those values and the
existing policy/score evidence.

```markdown
---
message_id: MSG-YYYYMMDD-<from>-to-<to>-REPORTE-assignment-<unit>
type: REPORTE
task_id: TASK-XXXX
from: <routing-agent>
to: <coordination-owner>
status: open
report_schema_version: "1.0"
report_kind: assignment
unit: <unit-id>
selected_agent: <routing_decision.explanation.selected>
required_capability: <routing_decision.required_capability>
candidate_agents:
  - <routing_decision.explanation.candidate_agents item>
candidates:
  - agent_id: <routing_decision.explanation.candidates item agent_id>
    load_score: <existing load_score>
    stable_hash: <existing stable_hash>
friction_count: 0
obstacles: []
one_line_summary: "Assignment for <unit-id> selected <agent-id> from existing routing evidence."
---

# Assignment report - <unit-id>

Selected: `<agent-id>`.
Rationale: policy `<routing_decision.policy>` required capability `<required-capability>`;
the selected candidate won using the existing candidate, filter, load-score, and stable-hash
evidence in `routing_decision.explanation`.
Filtered candidates: `<routing_decision.explanation.filtered, or []>`.
```

### Complete assignment example

```markdown
---
message_id: MSG-20260722-Router-to-Coordinator-REPORTE-assignment-UNIT-0042
type: REPORTE
task_id: TASK-0042
from: Router
to: Coordinator
status: open
report_schema_version: "1.0"
report_kind: assignment
unit: UNIT-0042
selected_agent: MakerB
required_capability: implementer
candidate_agents:
  - MakerA
  - MakerB
candidates:
  - agent_id: MakerA
    load_score: 2.0
    stable_hash: 941
  - agent_id: MakerB
    load_score: 1.0
    stable_hash: 317
friction_count: 0
obstacles: []
one_line_summary: "Assignment for UNIT-0042 selected MakerB from existing routing evidence."
---

# Assignment report - UNIT-0042

Selected: `MakerB`.
Rationale: policy `weighted_least_loaded_deterministic` required capability `implementer`;
MakerB had the lowest existing load score among the eligible candidates.
Filtered candidates: `[]`.
```

## Delivery report template

```markdown
---
message_id: MSG-YYYYMMDD-<from>-to-<to>-REPORTE-delivery-TASK-XXXX
type: REPORTE
task_id: TASK-XXXX
from: <delivery-owner>
to: <coordination-owner>
status: open
report_schema_version: "1.0"
report_kind: delivery
friction_count: <non-negative integer>
obstacles:
  - what: "<observable obstacle>"
    root_cause: "<cause>"
    resolution: "<resolution or current disposition>"
    recurrence_risk: low | medium | high
one_line_summary: "<delivered result and current lifecycle state>"
changed_refs:
  - <changed path or commit>
validation_refs:
  - <verification command and exit code>
---

# Delivery report - TASK-XXXX

<Delivery delta and evidence.>
```

### Complete delivery example with friction

```markdown
---
message_id: MSG-20260722-MakerB-to-Coordinator-REPORTE-delivery-TASK-0042
type: REPORTE
task_id: TASK-0042
from: MakerB
to: Coordinator
status: open
report_schema_version: "1.0"
report_kind: delivery
friction_count: 1
obstacles:
  - what: "The first verification run could not resolve a fixture path."
    root_cause: "The fixture used a working-directory-relative path."
    resolution: "The fixture now resolves from its own file location."
    recurrence_risk: low
one_line_summary: "TASK-0042 delivery is in_review with one resolved obstacle."
changed_refs:
  - src/component.py
validation_refs:
  - "python examples/run_cases.py: exit 0"
---

# Delivery report - TASK-0042

The bounded implementation is ready for independent review.
```

### Complete delivery example without friction

```markdown
---
message_id: MSG-20260722-MakerB-to-Coordinator-REPORTE-delivery-TASK-0043
type: REPORTE
task_id: TASK-0043
from: MakerB
to: Coordinator
status: open
report_schema_version: "1.0"
report_kind: delivery
friction_count: 0
obstacles: []
one_line_summary: "TASK-0043 delivery is in_review with no reported friction."
changed_refs:
  - docs/component.md
validation_refs:
  - "python scripts/validate_collaboration_state.py: exit 0"
---

# Delivery report - TASK-0043

The bounded documentation update is ready for independent review.
```
