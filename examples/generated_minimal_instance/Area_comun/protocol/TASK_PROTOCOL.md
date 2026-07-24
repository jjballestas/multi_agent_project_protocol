# TASK_PROTOCOL.md - Task Workflow

Source of truth: `AGENTS.md`.

## Principles

1. Tasks are small, verifiable and assignable.
2. One task has one owner.
3. Every handoff is self-contained.
4. Ambiguity is made visible as `blocked` plus one concrete question.
5. Shared artifacts reside in `Area_comun/`.
6. Domain-specific boundaries belong to the project instance, not to this generic protocol.

## Lifecycle

```text
proposed -> ready -> claimed -> in_progress -> in_review -> done
                              -> blocked
                              -> cancelled
```

The status in `Area_comun/tasks/TASK-XXXX-*.md` and `Area_comun/state/TASK_INDEX.json` must
match.

## Claiming Work

1. Read `TASK_INDEX.json`, `CLAIMS.json`, `mailbox/open/` and the task file.
2. Verify dependencies are satisfied.
3. Set status to `claimed` or `in_progress`.
4. Add or update a claim in `CLAIMS.json`.
5. Work only inside the claimed scope.
6. On completion, create deliverables, create a handoff, set task to `in_review`, and release
   the claim.

## Blocking Work

If a task cannot proceed:

1. Set the task to `blocked`.
2. Add one concrete question in `preguntas_abiertas` or `open_questions`.
3. Create a mailbox message if another actor must respond.

## Decisions

Changes to protocol, critical boundaries, architecture, or approval policy require an
append-only decision in `Area_comun/decisions/`.
