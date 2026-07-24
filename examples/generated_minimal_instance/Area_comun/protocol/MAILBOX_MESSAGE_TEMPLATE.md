# MAILBOX_MESSAGE_TEMPLATE.md - Compact Mailbox Message

Save as `Area_comun/mailbox/<open|answered|archived>/MSG-<YYYYMMDD>-<from>-to-<to>-<slug>.md`.

Compact and referential (DECISION-0005): one intention per message; if it needs an answer, one
concrete `question`. Reference artifacts by ID and path in `*_refs`; do not paste long content that
already lives in files.

```markdown
---
message_id: MSG-YYYYMMDD-<from>-to-<to>-<slug>
type: ACK | FYI | OK | REVIEW | CHANGES | BLOCKED | DONE | DECISION_REQUIRED | HUMAN_REQUIRED
task_id: TASK-XXXX | none
from: Claude | Codex | operador humano
to: Claude | Codex | operador humano
requires_response: true | false
response_owner: <agent> | none
subject: <short subject>
one_line_summary: <one line, the delta/decision/block/request>
requested_action: <exact action expected, or none>
question: <single concrete question, or none>
context_refs:
  - <ID or path to canonical artifact already holding the context>
changed_refs:
  - <path(s) changed by this work, or none>
validation_refs:
  - <command/result or report path proving the claim, or none>
deadline_or_blocking_level: none | low | normal | high | blocking
status: open | answered | archived
---

# <subject>

<Body: only the delta. Reference, do not recap. If this grows long, move it to an
artifact/handoff/report and link it here.>
```

## Minimal frontmatter (SPEC-0025, DECISION-0008 §3)

To cut frontmatter overhead, emit only the **obligatory set** and **omit** any optional field that
would be `none` / empty / a default. Omitted fields are assumed at their default; the validator does
not require them (back-compat: the full frontmatter above stays valid).

- **Obligatory always:** `message_id`, `type`, `task_id`, `from`, `to`, `status`, `one_line_summary`.
- **Obligatory only if `requires_response: true`:** `response_owner`, `requested_action`, `question`.
- **Omit when `none`/empty/false-by-default:** `requires_response` (⇒ false), `response_owner`,
  `subject`, `requested_action`, `question`, `context_refs`, `changed_refs`, `validation_refs`,
  `deadline_or_blocking_level`.

Minimal FYI example (no response needed):

```markdown
---
message_id: MSG-YYYYMMDD-<from>-to-<to>-<slug>
type: FYI
task_id: TASK-XXXX | none
from: Claude
to: Codex
status: open
one_line_summary: <one line, the delta>
---

# <subject>

<Body: only the delta.>
```

## Rules (DECISION-0005)
- One intention per message; if `requires_response: true`, exactly one `question`.
- Use `context_refs` instead of repeating context from AGENTS/PROJECT_STATE/TASK_INDEX/decisions/specs/tasks/handoffs.
- Long content → `artifacts/`, `specs/`, `reports/` or `decisions/`; the message only links it.
- Close the loop with a code reply (`OK` / `CHANGES` / `BLOCKED` / `ACK` / `FYI`) unless a detailed
  review is needed (then use a handoff).
- Group replies only within the same `task_id`.
