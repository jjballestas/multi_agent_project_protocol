# Analista verdict -- TASK-0259 (C3 obstacles gate: delivery-turn obligation)

Reviewer: Analista (independent adversarial checker)
Date: 2026-07-22 18:37 (local system clock, UTC+2)
Verdict: **NO-GO / CHANGE-REQUIRED**

## Canonical anchor

- Protocol HEAD under review: implementation commit `fc98db7` (delivery `881ecff`), cited by
  the REVIEW instruction MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-obstacles-gate.
- Protocol HEAD == origin/main == `2020c81` (no drift); canonical validate exit 0.
- Task: `Area_comun/tasks/TASK-0259-d0103-c3-turn-validate-obstacles-condicional.md`
  (in_review, owner Codex). Decision: DECISION-0103 clause C3 (runtime carril).
- Scope declared PRODUCT-FREE by the instruction. No product repo in scope.
- Method: fresh `git clone` to `D:/ccv259`, `checkout fc98db7`, gates run THERE by exit code;
  the guard (`is_delivery_turn` / `validate_delivery_obstacles`) extracted and exercised via the
  FULL `validate_turn` against the maker's own fixture builder with my own payloads.

## Reproduction (exit codes, clean clone at fc98db7)

    python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py    -> exit 0
    python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py       -> exit 0  (8 cases)
    python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py     -> exit 0  (5 cases)
    python scripts/validate_collaboration_state.py                            -> exit 0
    python scripts/scan_encoding.py                                           -> exit 0

Note: the task `verification_cmd` lists `run_runtime_turn_cases.py`, which does NOT exist in the
tree (actual runners are `run_runtime_turn_{schema,semantic,obstacle}_cases.py`). Minor DoR
drift, non-blocking, but the stated verification command fails file-not-found as written.

## The predicate under review

    def is_delivery_turn(report):        # runtime/turn_validate.py:220
        return report.get("outcome") in {"in_review", "done"}

    def validate_delivery_obstacles(report):
        if is_delivery_turn(report) and not report.get("obstacles"):
            return ["semantic: delivery turn is missing non-empty obstacles; ..."]
        return []

The predicate keys on the **`outcome` label**. It never reads `transitions.task_status.to`, the
field the rest of `validate_turn` treats as authoritative for the SAME event (capability gating
at line 97-115, race detection at line 320-327, apply.py). Nothing in the schema or the validator
couples `outcome` to `transitions.task_status.to` (grep confirmed: zero coupling).

## Vector-by-vector (behavior on FULL validate_turn, maker fixture state)

| # | Vector (instruction) | Result | Evidence |
|---|----------------------|--------|----------|
| 1 | delivery (outcome=in_review) NO obstacles -> REJECTED with actionable msg | PASS | missing-obstacles error present, no other errors |
| 2 | delivery (outcome=done) EMPTY obstacles [] -> REJECTED | PASS | missing-obstacles error present |
| 3 | non-delivery (outcome=ok, no delivery transition) NO obstacles -> ACCEPTED | PASS | clean control: zero errors |
| 4 | delivery (outcome=in_review) well-formed obstacles -> ACCEPTED | PASS | zero errors |
| P1| PREDICATE false-negative: real delivery to in_review, outcome relabeled 'ok', NO obstacles | **SLIP** | `is_delivery_turn=False`; FULL validate_turn returns **ZERO errors** -> orchestrator commits the delivery with no obstacles |
| P2| PREDICATE false-negative: transition to DONE, outcome='blocked', NO obstacles | **SLIP** | zero errors, accepted |
| P3| PREDICATE false-negative: delivery to in_review, outcome='no_op', NO obstacles | **SLIP** | zero errors, accepted |
| C5| C3 friction sensor on NON-delivery turn (gate_green:false / attempt>1 / revert) | **SLIP** | no friction sensor exists anywhere in runtime/; a blocked/in_progress turn with real friction carries NO obstacles obligation |
| C6| C3 anti-theater: frictionless delivery may leave obstacles empty | **SLIP** | impl forces obstacles on EVERY delivery even with gate green / attempt 1 / no revert |

## The blocker (P1/P2/P3) -- the exact escape the instruction asked me to hunt

