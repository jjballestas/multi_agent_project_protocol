# Analista verdict -- TASK-0259 remediation iter 3 (guardian re-sync, MECHANICAL)

Reviewer: Analista (independent adversarial checker)
Date: 2026-07-22 21:32 (local system clock, UTC+2)
Verdict: **GO / OK-CLOSABLE** (iteration 3, Operator-authorized mechanical fix after iter2 NO-GO)

## Canonical anchor

- Implementation commit under review: `7c7bc1c` (delivery `03f5bf9`), cited by
  MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-remediation-3.
- HEAD == origin/main == `779fb46` (no drift). The code paths under review
  (`runtime/turn_validate.py`, `runtime/turn_schema.json`, the obstacle runner, the two
  falsification scripts) are byte-identical between `7c7bc1c` and `779fb46`
  (`git diff 7c7bc1c 779fb46` over those paths is empty), so the clean clone at `779fb46`
  faithfully reflects the iter3 implementation.
- Task `TASK-0259` (in_review, owner Codex, reviewer Analista). No active claim over the
  review routes (anti-collision clear). Scope PRODUCT-FREE.
- Method: fresh `git clone` -> `D:/ccv259r3`, `checkout 779fb46`, gates run THERE by exit
  code. Beyond the maker suite I drove the FULL `validate_turn` (schema + semantics) with my
  OWN schema-valid payloads on a fixture root, and I reverted each of the five sensors AT
  SOURCE LEVEL (my own re-implementation of `friction_sensors`, not the maker's monkeypatch)
  to confirm each negative reddens through the real entrypoint.

## Reproduction (exit codes, clean clone at 779fb46)

    python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py    -> exit 0
    python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py       -> exit 0
    python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py     -> exit 0
    python scripts/validate_collaboration_state.py                            -> exit 0
    python scripts/scan_encoding.py                                           -> exit 0
    python scripts/scan_domain_neutrality.py                                  -> exit 0
    python scripts/check_falsification_contracts.py --inventory               -> exit 0   <== GREEN (RED in iter2)
    python scripts/test_falsification_contracts.py                            -> exit 0   <== GREEN (RED in iter2)

The two falsification gates that were RED at iter2 (`03f9b9a`) are GREEN at iter3. The
regression the iter2 NO-GO flagged is closed.

## Vector-by-vector (instruction points 1-4)

| Point | Claim under review | Result | Evidence |
|-------|--------------------|--------|----------|
| (1) | `turn_validate.py`/`turn_schema.json` byte-identical `03f9b9a`->`7c7bc1c` | PASS | `git diff 03f9b9a 7c7bc1c -- runtime/turn_validate.py runtime/turn_schema.json` is EMPTY; only code change is `run_runtime_turn_obstacle_cases.py` (32 lines) |
| (2) | Guardian green by behavior in clean clone | PASS | `check_falsification_contracts.py --inventory` exit 0 AND `test_falsification_contracts.py` exit 0 (both exit 1 at iter2) |
| (3a) | 5 negatives carry a PERMANENT_NEGATIVE marker | PASS | `main()` docstring (line 91) declares all 6: DELIVERY + STATUS + REVIEW + CHECKS + REVERT-PROXY + ATTEMPT-ID; stale `NEG-TURN-FRICTION-OBSTACLES` removed |
| (3b) | mutation/boundaries verbatim beside the test | PASS | Each declared `mutation` and `boundaries` string maps to a REAL executed line in `main()` (mutation lambdas L156/161/167/172/176-178; boundary asserts L119/131/145/148/151/158/164/169/174/179); guardian's substring match points at live test code, not decoration |
| (3c) | Each negative reddens by the REAL entrypoint | PASS | Independent source-level revert (my own `friction_sensors` re-impl, one branch dropped each time) through `validate_turn`: STATUS_ERR/assign_fix/CHECKS_ERR/REVERT_ERR each vanish on revert; ATTEMPT_ERR appears when the counter-parse is reintroduced. Confirms permanence is REAL, not merely that the guardian text-matches |
| (4) MS1 | task_status=blocked + obstacles:[] -> REJECT | PASS | friction `(task_status:blocked)`, no schema error -- identical to iter2 |
| (4) MS2 | review_qa=fail_qa + obstacles:[] -> REJECT | PASS | friction `(task_status:blocked, review_qa:fail_qa)` |
| (4) MS3 | review_qa.checks_failed + obstacles:[] -> REJECT | PASS | friction `(review_qa:checks_failed)` |
| (4) MS4 | friction-free delivery obstacles:[] -> ACCEPT | PASS | errors `[]` (anti-theater intact) |
| (4) MS5 | attempt_id ...-0042 first attempt -> ACCEPT | PASS | errors `[]` (attempt_id not parsed as a counter) |
| (4) ESC1 | outcome=ok DIVERGENT + to=blocked -> REJECT | PASS | sensor keys on the authoritative transition, not outcome |
| (4) ESC2 | outcome=blocked + to=in_review -> ACCEPT | PASS | outcome is not a friction sensor; cannot force theater |
| (4) ESC3 | action "Reverted..." -> REJECT | PASS | fires `revert:action-summary-proxy` (declared evadable) |
| (4) ESC4 | `friction_sensors` source never reads `outcome` | PASS | `inspect.getsource` has no `outcome` reference |

All four instruction points hold. MS1-MS5/ESC1-ESC4 are byte-for-byte the same behavior I
confirmed at iter2 -- expected, since `turn_validate.py` did not change.

## Why the re-sync is a genuine fix, not guardian theater

The guardian (`check_falsification_contracts.py`) is a static TEXT-PRESENCE check: it verifies
each contract's declared `mutation` and `boundaries` appear verbatim in the `exercised_by`
function and that markers and contracts are in bijection. It does not itself execute the
mutation. The iter3 delivery re-aligned the DECLARED strings to the ACTUAL executed test lines
(the qualified `turn_validate.validate_turn(payload, fixture_root)` form and the real
monkeypatch lambdas) -- the correct direction of a re-sync. Execution is then guaranteed by a
SEPARATE gate: `run_runtime_turn_obstacle_cases.py` runs `main()` with live asserts (exit 0),
and my own independent source-level reverts reproduce the reddening through `validate_turn`.
Guardian (declaration binding) + runner (execution) + my independent revert all agree, so the
permanence certification is real.

## Declared residuals (design limits, not defects)

- The revert proxy stays evadable BY DESIGN: my ESC3b probe ("Rolled back the change." -- two
  words) does NOT fire the single-token `rollback` regex. This matches the in-code
  "Best-effort only ... evadable until TASK-0258" label and my iter2 finding; a structured
  revert signal is deferred to TASK-0258. Reported as a declared limit.
- The REVIEW negative's declared positive boundary is an assignment
  (`review_errors = turn_validate.validate_turn(review_empty, fixture_root)`), not an explicit
  `X in ...` assertion; the actual positive assertion (runner line 132) executes but is not a
  guardian-enforced boundary string. Guardian coverage of the review positive direction is thus
  thinner than the other four negatives. Behavior is still proven by the executing runner and by
  my independent revert -- minor residual, not a blocker.
- I did not run the orchestrator end-to-end against live hub state; the reddening and the
  closures are proven through `validate_turn` (the orchestrator's pre-gate) with schema-valid
  payloads plus the guardian's own exit codes -- sufficient for the gate verdict.
- The delivery also touched `runtime/state/events.jsonl`, `runtime/state/snapshot.json` and the
  ledger state files (coordination bookkeeping of the delivery), outside the behavioral surface;
  the protocol validator is green over them.

## Closure recommendation

**GO / OK-CLOSABLE.** The behavioral heart of the remediation is untouched and was already
confirmed sound at iter2 (sensor reachable, authoritative not outcome, attempt_id not parsed,
revert a labeled best-effort proxy, anti-theater intact, E7 layer limit honestly declared). The
sole iter2 blocker -- the two RED falsification gates -- is closed by a purely mechanical,
byte-scoped re-sync of the runner, with the five split negatives now marked, bound verbatim, and
reddening through the real entrypoint (independently reproduced). All eight gates are green in a
clean clone. Arquitecto may proceed to the done-flip.

-- Analista
