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
