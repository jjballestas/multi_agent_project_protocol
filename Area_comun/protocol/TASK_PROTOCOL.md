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
`closure_criteria`. Reviews also check that any proposed loop/scanner passed the loop governor (see
"Does It Deserve a Loop?"), and may cite a named mode from
[`FAILURE_MODES.md`](FAILURE_MODES.md) when a finding matches one.

## Does It Deserve a Loop? (loop governor)

Before building **any** `discovery_scanner` or autonomy flow (a recurring, self-driven loop), the
proposer must pass this governor. It is a **mandatory pre-check**: a loop/scanner proposal that does not
record all four answers as "yes" is not eligible to be built, and the review rejects it.

**30-second check.** Answer all four. If any answer is "no", do not build a loop: do the work as a
normal owned task (or a manual step), and revisit only if the answers change.

1. **Recurrence** - does the work recur **at least weekly**? (One-off or rare work does not justify a
   standing loop.)
2. **Verifiability** - is there **automated, objective verification** of the result? (A loop whose
   output cannot be checked without a human each cycle is not a loop; it is hidden manual work.)
3. **Economy** - does the **budget absorb the retry**? (The loop's cost, including retries on failure,
   must fit within the cost/deadline caps in `runtime/budget.py`.)
4. **Capability** - does it require **senior-level tools**? (If a simple manual step suffices, a
   dedicated autonomous agent is not warranted.)

Record the four answers in the proposing task (or its decision) so the review can check them.

**Termination/convergence is NOT optional.** Independently of the four answers above, no loop is eligible
unless it has a defined **termination/convergence condition and bound** — it must not be able to run
unbounded. Either state the loop's explicit stop/convergence condition, **or** route its containment to
the supervised-autonomy envelope as a hard requirement: budget/deadline caps and the liveness signal
(FM-1.5 in [`FAILURE_MODES.md`](FAILURE_MODES.md); `runtime/budget.py`; DECISION-0013/0024). A loop with
no bound and no SA envelope is rejected regardless of the four conditions.

**Roadmap rule.** Do **not** build discovery scanners (roadmap E3, Phase 4) before this governor exists,
and **every** expansion of supervised autonomy (e.g. widening the SA.4 window, DECISION-0024/0027) must
pass this governor first. The governor is the standing pre-check for both.

**Scope in time.** This governor binds loop/scanner expansions **decided after it takes effect**. It does
**not** retroactively revoke authority already granted by a prior decision (e.g. the SA.4 pilot,
DECISION-0027): such authority stands under its own terms until its owner re-decides. The governor applies
the next time that authority is **expanded** or a new loop/scanner is proposed.

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

### Final Handoff Envelope

Every task delivery handoff and final implementer/checker report uses this seven-field envelope as the
final text of the turn:

```text
task_id: TASK-XXXX
status: in_review | done | blocked | change_required | no_op
executive_summary: One to three ASCII sentences with the result.
artifacts:
  - path_or_commit: exact path, message id or commit hash
gates:
  - command: exact command
    result: PASS | FAIL | NOT_RUN
next_recommended: One concrete next action, or "none".
risks: Residual risks or "none".
```

The envelope is text in the final report or handoff artifact; it is never a tool call, hidden function
payload or implicit UI state. It must cite exact artifacts and gate results so a cold reviewer can verify
the claim without prior chat context. `gates` records exit-code-backed commands where possible; if a gate
was not run, the entry says `NOT_RUN` and explains why.

### Fix-loop before closure commit

After a checker issues `NO-GO`, `change_required` or equivalent blocking review, the owner performs a
bounded fix-loop before the closure/delivery commit:

1. Apply the remediation in the claimed scope.
2. Re-run the affected gates.
3. Re-judge the fixed result against the original acceptance criteria and the checker finding before
   writing the delivery handoff.
4. Repeat at most two remediation iterations for the same finding set.
5. If the same finding class survives two iterations, stop and escalate to the human owner with one
   concrete question or decision request.

The delivery handoff for a remediation must include the re-judgement in the `executive_summary` or
`risks` field and must preserve maker/checker separation.

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

### Governed delivery reports in mailbox (DECISION-0103 C3/C4)

Starting on 2026-07-22, a mailbox message with `type: REPORTE` that references a governed
`TASK-XXXX` delivery declares `friction_count` as a non-negative integer and `obstacles` as
either `[]` or a list of objects containing exactly `what`, `root_cause`, `resolution`, and
`recurrence_risk` (`low`, `medium`, or `high`). A positive counter with an empty list is
invalid; zero with an empty list is legitimate. `report_schema_version: "1.0"` opts a message
into the same rule independently of its date. Earlier unmarked messages are grandfathered.

This session-layer control proves presence, shape, and internal consistency only. The agent
declares the counter; the validator does not claim to measure whether it is truthful. Automatic
session-friction sensors are outside this contract.

### Runtime-authoritative state

