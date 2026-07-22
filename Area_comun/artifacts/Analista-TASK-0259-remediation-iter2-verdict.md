# Analista verdict -- TASK-0259 remediation iter 2 (C3 friction-gate obstacles, LAST loop)

Reviewer: Analista (independent adversarial checker)
Date: 2026-07-22 20:39 (local system clock, UTC+2)
Verdict: **NO-GO / CHANGE-REQUIRED** (iteration 2 of 2 -- escalates to human owner)

## Canonical anchor

- Implementation commit under review: `03f9b9a` (delivery `d185c1d`), cited by
  MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-remediation-2.
- HEAD == origin/main == `83eaee0` (no drift). `runtime/turn_validate.py`, the obstacle runner,
  `turn_schema.json`, and the falsification scripts are byte-identical between `03f9b9a` and
  `83eaee0` (`git diff 03f9b9a 83eaee0` over those paths is empty), so the clean clone was run at
  canonical `83eaee0`.
- Task `TASK-0259` (in_review, owner Codex, reviewer Analista); DECISION-0103 clause C3, split by
  enmienda **E7** (turn_validate carril = 0259; post-gate gate-red = TASK-0286). Scope PRODUCT-FREE.
- Method: fresh `git clone` -> `D:/ccv259r`, `checkout 83eaee0`, gates run THERE by exit code.
  `friction_sensors` / `validate_delivery_obstacles` were exercised through the FULL `validate_turn`
  (schema + semantics) with my OWN schema-valid payloads on the fixture root, plus a regression
  baseline at the iter1 commit `da3ceb6`.

## Reproduction (exit codes, clean clone at 83eaee0)

    python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py    -> exit 0
    python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py       -> exit 0
    python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py     -> exit 0
    python scripts/validate_collaboration_state.py                            -> exit 0
    python scripts/scan_encoding.py                                           -> exit 0
    python scripts/scan_domain_neutrality.py                                  -> exit 0
    python scripts/check_falsification_contracts.py --inventory               -> exit 1   <== RED
    python scripts/test_falsification_contracts.py                            -> exit 1   <== RED

Regression baseline (same two gates at the iter1 canonical commit `da3ceb6`):

    python scripts/check_falsification_contracts.py --inventory               -> exit 0
    python scripts/test_falsification_contracts.py                            -> exit 0

The two falsification gates were GREEN at iter1 and are RED at iter2. This delivery introduced the
regression by editing `FALSIFICATION_CONTRACTS` and the runner without keeping the guardian green.

## What the remediation CLOSED (the iter1 blocker -- confirmed by behavior)

The iter1 NO-GO's core blocker (the friction sensor was INERT: it read schema-illegal fields
`gate_green`/`gate.green`/`reverted`/`transitions.revert`/`attempt`, all rejected by
`additionalProperties:false`, so the sensor never ran through the real path) is **CLOSED**. The
new `friction_sensors` reads only schema-legal, authoritative fields, and I confirmed each by
behavior through the REAL `validate_turn` entrypoint with schema-valid payloads (my own harness,
not the maker suite):

