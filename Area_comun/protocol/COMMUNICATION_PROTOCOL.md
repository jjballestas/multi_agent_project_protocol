# COMMUNICATION_PROTOCOL.md - Agent Communication

Source of truth: `AGENTS.md` and `TASK_PROTOCOL.md`.

## Channels

| Channel | Path | Use |
|---------|------|-----|
| Global state | `Area_comun/state/PROJECT_STATE.json` | Current phase, risks, questions and next actions. |
| Backlog | `Area_comun/state/TASK_INDEX.json` | Canonical task list. |
| Claims | `Area_comun/state/CLAIMS.json` | Soft locks over routes. |
| Mailbox | `Area_comun/mailbox/<open|answered|archived>/MSG-*.md` | Lightweight messages. |
| Handoffs | `Area_comun/handoffs/` | Formal deliveries and reviews. |
| Decisions | `Area_comun/decisions/` | Append-only decisions. |

## Anti-duplication

Before creating a document, contract, task or artifact, search existing state and shared
folders. If an equivalent source exists, reference it or add a delta. If sources contradict,
create a reconciliation message.

## Claims

Claims contain:

- `claim_id`
- `task_id`
- `owner`
- `status`: `active`, `released`, `blocked`
- `scope`
- `started_at`
- `updated_at`
- `expires_at`
- `notes`

An agent creates or updates its claim before editing shared files.

### Claim before shared draft

No agent may create, edit or leave a draft in a shared route without an active claim that lists the
route in `scope`. "Draft" includes new files, partial implementations, temporary fixtures and
scripts that remain in the workspace.

If unclaimed work is found in a shared route, do not overwrite it. Send one mailbox message with a
single ownership question and reference the exact path.

## Mailbox

Messages are stored at:

```text
Area_comun/mailbox/<status>/MSG-<YYYYMMDD>-<from>-to-<to>-<slug>.md
```

Required fields:

- `message_id`
- `from`
- `to`
- `task_id`
- `type`
- `created_at`
- `requires_response`
- `response_owner`
- `status`
- `subject`
- `requested_action`
- `context`
- `links`

Use mailbox for lightweight coordination. Use handoffs for formal task delivery or review.

For compact messages, prefer the codes and fields of `MAILBOX_MESSAGE_TEMPLATE.md` (DECISION-0005).
Historical messages with the legacy fields above remain valid.

## Compact / token-efficient communication (DECISION-0005)

Principle: **do not converse to reconstruct context.** Reference canonical artifacts by ID and path
and send only the delta, decision, block or concrete request.

- **One intention per message.** If it needs an answer, **one concrete question**.
- **Use IDs and paths** (`context_refs`), do not recite stable context already in
  AGENTS/PROJECT_STATE/TASK_INDEX/decisions/specs/tasks/handoffs.
- **Send deltas**, not full recaps.
- **Close the loop** with a code: `OK` / `CHANGES` / `BLOCKED` / `ACK` / `FYI` (or a handoff if a
  detailed review is needed).
- **Move long content** to `artifacts/`, `specs/`, `handoffs/` or `reports/`; the message links it.
- **Group replies** only within the same `task_id`.
- Avoid narrative conversations between agents.
- Compactness must **never** sacrifice traceability or clarity.

Standard codes: `ACK`, `FYI`, `OK`, `REVIEW`, `CHANGES`, `BLOCKED`, `DONE`, `DECISION_REQUIRED`,
`HUMAN_REQUIRED` (see `MAILBOX_MESSAGE_TEMPLATE.md`).
