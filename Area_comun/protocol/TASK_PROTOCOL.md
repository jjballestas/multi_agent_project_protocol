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

### Claim Before Shared Draft

An agent must create or update an active claim **before** creating, editing or leaving any draft in
a shared route. This includes new files, partial drafts, temporary scripts/fixtures that remain in
the workspace, and shared state edits.

Private drafts may live in the agent private area without a task claim only when that route is not
covered by another owner's active claim.

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
