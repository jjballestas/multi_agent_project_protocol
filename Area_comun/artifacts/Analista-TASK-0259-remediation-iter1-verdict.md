# Analista verdict -- TASK-0259 remediation iter 1 (C3 friction-gate obstacles)

Reviewer: Analista (independent adversarial checker)
Date: 2026-07-22 19:23 (local system clock, UTC+2)
Verdict: **NO-GO / CHANGE-REQUIRED** (iteration 1 of 2)

## Canonical anchor

- Protocol HEAD under review: implementation commit `c725e9b` (delivery `435ab5b`), cited by
  MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-remediation-1.
- HEAD == origin/main == `da3ceb6` (no drift); canonical `validate_collaboration_state.py` exit 0.
- Task `TASK-0259` (in_review, owner Codex, reviewer Analista); DECISION-0103 clause C3 (runtime
  carril). Scope declared PRODUCT-FREE; no product repo in scope.
- Method: fresh `git clone` -> `D:/ccv259r`, `checkout da3ceb6`, gates run THERE by exit code.
  The guard (`is_delivery_turn` / `friction_sensors` / `validate_delivery_obstacles`) was extracted
  and exercised through the FULL `validate_turn` (schema + semantics) with my own payloads, plus
  three revert-mutation experiments against the maker's own suite.

## Reproduction (exit codes, clean clone at da3ceb6)

    python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py    -> exit 0
    python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py       -> exit 0 (8)
    python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py     -> exit 0 (5)
    python scripts/check_falsification_contracts.py --inventory               -> exit 0
      (declares NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES b=3,
       NEG-TURN-FRICTION-OBSTACLES b=4)
    python scripts/test_falsification_contracts.py                            -> exit 0
    python scripts/validate_collaboration_state.py                            -> exit 0
    python scripts/scan_encoding.py                                           -> exit 0

The suite is green. The green is not sufficient: money-shot #2 is proved only against a payload
the real path cannot deliver (see the blocker).

## What the remediation CLOSED (my prior NO-GO's core -- confirmed by behavior)

- **(1) Predicate authoritative -- CLOSED.** `is_delivery_turn` now reads
  `transitions.task_status.to in {in_review, done}`, the same authoritative signal the rest of
  `validate_turn` trusts. Money-shot: a real delivery `in_progress->in_review`, `outcome="ok"`
  (divergent), obstacles removed, through FULL `validate_turn` -> now returns
  `["semantic: delivery turn is missing the obstacles block; ..."]` (was `errors=[]` at fc98db7).
  The P1/P2/P3 relabel escape is gone. Revert-mutation (predicate back to `outcome`) reddens the
  maker suite (exit 1).
- **(3) Anti-theater -- CLOSED.** A delivery with `obstacles: []` and no objective friction,
  through FULL `validate_turn` -> `errors=[]` (accepted). No forced prose. Revert-mutation
  (`"obstacles" not in report` -> `not report.get("obstacles")`) reddens the maker suite (exit 1),
  so the fix is load-bearing.
- **(4) Negatives / mutation -- present.** The two turn contracts are in the inventory; all three
  guarantees redden when their fix is reverted (MUT1 predicate, MUT2 anti-theater, MUT3 friction ->
  exit 1 each; restore -> exit 0).

## The blocker -- (2) FRICTION SENSOR is INERT on any real turn report

Money-shot #2 asks: build a NON-delivery turn with a RED GATE and `obstacles: []` and confirm it
reddens. Built HONESTLY (schema-valid) through the real path, it does NOT redden.

    friction_sensors(report):  # runtime/turn_validate.py:225
      reads report["gate_green"]  and report["gate"]["green"]   (gate-red sensor)
      reads report["attempt"]     then report["attempt_id"]     (retry sensor)
      reads report["reverted"], transitions["revert"], actions[].summary  (revert sensor)

`turn_schema.json` sets `additionalProperties: false` at top level AND on `gate` AND on
`transitions`. So EVERY structured friction field the sensor reads is schema-illegal:

| field read by sensor | schema-legal? | behavior in full validate_turn |
|----------------------|---------------|--------------------------------|
| `gate_green` (top)   | NO | `schema: Additional properties are not allowed ('gate_green' ...)` -> early return, friction NEVER evaluated |
| `gate.green`         | NO | `schema: ... ('green' was unexpected)` -> early return |
| `reverted` (top)     | NO | `schema: ... ('reverted' ...)` -> early return |
| `transitions.revert` | NO | `schema: ... ('revert' ...)` -> early return |
| `attempt` (top, int) | NO | `schema: ... ('attempt' ...)` -> early return (dead read; always falls to attempt_id) |

And architecturally: `validate_turn` runs BEFORE the gate (orchestrator.py:947 validates;
apply.py `apply_gate_and_commit` runs the gate AFTER). `gate_green` / `reverted` are produced by
the gate result and written to the RUN LOG (`runlog.py:116-139`), never to the turn report that
`friction_sensors` receives. At validate time the gate has not run, so a red gate is unknowable to
the report. `friction_sensors` is only ever called with the turn report (grep: sole caller is
`validate_delivery_obstacles`, sole caller of that is `validate_turn`); the docstring's "turn or
runtime result" has no runtime-result caller.