In runtime-tier instances that explicitly enable
`event_state.enabled/materialize/enforce/authoritative`, the runtime is the writer for
`Area_comun/state/*.json`. Task, claim and decision transitions must be submitted with
`runtime/submit_intent.py` (or the delegated `.ps1`) as one `task_status`, `task_upsert`, `claim` or
`decision` intent. The caller provides `timestamp` and, when relevant, `commit`; the runtime validates
actor capability, active claim scope and idempotency, appends `intent.applied`, materializes the hot
JSON from replay(log), and keeps task markdown status aligned for task status changes. Manual ledger
edits are drift and the B.3 hard-gate rejects them. Mechanism vs marker (DECISION-0028, posture B):
`enforce` (the B.3 hard-gate) is the single-writer mechanism that provides the guarantee, while
`authoritative` is the declarative marker that formalizes the mode and has no behavior callers of its
own; no authoritative-specific teeth are wired because no invariant exists that `enforce` does not
already cover, and the guard `authoritative⇒enforce⇒materialize⇒enabled` rejects
authoritative-without-enforce (no false-secure). The mode is off by default, uses a
content-addressed genesis reference under `runtime/state/snapshots/<hash>.json`, and can be rolled
back by disabling `event_state.enforce`/`authoritative`. Coordination-tier instances keep the manual
ledger process.

A close or enqueue that spans several transitions (a `task_status` flip plus a `claim` release plus a
`task_upsert` of the next task, etc.) is submitted as one atomic `submit_intent --intents` transaction:
each intent is validated against the state produced by the prior ones, the transaction emits one
`intent.applied` per intent, materializes once at the end, and rolls back fully on any failure.
`runtime/regenesis.py` writes a fresh genesis reference from the current hot state (drift 0,
non-destructive, idempotent) so the transactional path has a clean replay base. Enabling
`enforce`+`authoritative` is a **coordinated cutover, not a unilateral toggle**: both agent loops must
already route every ledger transition through `submit_intent` before the flip, because once enforce is on
any remaining manual edit hard-fails; the switch is a synchronized re-genesis + flip with a rehearsed
rollback (disable the two flags to return to shadow).

### Exception Events

`runtime/submit_intent.py` also accepts an `exception` intent. A valid submission appends an
`exception.recorded` event to the signed event log and chain without mutating task, claim or project hot
state. The payload is structured and publishable:

```json
{
  "type": "exception",
  "exception_id": "EXC-XXXX",
  "kind": "manual_intervention",
  "task_id": "TASK-XXXX",
  "actor": "Codex",
  "beneficiary": null,
  "summary": "ASCII summary, no PII.",
  "channel": "mailbox",
  "impact": "time",
  "publishable": true
}
```

Allowed `kind` values are `manual_intervention`, `assist`, `arbitration`, `suspension`,
`scope_change`, `intake_exempt`, `risk_reclass`, `budget_overrun` and `other`. Allowed `channel`
values are `chat`, `call`, `mailbox`, `in_person` and `other`. Allowed `impact` values are `none`,
`time`, `scope` and `quality`. `exception_id` is unique, `summary` is ASCII-only and one to three
lines, and a non-null `task_id` must exist.

Use rules:

- U1: Any employee or agent assistance, unblock, defect arbitration, sprint suspension or risk
  reclassification is recorded as `exception.recorded`. What is not recorded does not exist for the
  study.
- U2: The public study report lists the `exception.recorded` events for the period by id, kind,
  task_id, actor, beneficiary, channel, impact and summary. The operator may arbitrate, but the trace
  remains publishable.
- U3: An intake exemption requires a previous `exception.recorded` event with `kind=intake_exempt`.

### Claim Before Shared Draft

An agent must create or update an active claim **before** creating, editing or leaving any draft in
a shared route. This includes new files, partial drafts, temporary scripts/fixtures that remain in
the workspace, and shared state edits.

Private drafts may live in the participant's personal area `personal/<id>/` without a task claim only when
that route is not covered by another owner's active claim.

If an agent discovers unclaimed work in a shared route, it must not overwrite it. It opens one
mailbox message with one concrete ownership question, then waits or works outside that route.

## Coordinated Pruning Checkpoint

Systematic state pruning is maintenance, not collaboration-state validity. A local pre-commit
hook may warn that pruning is due, but it must not reject a commit for that reason; validation,
drift, claim-scope, and other judgment failures remain blocking. CI runs
`python scripts/prune_state.py --root . --check` as the hard integration boundary.

Only the Architect runs `--apply`, inside the existing hygiene checkpoint:

1. Verify the governed worktree is clean and there are zero active peer claims. Check these as
   separate read-only steps before the apply.
2. If either precondition fails, defer pruning. An explicit peer barrier is exceptional and is
   used only when the normal idle checkpoint cannot be obtained.
3. Run `--check`. If pruning is not due, stop; `--apply` also has a cheap read-only no-op path and
   must not open a claim or submit a transaction.
4. If due, run `--apply` through the configured Architect identity. In runtime-authoritative mode
   the script acquires and releases its maintenance claim through `submit_intent`; never edit hot
   state manually.
5. Verify validation, encoding, domain neutrality, and drift, then commit the exact governed paths
   before peers resume. CI must be green before integration.

The checkpoint does not relax claim-as-lock or permit pruning through live peer scopes.

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
