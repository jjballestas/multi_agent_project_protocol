# AGENTS.md - Shared source of truth for dotnet_enterprise_instance

> This file is the project contract. All agents and the human operator read and obey it.
> If a one-off instruction conflicts with this file, this file wins unless the human owner
> explicitly overrides it and records a decision in `Area_comun/decisions/`.
>
> Last updated: 2026-06-05. Maintainer: Claude + operador humano.

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

`Validate adoption of the dotnet_enterprise professional profile over the neutral core.`

Description:

`Controlled example instance for TASK-0006: core plus dotnet_enterprise profile.`

## 2. Current Phase and Scope

- Phase id: `P1`
- Phase name: `Profile adoption`
- Phase goal: `Demonstrate a valid instance that adopts dotnet_enterprise.`

In scope:

`Project-specific work declared by the instance.`

Out of scope:

`Work not explicitly approved for this instance.`

## 3. Agent Roles

`- `Claude`: Architect / orchestrator.
- `Codex`: Implementation specialist.
- `operador humano`: Human owner.`

Suggested role model:

| Agent | Main role | Does | Does not do |
|-------|-----------|------|-------------|
| `Claude` | Architect / orchestrator | Designs, reviews, decomposes tasks, maintains shared method artifacts | Does not own implementation-only work unless assigned |
| `Codex` | Implementation specialist | Scaffolding, patches, scripts, tests, CI, concrete technical proposals | Does not change protocol or critical boundaries without a decision |
| `operador humano` | Human owner | Approves project policy, critical transitions and business decisions | - |

## 4. Hard Project Boundaries

These are domain-specific and must be completed by the project instance:

`No secrets committed. dotnet_enterprise profile boundaries apply when adopted.`

Changes to these boundaries require a decision in `Area_comun/decisions/` and any human
approval listed in `Profile adoption and security boundary changes require human owner approval.`.

## 5. Stack Decisions and Quality Gates

Stack decisions:

`Adopts the optional dotnet_enterprise profile for .NET enterprise practices.`

Quality gates:

`Collaboration state validator green; dotnet_enterprise profile gates apply where relevant.`

Human approval points:

`Profile adoption and security boundary changes require human owner approval.`

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

`Complete this section with the instance repository map.`

Recommended shared structure:

```text
dotnet_enterprise_instance/
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
`-- project_code_or_docs/
```

## 9. Base Definition of Done

A task is not done until:

1. Its specific definition of done is satisfied.
2. It does not violate `No secrets committed. dotnet_enterprise profile boundaries apply when adopted.`.
3. It introduces no secrets.
4. It creates a self-contained handoff if another agent must review or use the output.
5. It updates `TASK_INDEX.json`.
6. Any unresolved ambiguity is recorded as `blocked` with a concrete question.
