# TASK_PROTOCOL.md - Task Workflow

Source of truth: `AGENTS.md`.

## Principles

1. Tasks are small, verifiable and assignable.
2. One task has one owner.
3. Every handoff is self-contained.
4. Ambiguity is made visible as `blocked` plus one concrete question.
5. Shared artifacts reside in `Area_comun/`.
6. Domain-specific boundaries belong to the project instance, not to this generic protocol.
7. Clarity comes before execution: specification, pipeline, acceptance criteria and test plan must
   be explicit before implementation starts.
8. Hot state files are optimized for active work; historical `done` tasks and `released` claims may
   live in `Area_comun/state/*_ARCHIVE.json`. Validators must read hot state plus archives.

## Lifecycle

```text
proposed -> ready -> claimed -> in_progress -> in_review -> done
                              -> blocked
                              -> cancelled
```

With SDD enabled for new implementable tasks, the effective path is:

```text
proposed -> spec_ready -> ready -> claimed -> in_progress -> in_review -> done
```

`spec_ready` is not a persisted status. It means the task has the required SDD fields for its
`type`, and the referenced `spec_id` resolves to an existing file when a spec is required.

The status in `Area_comun/tasks/TASK-XXXX-*.md` and `Area_comun/state/TASK_INDEX.json` must
match.

## Clarity Before Execution

If the requirement is ambiguous, incomplete or internally inconsistent, the agent asks before
implementing. It does not invent scope, steps, acceptance criteria, decisions or tests.

If there is not enough clarity to write a spec, create or request a `discovery` or `analysis` task
instead of an `implementation` task. If the task already exists, set it to `blocked` with one
concrete question.

No implementable task may move to `ready`, `claimed` or `in_progress` unless it declares:

- `spec_id`
- `execution_pipeline`
- `acceptance_criteria`
- `linked_decisions`
- `test_plan`
- `closure_criteria`

The review checks the result against `spec_id`, `acceptance_criteria`, `test_plan` and
`closure_criteria`.

## Task Types

Every new task declares `type`.

Full SDD is required for:

- `implementation`
- `refactor`
- `integration`
- `migration`
- `security`
- `release`

Lightweight SDD is allowed for:

- `discovery`
- `analysis`
- `review`
- `documentation`
- `triage`

Lightweight tasks may use `spec_id: none`, but they must declare:

- `objective`
- `expected_output`
- `question_to_resolve`
- `closure_criterion`

Documentation tasks that change published protocol contracts, templates or user-facing rules may
be treated as implementable by the architect and should use full SDD.

## Claiming Work

1. Read `TASK_INDEX.json`, `CLAIMS.json`, `mailbox/open/` and the task file.
2. Verify dependencies are satisfied.
3. Verify SDD eligibility:
   - full SDD for implementable tasks;
   - lightweight SDD for discovery/analysis/review/documentation/triage;
   - `spec_id` exists when it is not `none`.
4. Set status to `claimed` or `in_progress`.
5. Add or update a claim in `CLAIMS.json`.
6. Work only inside the claimed scope and the task `execution_pipeline`.
7. On completion, create deliverables, create a handoff, set task to `in_review`, and release
   the claim.

### Handoff-release and liveness

- When a task owner moves a task to `in_review` or `done`, that same coordination step releases the
  owner's active claim for the task.
- A task in `in_review` or `done` must not retain an active claim from its owner; this is a validator
  error.
- While holding an active claim on `in_progress` work, each work turn must leave a verifiable signal:
  deliverable progress, a compact FYI, or `blocked` with one concrete question.
- A handoff-release is atomic in intent: the message that declares `in_review`/`done` and the state
  transition (release the claim, flip the status) must land together. If a turn ends with the message
  written but the state not transitioned (claim still `active`, status still `in_progress`), that is an
  anomaly to be notified and completed, not a valid delivery.

### Anomaly notification (DECISION-0018)

An agent that detects an anomaly or inconsistency in another participant's work or in shared state
(incomplete handoff-release, status that contradicts the claims/mailbox, stale or orphaned claim, missing
or mismatched artifact) must notify the responsible owner via `mailbox/open/` with one concrete, actionable
message, and record it. It must not silently fix routes under another owner's active claim, nor leave the
anomaly unsignaled; if the fix needs those routes, it asks the owner (or the human) and waits.

