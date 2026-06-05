# AGENTS.md - Shared source of truth for {{PROJECT_NAME}}

> This file is the project contract. All agents and the human operator read and obey it.
> If a one-off instruction conflicts with this file, this file wins unless the human owner
> explicitly overrides it and records a decision in `Area_comun/decisions/`.
>
> Last updated: {{LAST_UPDATED}}. Maintainer: {{MAINTAINER}}.

## 0. How to Start

An agent entering cold can operate by reading only:

1. `AGENTS.md`.
2. `Area_comun/` in this order:
   - `Area_comun/README.md`
   - `Area_comun/protocol/TASK_PROTOCOL.md`
   - `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.json`
   - `Area_comun/mailbox/open/`
   - the concrete file in `Area_comun/tasks/`.

Never assume another agent knows your context. Every task and handoff must be self-contained.

## 1. Project Goal

`{{PROJECT_GOAL}}`

Description:

`{{PROJECT_DESCRIPTION}}`

## 2. Current Phase and Scope

- Phase id: `{{PHASE_ID}}`
- Phase name: `{{PHASE_NAME}}`
- Phase goal: `{{PHASE_GOAL}}`

In scope:

`{{IN_SCOPE}}`

Out of scope:

`{{OUT_OF_SCOPE}}`

## 3. Agent Roles

`{{AGENT_ROLES}}`

Suggested role model:

| Agent | Main role | Does | Does not do |
|-------|-----------|------|-------------|
| `{{AGENT_ARCHITECT}}` | Architect / orchestrator | Designs, reviews, decomposes tasks, maintains shared method artifacts | Does not own implementation-only work unless assigned |
| `{{AGENT_IMPLEMENTER}}` | Implementation specialist | Scaffolding, patches, scripts, tests, CI, concrete technical proposals | Does not change protocol or critical boundaries without a decision |
| `{{HUMAN_OWNER}}` | Human owner | Approves project policy, critical transitions and business decisions | - |

## 4. Hard Project Boundaries

These are domain-specific and must be completed by the project instance:

`{{DOMAIN_CRITICAL_BOUNDARIES}}`

Changes to these boundaries require a decision in `Area_comun/decisions/` and any human
approval listed in `{{HUMAN_APPROVAL_POINTS}}`.

## 5. Stack Decisions and Quality Gates

Stack decisions:

`{{STACK_DECISIONS}}`

Quality gates:

`{{QUALITY_GATES}}`

Human approval points:

`{{HUMAN_APPROVAL_POINTS}}`

## 6. Task Lifecycle

Task status lifecycle:

```text
proposed -> ready -> claimed -> in_progress -> in_review -> done
                              -> blocked
                              -> cancelled
```

The task status must match in two places:

- `Area_comun/tasks/TASK-XXXX-*.md`
- `Area_comun/state/TASK_INDEX.json`

## 7. Collaboration Protocol

- Work is decomposed into small, verifiable, assignable tasks.
- One task has one owner.
- Shared work lives in `Area_comun/`.
- Private drafts reside in each agent private folder if the project uses them.
- Before editing, check `TASK_INDEX.json`, `CLAIMS.json` and `mailbox/open/`.
- If a route is covered by another owner active claim, do not edit it.
- Ambiguity becomes `blocked` plus one concrete question.
- Any protocol or critical-boundary change requires a recorded decision.

## 8. Repository Map

`{{REPO_MAP}}`

Recommended shared structure:

```text
{{PROJECT_NAME}}/
|-- AGENTS.md
|-- Area_comun/
|   |-- README.md
|   |-- protocol/
|   |-- state/
|   |-- tasks/
|   |-- mailbox/
|   |-- handoffs/
|   |-- reports/
|   |-- artifacts/
|   |-- contracts/
|   `-- decisions/
`-- {{PROJECT_CODE_OR_DOCS}}
```

## 9. Base Definition of Done

A task is not done until:

1. Its specific definition of done is satisfied.
2. It does not violate `{{DOMAIN_CRITICAL_BOUNDARIES}}`.
3. It introduces no secrets.
4. It creates a self-contained handoff if another agent must review or use the output.
5. It updates `TASK_INDEX.json`.
6. Any unresolved ambiguity is recorded as `blocked` with a concrete question.
