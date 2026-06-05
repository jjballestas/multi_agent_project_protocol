# Area_comun — Shared Entry Point

Shared, auditable state for `multi_agent_project_protocol` (the protocol dogfooding itself).

## Required Reading Order

1. `../AGENTS.md`
2. `protocol/TASK_PROTOCOL.md`
3. `protocol/COMMUNICATION_PROTOCOL.md`
4. `state/PROJECT_STATE.json`
5. `state/TASK_INDEX.json`
6. `state/CLAIMS.json`
7. `mailbox/open/`
8. the concrete task in `tasks/`

## Folder Map

| Folder | Purpose |
|--------|---------|
| `protocol/` | Method, task, communication and handoff contracts (also the shipped product). |
| `state/` | Live project state, task index and claims (`*.json`). `*.template.json` are shipped masters. |
| `mailbox/` | Lightweight messages between agents. |
| `tasks/` | One file per task. |
| `handoffs/` | Self-contained formal deliveries. |
| `reports/` | Human-readable process reports. |
| `artifacts/` | Shared outputs ready for use. |
| `contracts/` | Project-specific contracts (kept empty: this repo is the neutral core). |
| `decisions/` | Append-only decisions. |

## Minimum Rules

- Check `TASK_INDEX.json`, `CLAIMS.json` and `mailbox/open/` before editing.
- Create/update an active claim before creating or editing any shared file, including drafts.
- Do not edit another owner's active claim.
- Record blocking ambiguity as `blocked` with one concrete question.
- Keep the protocol core **domain-neutral**; protocol/compatibility changes need a decision.