### Concurrent ledger writes / anti-collision (DECISION-0020)

When more than one agent may write the shared ledger (`Area_comun/state/*.json`, mailbox) in overlapping
windows (e.g. an autonomous peer on a short clock plus a reactive agent), every writer follows the
anti-collision rule. It was validated empirically across Phase 5.2/5.3, Phase 6.x and D2.x and addresses
three observed failures (HALLAZGOS):

1. **Prepare out of band.** Specs, tasks and drafts are prepared in the agent's personal area
   `personal/<id>/` (not claimable by the peer) while the peer is busy; they are promoted to shared routes
   only in a safe window.
2. **Safe window.** Before writing the ledger, verify the peer holds no active claim over the routes to
   touch and the working tree shows no half-written peer delivery. If the peer is `in_progress` with an
   active claim or the tree is dirty from the peer, do not touch the ledger: wait (re-arm) and retry.
3. **Atomic ledger write.** Close/enqueue in a single script (ideally one read-modify-write per file) that
   minimizes the interleave window. Create mailbox messages with the file editor, not embedded in fragile
   heredocs.
4. **Artifacts-before-claim (#1).** A claim never lists in its `scope` an artifact that does not exist yet:
   write the artifact first, then the claim that covers it.
5. **Explicit staging when committing (#2).** Stage explicit paths, never broad directories, so concurrent
   peer work is not captured. If edits already interleaved, commit a consistent snapshot (green gates), not
   a half-written state.
6. **Assertions true when written (#3).** Any assertion in mailbox or a shared artifact must be true in the
   ledger at the moment it is written: the "DONE" FYI goes after the status flip; the "X ready" GO goes
   after X is recorded. Create those messages after the atomic script.
7. **Promote one at a time, with GO + ETA.** Promote a single task to `ready` and send a GO with ETA; do not
   enqueue multiple tasks the peer could claim in a race.

This complements DECISION-0018 (handoff-release atomicity) and the claim discipline (DECISION-0007/0011).

### Runtime-authoritative state

In runtime-tier instances that explicitly enable
`event_state.enabled/materialize/enforce/authoritative`, the runtime is the writer for
`Area_comun/state/*.json`. Task, claim and decision transitions must be submitted with
`runtime/submit_intent.py` (or the delegated `.ps1`) as one `task_status`, `task_upsert`, `claim` or
`decision` intent. The caller provides `timestamp` and, when relevant, `commit`; the runtime validates
actor capability, active claim scope and idempotency, appends `intent.applied`, materializes the hot
JSON from replay(log), and keeps task markdown status aligned for task status changes. Manual ledger
edits are drift and the B.3 hard-gate rejects them. The mode is off by default, uses a
content-addressed genesis reference under `runtime/state/snapshots/<hash>.json`, and can be rolled
back by disabling `event_state.enforce`/`authoritative`. Coordination-tier instances keep the manual
ledger process.

### Claim Before Shared Draft

An agent must create or update an active claim **before** creating, editing or leaving any draft in
a shared route. This includes new files, partial drafts, temporary scripts/fixtures that remain in
the workspace, and shared state edits.

Private drafts may live in the participant's personal area `personal/<id>/` without a task claim only when
that route is not covered by another owner's active claim.

If an agent discovers unclaimed work in a shared route, it must not overwrite it. It opens one
mailbox message with one concrete ownership question, then waits or works outside that route.

## Blocking Work

If a task cannot proceed:

1. Set the task to `blocked`.
2. Add one concrete question in `preguntas_abiertas` or `open_questions`.
3. Create a mailbox message if another actor must respond.

Use `blocked` when the spec is missing, the acceptance criteria are not verifiable, decisions
contradict each other, or the test plan cannot prove the requested result.

Before blocking or asking for clarification, formulate **one concrete, minimal question**
(DECISION-0005). If there is more than one question, split them into separate messages or convert
them into a `discovery` task. Reference context by ID/path; do not recap stable context.

## Decisions

Changes to protocol, critical boundaries, architecture, approval policy or compatibility behavior
require an append-only decision in `Area_comun/decisions/`.
