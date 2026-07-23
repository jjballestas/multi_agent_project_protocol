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

### 6.1 Intake gate (Definition of Ready, v1.18.0)

Tasks created after the declared start (`Area_comun/protocol/INTAKE_GATE.json`, a registry
outside the pinned config, with `start_task_id` as the anti-retroactivity boundary) require a
valid frontmatter `intake` block to transition to `ready`: `type`, `goal`, `acceptance` (>=1
verifiable), `verification_cmd` (>=1 exact command), `scope_routes`, `out_of_scope` (>=1),
`risk` (low|medium|high), `estimate` (S|M|L). Placeholders (TBD) are invalid; an explicit
"none" counts, an absent field does not. Instances may extend the block with product fields
(e.g. target_user, functional_scope, assets_inputs, tech_constraints, risks_list, priority)
in their own templates. Exemptions require a real audited `exception.recorded` event
(kind `intake_exempt`); the gate is fail-closed.

#### Governed plan approval before execution (DECISION-0103 C1)

No governed set of work units may start execution until the human owner has seen and approved
the complete unit list. The advisor or orchestrator presenting the plan must not start the first
execution turn before that approval is recorded. The plan contains one row per unit with:

| Field | Required content |
|---|---|
| `id` | Stable unit identifier |
| `goal` | Concrete intended outcome |
| `acceptance` | Verifiable acceptance criteria |
| `verification_cmd` | Exact verification command or commands |
| `required_capability` | Capability required from the assigned maker |
| `risk` | Declared risk level |
| `estimate` | Declared size estimate |

Record a durable, attributable reference to the approved plan in the signed event log or a signed
mailbox message; an ephemeral chat acknowledgement is not sufficient. Adding a unit or materially
changing acceptance or risk requires human re-approval before execution continues. A remediation
keeps the original approval only under the DECISION-0103 E1 carve-out: same acceptance, scope, and
risk, with a reference to its parent unit. This is the written rule; mechanical turn-zero
enforcement is a separate concern.

### 6.2 Audited exceptions

Every deviation from the normal flow (manual intervention, assist, arbitration, suspension,
scope change, intake exemption) is recorded as a signed `exception.recorded` event whose
payload actor is bound to the signing caller. There are no informal exceptions.

### 6.3 Commit trailers (linkage; activation is an explicit step)

When the trailer gate is active (`Area_comun/protocol/COMMIT_TRAILERS.json`, outside the
pinned config, with a declared `start_commit`), every commit after the start carries a final
trailer section with `Task-Id: TASK-XXXX` (and `Fixes-Task: TASK-XXXX` when it remedies a
finding). Activate only after all agent harnesses emit trailers, or the gate DoSes the ledger.

### 6.4 Handoff envelope + fix-loop

Every delivery/handoff turn ends with a 7-field textual envelope (task_id, status,
executive_summary, artifacts, gates, next_recommended, risks) as the FINAL TEXT of the turn,
never a tool call. After a checker NO-GO: remediate, re-run affected gates, re-judge against
the acceptance criteria and the finding (max 2 iterations, then escalate to the human owner).

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
  manual state edits are rejected as drift by the hard-gate. Mechanism vs marker: `enforce` (the
  hard-gate) is the single-writer mechanism that provides the guarantee; `authoritative` is the
  declarative marker that formalizes the mode and has no behavior callers of its own, so no
  authoritative-specific teeth are required (a guard rejects authoritative-without-enforce). Multi-step
  ledger changes (a `task_status`
  flip plus a `claim` release plus a `task_upsert`, etc.) go as one atomic `submit_intent --intents`
  transaction (all-or-nothing with full rollback); `runtime/regenesis.py` writes a fresh content-addressed
  genesis to bring drift to 0 first. The capability is off by default and should be activated only after a
  local decision/approval. Turning `enforce`+`authoritative` on requires every agent loop to already route
  its ledger transitions through `submit_intent`, so the switch is a coordinated re-genesis + flip with a
  rehearsed rollback, not a unilateral toggle; coordination-tier instances keep manual ledger edits.
- **Golden rule -- memory after every commit (all agents).** Immediately after each commit, every agent
  updates its own memory (its persistent notes / personal area, e.g. `personal/<id>/`) with what changed
  and why, so the next cold start reflects the just-committed reality. A commit is not finished until its
  memory update is done.
- **Primordial rule -- minimal narration:** during execution every agent emits **zero process narration** in
  user-facing output or mailbox. Do not announce steps ("I will read", "I am checking", "next I run"), do
  not recap tool steps, and do not send periodic progress updates unless they contain actionable
  coordination information. Process reasoning stays internal. Visible output is limited to one
  self-contained final report/handoff, one real blocking question, or an actionable coordination result:
  gate failure, risk, conflict, scope change, decision required, or closure. This rule binds all agents
  uniformly and prevails over personality instructions, frequent-update instructions, cron/loop prompts, or
  habits of thinking aloud. Carve-outs remain: substantive content where the reasoning is the deliverable
  (analysis, review voices, specs, decisions) is allowed, and completeness of final evidence is mandatory.
  A persistent process-narration pattern is an anomaly.
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