Behavioral proof (FULL validate_turn):

    V2a full delivery + gate_green:false + obstacles [] -> ["schema: ... 'gate_green' ..."]  (NOT friction)
    V2b full delivery + gate:{green:false} + obstacles [] -> ["schema: ... 'green' ..."]     (NOT friction)
    V2c schema-valid blocked turn, obstacles [] (an honest red-gate turn)
        -> validate_turn errors = []   ==> C3 "gate rojo + obstacles vacio = FAIL" NOT ENFORCED

The maker suite makes the gate-red case red ONLY by calling
`validate_delivery_obstacles({"outcome":"blocked","gate_green":False,"obstacles":[]})` at the UNIT
level, bypassing the schema gate with an out-of-schema field. That is testing the guard by a
payload the real path can never deliver -- the exact "unit not behavior" trap.

## Vector-by-vector (behavior on FULL validate_turn)

| # | Vector | Result | Evidence |
|---|--------|--------|----------|
| 1 | delivery in_progress->in_review, outcome=ok DIVERGENT, no obstacles -> RED | PASS | DELIVERY_ERR present; was [] at fc98db7 |
| 3 | delivery, obstacles [], no friction -> ACCEPTED | PASS | errors=[] |
| 2a| full turn + gate_green:false + obstacles [] -> friction RED | **SLIP** | schema error, friction never runs |
| 2b| full turn + gate.green:false + obstacles [] -> friction RED | **SLIP** | schema error, friction never runs |
| 2c| honest schema-valid red-gate turn, obstacles [] -> RED | **SLIP** | errors=[]; C3 gate-red rule unenforced |
| D | non-delivery attempt_id="attempt-2", obstacles [] -> RED | PASS | fires "attempt>1" (attempt_id is schema-legal) |
| D2| non-delivery attempt_id="TASK-0259-codex-0042" (FIRST attempt), obstacles [] | **SLIP** | FALSE friction: grabs trailing int 42 -> "attempt>1" over-fires on a benign idempotency id |
| E | non-delivery actions[].summary "Reverted...", obstacles [] -> RED | PASS | fires "revert" (actions summary is schema-legal) |

Net: of the three friction sensors, only the retry (attempt_id) and revert (actions.summary)
signals reach the guard on schema-valid input; the retry one over-fires on benign ids and its
int `attempt` path is dead. The gate-red sensor -- the one C3's runtime carril names first
("el validador puede cruzar gate rojo + obstacles vacio = FAIL") and the one money-shot #2 names
-- cannot fire on any real turn report.

## Acceptance violation (undisclosed)

TASK-0259 acceptance: "Si algun sensor no es derivable del reporte actual ... la unidad lo declara
en el handoff y lo implementa sobre el campo real disponible, SIN INVENTAR campos fuera de
TASK-0258." The impl invents `gate_green`, `gate.green`, `attempt`, `reverted`,
`transitions.revert` -- none in the TASK-0258 turn schema -- and the handoff
(MSG-...-Codex-...-HANDOFF-remediation-1) does NOT declare that gate-red is non-derivable at
turn-validate time; it asserts "Gate-red ... cases with empty obstacles are rejected" without
disclosing that this holds only against out-of-schema input, not through `validate_turn`.

## Closure recommendation

**CHANGE-REQUIRED (NO-GO).** Grieta (1) predicate and grieta (3) anti-theater are closed and
load-bearing. Grieta (2) friction sensor is NOT closed when tested by behavior: the gate-red
sensor is inert on real turn reports, so C3's headline runtime-carril rule is unenforceable, and
the green suite masks this by exercising the sensor with a schema-illegal payload.

Direction for iteration 2 (maker/Arquitecto choose; I do not prescribe an implementation):

- Restrict the sensor honestly to the schema-derivable signals (attempt_id, actions[].summary),
  fix the attempt_id over-fire (do not treat any trailing integer as an attempt count), and
  DECLARE in the handoff that gate-red is not observable at turn-validate time; OR
- Move the friction obligation to a post-gate check over the run-log entry
  (`gate_green`/`reverted` exist THERE), i.e. a second validation pass after the gate; OR
- Add the friction fields to the turn schema -- but that is TASK-0258 scope and out of scope for
  0259, so it needs coordination, not a silent invention here.
- Whichever path: the negative for gate-red must be exercised through the REAL entrypoint that
  receives the field, not by feeding an out-of-schema field to the unit function.

## Declared residuals

- I did not run the orchestrator end-to-end against live hub state; the escape is proven through
  `validate_turn` (the orchestrator's pre-gate) returning zero errors on an honest red-gate turn,
  and through schema rejection of the invented fields -- sufficient for reachability.
- The retry sensor over-fire (D2) is reported as a correctness defect adjacent to the blocker; it
  is not the sole basis of the verdict.

## Fix loop declared (CHANGE-REQUIRED)

- Iteration accounting: this is remediation iteration 1; my NO-GO defines iteration 2. Affected
  gates: `runtime/turn_validate.py` + `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`
  (exercise gate-red friction through the real entrypoint, not the unit shortcut) + obstacle/
  semantic/schema runners + falsification test + validate + encoding scan.
- Re-judgement by me (Analista) before the closing commit. A second NO-GO escalates to the human
  owner.

-- Analista