The instruction's own question: "el predicado de 'entrega' no deja escapar un turno de entrega
real...?" -- **It does.** A genuine maker delivery -- `transitions.task_status.to: in_review`
(from in_progress), releasing the claim, changing task files -- with `outcome: "ok"` and no
`obstacles` passes the FULL `validate_turn` with **zero errors**. The orchestrator applies the
transition and commits it. The obstacles gate is bypassed by a one-word relabel of an orthogonal
field. Same for `outcome: "blocked"` / `"no_op"` while transitioning to done/in_review.

Money-shot (identical to the clean non-delivery control except that it actually delivers):

    delivery in_progress->in_review, outcome="ok", releases claim, NO obstacles
      -> is_delivery_turn = False ; validate_turn errors = []  (COMMITTED)

This is not a discipline nit. DECISION-0103 C4 states the obstacles rule must be a validator
rule, "no es cuestion de disciplina". A gate defeatable by the agent's free choice of a label
that every other check ignores IS discipline, not enforcement. The maker's permanent-negative
(`is_delivery_turn = lambda: False` reddens) proves the guard is load-bearing WHEN outcome is the
delivery signal; it never tests a delivery signaled by the transition with a divergent outcome,
so it does not cover this vector.

## Scope divergence vs C3 (instruction invited this: "si el alcance quedo corto respecto a C3, dilo")

C3 defines the runtime carril around **friction**, mechanically detectable: `gate_green:false`,
`attempt>1`/bounce, revert -- independent of delivery. TASK-0259 acceptance verbatim: "Los
sensores de friccion quedan documentados en el codigo, que campo del reporte de turno dispara
cada uno... Suite cubre los 3 sensores x (con/sin obstacles) + el caso sin friccion". NONE of the
three sensors exist in the code (grep: the only obstacles logic is the delivery predicate). The
narrowing from "friction sensors" to "delivery/non-delivery" therefore:

- C5 (false negative vs C3): a NON-delivery turn with real friction (blocked/in_progress after a
  red gate, retries or a revert) -- the richest source of lessons -- is under NO obligation. C3:
  "NO puede ir vacia si el turno tuvo friccion"; runtime carril: "el validador puede cruzar gate
  rojo + obstacles vacio = FAIL". Not implemented.
- C6 (false positive vs C3): EVERY delivery, including a clean happy-path turn, is FORCED to
  narrate obstacles. C3: "Lista vacia es respuesta legitima. No se fuerza prosa donde no hubo
  friccion." The impl manufactures exactly the "sin problemas" theater C3's anti-theater rule
  exists to prevent -- visible already in the maker's own positive fixtures, whose obstacle is
  content-free filler ("The fixture must satisfy the delivery reporting contract").

## Closure recommendation

**CHANGE-REQUIRED (NO-GO).** The blocker (P1/P2/P3) fails the narrowed acceptance itself: the
delivery predicate reads the wrong field and the delivery escapes end-to-end. C5/C6 are the
scope-vs-C3 divergences the instruction asked me to weigh; C5 in particular drops the mechanism
C3 names as the runtime carril's whole reason for being.

Minimal fix for the blocker: key `is_delivery_turn` on the authoritative delivery signal
`(report.get("transitions") or {}).get("task_status", {}).get("to") in {"in_review","done"}`
(and/or add a cross-check that outcome agrees with the transition), so the gate reads the same
signal the rest of validate_turn already trusts. A full C3 realization additionally wires the
three friction sensors (gate_green:false / attempt>1 / revert) and makes obstacles conditional on
friction rather than on delivery, restoring C3's "empty is legitimate without friction".

## Declared residuals

- I did not run the runtime orchestrator end-to-end against live hub state; the escape is proven
  through `validate_turn` (the orchestrator's pre-gate), which returns zero errors -- sufficient
  to establish reachability, since a zero-error report is committed.
- The `verification_cmd` filename drift (above) is reported for the Arquitecto to reconcile; it is
  not the basis of this verdict.

## Fix loop declared (CHANGE-REQUIRED)

- Remediation owner: Codex (maker). Affected gates: `runtime/turn_validate.py` +
  `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` (add a delivery-via-transition
  negative and, if C5 is taken, friction-sensor cases) + validate + encoding scan + CI.
- Re-judgement by me (Analista) before the closing commit. Maximum 2 iterations before escalating
  to the human owner.

-- Analista
