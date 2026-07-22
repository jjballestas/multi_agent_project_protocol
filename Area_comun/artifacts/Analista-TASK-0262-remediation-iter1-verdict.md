---
artifact_id: Analista-TASK-0262-remediation-iter1-verdict
author: Analista
role: adversarial-checker
task_id: TASK-0262
review_iteration: remediation-iter1
verdict: OK-CLOSABLE
date: 2026-07-23
---

# Analista verdict -- TASK-0262 remediation iter1 (assignment candidate key)

Local time: 2026-07-23 00:54 (UTC+2). Reviewer: Analista (independent adversarial voice).
Scope: SIN PRODUCTO -- protocol docs + validator only. This verdict gates closure.

Re-judgment of the single slip my prior CHANGE-REQUIRED
(`Analista-TASK-0262-plantillas-reporte-asignacion-verdict.md`, vector 4) raised: the
assignment template annotated the candidate identifier as `agent_id`, but the real routing
candidate key is `agent`.

## Canonical anchor

- Remediation impl commit under review: `c7ffa91` ("docs(protocol): correct assignment candidate key").
- Protocol HEAD at review time (canonical live state, validate green): `dfff6db`.
- Template stable across the interval: `git diff --stat c7ffa91 dfff6db -- Area_comun/protocol/MAILBOX_REPORT_TEMPLATES.md` is EMPTY (later commits are ledger/coordination only).
- Clean clone (never in-place): cloned to `D:/ccv0262b`, checked out `dfff6db`, gates run THERE, then removed.
- Real routing key cross-referenced at HEAD: `runtime/router.py:390` emits the candidate object as `{"agent": agent_id, ...}` inside `routing_decision.explanation.candidates`; the identifier lives under key `agent` (the `agent_id` on the right is a local variable name, not a dict key).

## Reproduction (exit-code gated, clean clone @ dfff6db)

```
python scripts/validate_collaboration_state.py                 -> OK, exit 0
python scripts/scan_encoding.py                                -> OK, exit 0
python scripts/scan_domain_neutrality.py                       -> exit 0
python examples/mailbox_report_cases/run_mailbox_report_cases.py -> OK (17), exit 0
git diff --check c7ffa91^ c7ffa91                              -> exit 0 (no whitespace defects)
git grep -n "agent_id" -- Area_comun/protocol/MAILBOX_REPORT_TEMPLATES.md -> no match, exit 1 (ZERO residual)
```

Central behavioral re-check (the changed example must still validate GREEN and must genuinely
flow through the governed report path): I extracted the THREE concrete examples verbatim from
the CURRENT template (fenced-block slices, no retyping) into real
`Area_comun/mailbox/open/MSG-*.md` files in the clean clone and validated:

```
assignment (agent: MakerA / agent: MakerB, friction 0 + obstacles [])  -> validate exit 0
delivery with friction (friction 1 + 1 obstacle)                        -> validate exit 0
delivery without friction (friction 0 + obstacles [])                   -> validate exit 0
(only a non-fatal context_refs WARNING on the assignment example; warnings do not fail)
```

Negative control on the CHANGED example (proves the assignment report is genuinely exercised,
not trivially skipped after the key rename):

```
mutant: assignment friction_count 2 + obstacles []
  -> FAIL exit 1: "Governed REPORTE ... declares friction_count > 0 but obstacles is empty"
```

The assignment example flows through `validate_governed_mailbox_report` and passes only because
it is well formed; the `agent_id -> agent` rename did not break that path.

## Vector-by-vector

| # | Vector | Result | Evidence |
|---|--------|--------|----------|
| 1 | Fix: `agent_id` -> `agent` in annotation AND example (both candidates), pointing to `...candidates[].agent`, zero `agent_id` residual | PASS | `git show c7ffa91` template hunk changes exactly 3 lines: annotation `<... candidates item agent>` + `agent: MakerA` + `agent: MakerB`. `git grep agent_id` on the template = no match. Matches real key `router.py:390`. |
| 2a | No-regression: obstacles block three-way identical to TASK-0258 | PASS | Template obstacle fields `what, root_cause, resolution, recurrence_risk` + enum `low` unchanged by the fix; validator `OBSTACLE_FIELDS`/`OBSTACLE_RISKS` (validate lines 79-80, 613-619) match. Fix touched no obstacle line. |
| 2b | No-regression: the 3 examples PASS validate_mailbox of 0261; the assignment one stays VERDE after the key change | PASS | All 3 extracted examples validate exit 0; assignment mutant fails exit 1. Path genuinely exercised. |
| 2c | No-regression: R1 closed (temporal anchor mandatory), complete examples, neutrality + ASCII | PASS | Common-rules anchor mandate and the 3 complete example blocks untouched by the fix; scan_domain_neutrality + scan_encoding exit 0. |
| 3 | Scope: change is ONLY the candidate key; nothing to REPORTE structure / schema / anchor / runtime | PASS | Template diff is the 3 candidate-key lines only. Other files in `c7ffa91` (CLAIMS/PROJECT_STATE/TASK_INDEX/events.jsonl/snapshot/task file) are the delivery's ledger housekeeping, not template content. |
| 4 | The prior slip (vector 4) is resolved | PASS | Provenance pointer and both concrete values now name the real routing key `agent`; no reader can infer a non-existent runtime `agent_id` key. |

## Declared residuals (benign, NOT blockers)

- R-a: The extracted assignment example emits a non-fatal `context_refs` WARNING when placed as
  a real compact mailbox message. Warnings do not fail the validator; unchanged from iter1 and
  not in scope.
- R-b: The no-anchor-treated-as-historical grandfathering is 0261 validator design, out of scope
  here; 0262 closes R1 for template FOLLOWERS by making the anchor mandatory in the template.

## Closure recommendation: OK-CLOSABLE (GO)

The single slip is fixed, cero residual, no regression across the 5 vectors that passed in iter1,
and the scope is exactly the candidate key. All gates exit 0 in a clean clone at the canonical
HEAD. TASK-0262 is closable. Fix loop consumed: 1 of max 2 iterations; no further remediation
required.
