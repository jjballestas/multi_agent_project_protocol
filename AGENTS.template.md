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
- Private drafts reside in each participant's personal area `personal/<id>/`.
- Onboarding rule: every participant (agent or human) that registers creates its personal area at
  `personal/<id>/` (same `<id>` as in the agent registry / agents block).
- Before editing, check `TASK_INDEX.json`, `CLAIMS.json` and `mailbox/open/`.
- Before creating or editing any file in a shared route, create/update an active claim that lists
  that route in `scope`; this includes new drafts and temporary files that remain in the workspace.
- If a route is covered by another owner active claim, do not edit it.
- Ambiguity becomes `blocked` plus one concrete question.
- Anomaly notification: an agent that detects an anomaly or inconsistency in another participant's work
  or in shared state (e.g. an incomplete handoff-release, a status that contradicts the claims/mailbox, a
  stale or orphaned claim, a missing or mismatched artifact) must notify the responsible owner via
  `mailbox/open/` with a concrete, actionable message, and record it. It must not silently fix routes
  under another owner's active claim, nor leave the anomaly unsignaled; if the fix needs those routes, it
  asks the owner (or the human) and waits.
- Anti-collision rule for concurrent ledger writes: when more than one agent may write the shared ledger
  (state JSON, mailbox) in overlapping windows, every writer: (1) prepares drafts in its personal area
  `personal/<id>/` while the peer is busy; (2) writes the ledger only in a safe window (peer has no active
  claim on the routes and the working tree shows no half-written peer delivery; otherwise it waits and
  retries); (3) makes ledger closes/enqueues in a single atomic script; (4) never lists a not-yet-created
  artifact in a claim `scope` (artifacts-before-claim); (5) stages explicit paths when committing, never
  broad directories, and commits only a consistent snapshot with green gates; (6) writes any
  mailbox/artifact assertion only after the ledger backs it (the "DONE" FYI after the status flip, the
  "ready" GO after the task is recorded); (7) promotes one task at a time with a GO + ETA.
- Runtime-authoritative mode: only runtime-tier instances with
  `event_state.enabled/materialize/enforce/authoritative:true` treat the runtime as the writer of
  `Area_comun/state/*.json`. In that mode, transitions go through `runtime/submit_intent.py`
  (`task_status`, `task_upsert`, `claim`, `decision`) with caller-provided `timestamp`/`commit`, and
  manual state edits are rejected as drift by the hard-gate. Multi-step ledger changes (a `task_status`
  flip plus a `claim` release plus a `task_upsert`, etc.) go as one atomic `submit_intent --intents`
  transaction (all-or-nothing with full rollback); `runtime/regenesis.py` writes a fresh content-addressed
  genesis to bring drift to 0 first. The capability is off by default and should be activated only after a
  local decision/approval. Turning `enforce`+`authoritative` on requires every agent loop to already route
  its ledger transitions through `submit_intent`, so the switch is a coordinated re-genesis + flip with a
  rehearsed rollback, not a unilateral toggle; coordination-tier instances keep manual ledger edits.
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
|-- personal/<id>/   (per-participant private areas; created on registration)
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