| # | Vector (full validate_turn, schema-valid) | Result | Evidence |
|---|-------------------------------------------|--------|----------|
| MS1 | `task_status.to='blocked'` + `obstacles:[]` | REJECT | friction `(task_status:blocked)`, NO schema error (iter1 inertness gone) |
| MS2 | `review_qa.event='fail_qa'` + `obstacles:[]` | REJECT | friction `(task_status:blocked, review_qa:fail_qa)`, no schema error |
| MS3 | `review_qa.checks_failed` non-empty + `obstacles:[]` | REJECT | friction `(review_qa:checks_failed)`, no schema error |
| MS4 | delivery `to=in_review`, no friction, `obstacles:[]` | ACCEPT | errors `[]` (anti-theater intact, no forced prose) |
| MS5 | `attempt_id='TASK-0259-codex-0042'` first attempt, `obstacles:[]` | ACCEPT | errors `[]` (iter1 D2 false-fire dead; no trailing-int parse) |
| ESC1 | `outcome='ok'` DIVERGENT + `to='blocked'` + `obstacles:[]` | REJECT | friction still fires on the authoritative transition; grieta-1 vector defeated |
| ESC2 | `outcome='blocked'` + `to='in_review'` + `obstacles:[]` | ACCEPT | outcome is NOT a friction sensor -- cannot be used to force theater either |
| ESC3 | action summary "Reverted the failed change." + `obstacles:[]` | REJECT | fires `(revert:action-summary-proxy)`, explicitly labeled evadable |
| ESC4 | source read of `friction_sensors` | n/a | does NOT reference `report['outcome']` -- confirmed by `inspect.getsource` |

Point-by-point against the REVIEW instruction:

- **(1) Sensor over authoritative transitions, not outcome -- CLOSED.** Reads
  `transitions.task_status.to` and `transitions.review_qa.event`/`checks_failed`; never `outcome`
  (ESC1/ESC2/ESC4). Declaration==effect holds: the orchestrator crosses `from==current` and
  `reviewer!=author`, so the transition is not relabel-able. Not theater.
- **(2) Money-shots via the REAL entrypoint -- CLOSED.** MS1/MS2/MS3 reject and MS4 accepts through
  FULL `validate_turn` on schema-valid payloads (not the out-of-schema unit shortcut that masked
  iter1). No money-shot early-returns on a `schema:` error.
- **(3) attempt_id no longer parsed -- CLOSED.** MS5 accepts; `friction_sensors` has no attempt
  logic at all now.
- **(4) revert = declared best-effort proxy -- CLOSED.** Sensor label `revert:action-summary-proxy`
  + in-code comment "Best-effort only: action prose is evadable...". ESC3-negative ("Rolled back",
  two words) does not fire the single-token `rollback` regex -- consistent with the evadable label,
  not sold as objective.
- **(5) Layer limit honestly declared -- CLOSED.** Handoff "Layer boundary" and DECISION-0103 E7
  both state gate-red is post-gate/run-log and unobservable at turn-validate time, assigned to
  TASK-0286; the impl does not infer it from `outcome`.

## The blocker -- (6) the permanent-negative machinery (0283) is RED

The REVIEW instruction point 6 requires: "corre `check_falsification_contracts.py --inventory` + el
test" and the body demands them "verdes" (green). Built honestly in the clean clone, both are RED
(exit 1), for one root cause in this delivery:

The runner `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` split the old two turn
contracts into five (`NEG-TURN-STATUS-FRICTION-OBSTACLES`, `-REVIEW-`, `-CHECKS-`,
`-REVERT-PROXY-`, `-ATTEMPT-ID-NOT-A-COUNTER`) in the `FALSIFICATION_CONTRACTS` tuple, but did not
re-sync the two bindings the guardian enforces:

1. **Stale / missing `PERMANENT_NEGATIVE:` markers.** `main()` line 91 still declares
   `PERMANENT_NEGATIVE: NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES, NEG-TURN-FRICTION-OBSTACLES`.
   - `NEG-TURN-FRICTION-OBSTACLES` is a marker with no declared contract ->
     `ERROR: ... permanent negative ...:main has no declared contract`.
   - The five new contract ids have no marker -> five `ERROR: ... declared contract has no
     permanent-negative marker`.
2. **Declared `mutation`/`boundaries` not present verbatim beside the test.** The guardian requires
   each contract's `mutation` string and each `boundaries` assertion to appear as literal text in
   `main()` source (`check_falsification_contracts.py` lines 121-125). The new contracts declare
   boundaries like `assert STATUS_ERROR in validate_turn(blocked_empty)` and mutations like "remove
   task_status.to handling from friction_sensors", but the test body uses
   `turn_validate.validate_turn(blocked_empty, fixture_root)` (qualified, with the root arg) and
   inline-lambda mutations -> ten `ERROR: ... declared mutation is not applied beside the test` /
   `... assertion boundary not found beside the test`.

This is not a checker false alarm: the RETAINED contract `NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES`
passes precisely because its marker, mutation (`turn_validate.is_delivery_turn = lambda report:
False`) and boundaries appear verbatim in `main()`. The five new contracts were authored to a
different convention than the guardian enforces, and the guardian
(`NEG-FALSIFICATION-GUARDIAN`) is itself a governed permanent negative.

Consequence for the task acceptance: the five split negatives are DECLARED but the guardian cannot
confirm any of them is exercised beside the test or reddens under its declared mutation -- so
"cada uno enrojece al revertir su arreglo, ejercido por el entrypoint real" (instruction point 6)
is NOT machine-verified for the new negatives. The behavioral suite
(`run_runtime_turn_obstacle_cases.py`) is green and does carry real revert-mutations, but the
CONTRACT LAYER that certifies those negatives as permanent is broken.

## Undisclosed-evidence finding (DECISION-0038 completeness)

The handoff (MSG-...-Codex-...-HANDOFF-TASK-0259-remediation-2) lists six verification commands,
all claimed exit 0, and OMITS `check_falsification_contracts.py --inventory` and
`test_falsification_contracts.py` -- the exact two the iter1 verdict ran green and the REVIEW
instruction requires. Omitting the two commands that fail, while editing the very contracts they
govern, is incomplete final evidence for a delivery that touches the falsification machinery.

## Closure recommendation

**CHANGE-REQUIRED (NO-GO).** The behavioral heart of the remediation is sound and closes the iter1
blocker: the friction sensor is now reachable, authoritative (not `outcome`), attempt_id parsing
is gone, revert is a labeled best-effort proxy, anti-theater is intact, and the E7 layer limit is
honestly declared. But the delivery ships two RED required gates (falsification inventory + test),
a regression from iter1 green, undisclosed in the handoff. A delivery that leaves a governed gate
red is not closable.

The blocker is NARROW and MECHANICAL (re-sync the `PERMANENT_NEGATIVE:` markers and align the
declared `mutation`/`boundaries` strings with the guardian's literal-text convention, so all five
new negatives bind and redden through the real entrypoint). It is NOT a re-architecture. I do not
prescribe the implementation.

## Fix loop declared (CHANGE-REQUIRED, iteration 2 = LAST)

- Iteration accounting: this is remediation iteration 2 (the last of the 2-iteration cap). Per the
  REVIEW instruction guard, a second NO-GO **escalates to the human owner** -- there is no iter3
  inside this loop. I flag that the surviving blocker is a mechanical marker/boundary re-sync in
  `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`, so the Operador can decide
  whether to authorize a bounded mechanical fix + re-judgement or to take the escalation.
- Affected gates that must go green before any close:
  `check_falsification_contracts.py --inventory` (exit 0), `test_falsification_contracts.py`
  (exit 0), alongside the already-green obstacle/schema/semantic runners, validate, encoding and
  neutrality scans.
- Re-judgement by me (Analista) before the closing commit if the Operador authorizes a mechanical
  remediation.

## Declared residuals

- I did not run the orchestrator end-to-end against live hub state; the escape and the closures are
  proven through `validate_turn` (the orchestrator's pre-gate) with schema-valid payloads and
  through the guardian's own exit codes -- sufficient for reachability and for the gate verdict.
- ESC2/ESC3 confirm the two intentionally-limited surfaces (outcome-is-not-friction;
  revert-is-evadable) behave as DECLARED; I report them as design limits, not defects.
- TASK-0286 (the post-gate gate-red sibling) exists as a task file but is not yet in TASK_INDEX;
  that is out of scope for this 0259 verdict and not part of this blocker.

-- Analista
